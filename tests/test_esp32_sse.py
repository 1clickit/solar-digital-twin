import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from solar_digital_twin.collectors import esp32_sse


def sse_event(entity_id, value):
    return "data:" + json.dumps(
        {
            "id": entity_id,
            "name": "Test entity",
            "domain": "sensor",
            "value": value,
            "state": str(value),
        }
    )


class FakeResponse:
    def __init__(self, lines=(), interrupt=False):
        self.lines = lines
        self.interrupt = interrupt
        self.closed = False

    def raise_for_status(self):
        return None

    def iter_lines(self, **_kwargs):
        yield from self.lines
        if self.interrupt:
            raise KeyboardInterrupt

    def close(self):
        self.closed = True


class FileDouble:
    def __init__(self, label, events=None, fail_write=False, fail_flush=False):
        self.label = label
        self.events = events if events is not None else []
        self.fail_write = fail_write
        self.fail_flush = fail_flush
        self.lines = []
        self.closed = False
        self.flushes = 0

    def write(self, value):
        self.events.append(f"{self.label}_write")
        if self.fail_write:
            raise OSError("simulated retained failure with private data")
        self.lines.append(value)
        return len(value)

    def flush(self):
        self.events.append(f"{self.label}_flush")
        if self.fail_flush:
            raise OSError("simulated retained flush failure with private data")
        self.flushes += 1

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


class CollectorHarness:
    def __init__(self, raw=None, retained=None):
        self.raw = raw or FileDouble("raw")
        self.retained = retained or FileDouble("retained")
        self.tempdir = TemporaryDirectory()
        self.raw_path = Path(self.tempdir.name) / "esp32_sse_test.ndjson"

    def cleanup(self):
        self.tempdir.cleanup()

    def patches(self, request_side_effect, **extra):
        opened = iter((self.raw, self.retained))
        patches = [
            patch.object(esp32_sse, "new_output_path", return_value=self.raw_path),
            patch.object(Path, "mkdir"),
            patch.object(Path, "open", side_effect=lambda *args, **kwargs: next(opened)),
            patch.object(
                esp32_sse.requests,
                "get",
                side_effect=request_side_effect,
            ),
            patch.object(esp32_sse.time, "sleep"),
        ]
        patches.extend(extra.values())
        return patches


class Esp32CollectorTests(unittest.TestCase):
    def make_harness(self, raw=None, retained=None):
        harness = CollectorHarness(raw, retained)
        self.addCleanup(harness.cleanup)
        return harness

    def run_until_interrupt(self, harness, responses, **extra_patches):
        patches = harness.patches(
            [*responses, KeyboardInterrupt()],
            **extra_patches,
        )
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            for extra in patches[5:]:
                extra.start()
            try:
                with self.assertRaises(KeyboardInterrupt):
                    esp32_sse.collect(0)
            finally:
                for extra in reversed(patches[5:]):
                    extra.stop()

    def test_raw_is_flushed_before_retained_processing_and_records_match(self):
        events = []
        harness = self.make_harness(
            FileDouble("raw", events),
            FileDouble("retained", events),
        )

        def retain_after_raw(record, policy, monotonic_now):
            self.assertEqual(events[-1], "raw_flush")
            return True

        self.run_until_interrupt(
            harness,
            [FakeResponse([sse_event("text_sensor-00_current_status", "On")])],
            retain=patch.object(
                esp32_sse,
                "should_retain_record",
                side_effect=retain_after_raw,
            ),
        )

        self.assertEqual(harness.raw.lines, harness.retained.lines)
        self.assertEqual(
            events[:4],
            ["raw_write", "raw_flush", "retained_write", "retained_flush"],
        )

    def test_retained_path_is_a_predictable_sibling(self):
        raw = Path("evidence/esp32/esp32_sse_20260714_120000Z.ndjson")

        self.assertEqual(
            esp32_sse.retained_output_path(raw),
            Path(
                "evidence/esp32/"
                "esp32_sse_20260714_120000Z_retained.ndjson"
            ),
        )

    def test_allowlist_and_receipt_timestamp_are_unchanged(self):
        harness = self.make_harness()
        response = FakeResponse(
            [
                sse_event("not-approved", 1),
                sse_event("sensor-01_gen_frequency", 60.0),
            ]
        )
        self.run_until_interrupt(
            harness,
            [response],
            timestamp=patch.object(
                esp32_sse,
                "receipt_timestamp",
                return_value="2026-07-14T12:00:00.000Z",
            ),
        )

        self.assertEqual(len(harness.raw.lines), 1)
        record = json.loads(harness.raw.lines[0])
        self.assertEqual(record["id"], "sensor-01_gen_frequency")
        self.assertEqual(record["received_at_utc"], "2026-07-14T12:00:00.000Z")
        self.assertEqual(list(record), [
            "received_at_utc", "source_url", "id", "name", "domain",
            "value", "state",
        ])

    def test_frequency_policy_state_survives_reconnect(self):
        harness = self.make_harness()
        responses = [
            FakeResponse([sse_event("sensor-01_gen_frequency", 60.00)]),
            FakeResponse(
                [
                    sse_event("sensor-01_gen_frequency", 60.03),
                    sse_event("sensor-01_gen_frequency", 60.04),
                ]
            ),
        ]
        self.run_until_interrupt(harness, responses)

        self.assertEqual(len(harness.raw.lines), 3)
        self.assertEqual(
            [json.loads(line)["value"] for line in harness.retained.lines],
            [60.0, 60.04],
        )

    def test_frequency_policy_state_starts_fresh_for_each_collect_run(self):
        first_run = self.make_harness()
        second_run = self.make_harness()

        self.run_until_interrupt(
            first_run,
            [FakeResponse([sse_event("sensor-01_gen_frequency", 60.0)])],
        )
        self.run_until_interrupt(
            second_run,
            [FakeResponse([sse_event("sensor-01_gen_frequency", 60.0)])],
        )

        self.assertEqual(len(first_run.retained.lines), 1)
        self.assertEqual(len(second_run.retained.lines), 1)

    def test_duration_expiry_closes_both_outputs(self):
        harness = self.make_harness()
        patches = harness.patches([FakeResponse([sse_event("sensor-01_gen_frequency", 60)])])
        monotonic = patch.object(
            esp32_sse.time,
            "monotonic",
            side_effect=[0.0, 0.0, 1.0],
        )
        with patches[0], patches[1], patches[2], patches[3], patches[4], monotonic:
            esp32_sse.collect(1.0)

        self.assertTrue(harness.raw.closed)
        self.assertTrue(harness.retained.closed)

    def test_keyboard_interrupt_closes_both_outputs(self):
        harness = self.make_harness()
        self.run_until_interrupt(harness, [FakeResponse(interrupt=True)])

        self.assertTrue(harness.raw.closed)
        self.assertTrue(harness.retained.closed)

    def test_retained_write_failure_is_reported_once_and_raw_continues(self):
        retained = FileDouble("retained", fail_write=True)
        harness = self.make_harness(retained=retained)
        response = FakeResponse(
            [
                sse_event("text_sensor-00_current_status", "One"),
                sse_event("text_sensor-00_current_status", "Two"),
            ],
            interrupt=True,
        )
        output = StringIO()

        with redirect_stdout(output):
            self.run_until_interrupt(harness, [response])

        self.assertEqual(len(harness.raw.lines), 2)
        self.assertEqual(retained.events.count("retained_write"), 1)
        self.assertEqual(output.getvalue().count("Retained ESP32 output disabled"), 1)
        self.assertNotIn("private data", output.getvalue())
        self.assertTrue(retained.closed)

    def test_retained_open_failure_does_not_stop_raw_collection(self):
        harness = self.make_harness()
        open_count = 0

        def open_output(*_args, **_kwargs):
            nonlocal open_count
            open_count += 1
            if open_count == 1:
                return harness.raw
            raise OSError("private retained path details")

        response = FakeResponse(
            [sse_event("text_sensor-00_current_status", "One")],
            interrupt=True,
        )
        output = StringIO()
        with (
            patch.object(esp32_sse, "new_output_path", return_value=harness.raw_path),
            patch.object(Path, "mkdir"),
            patch.object(Path, "open", side_effect=open_output),
            patch.object(esp32_sse.requests, "get", return_value=response),
            redirect_stdout(output),
            self.assertRaises(KeyboardInterrupt),
        ):
            esp32_sse.collect(0)

        self.assertEqual(len(harness.raw.lines), 1)
        self.assertEqual(output.getvalue().count("Retained ESP32 output disabled"), 1)
        self.assertNotIn("private retained", output.getvalue())

    def test_retained_flush_failure_disables_retention_only(self):
        retained = FileDouble("retained", fail_flush=True)
        harness = self.make_harness(retained=retained)
        response = FakeResponse(
            [
                sse_event("text_sensor-00_current_status", "One"),
                sse_event("text_sensor-00_current_status", "Two"),
            ],
            interrupt=True,
        )

        with redirect_stdout(StringIO()):
            self.run_until_interrupt(harness, [response])

        self.assertEqual(len(harness.raw.lines), 2)
        self.assertEqual(retained.events.count("retained_flush"), 1)

    def test_retained_processing_failure_disables_retention_only(self):
        harness = self.make_harness()
        response = FakeResponse(
            [
                sse_event("sensor-01_gen_frequency", 60.0),
                sse_event("sensor-01_gen_frequency", 60.1),
            ],
            interrupt=True,
        )

        with redirect_stdout(StringIO()):
            self.run_until_interrupt(
                harness,
                [response],
                retain=patch.object(
                    esp32_sse,
                    "should_retain_record",
                    side_effect=ValueError("private record value"),
                ),
            )

        self.assertEqual(len(harness.raw.lines), 2)
        self.assertEqual(harness.retained.lines, [])


if __name__ == "__main__":
    unittest.main()
