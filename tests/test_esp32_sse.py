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
    def __init__(self, raw=None, retained=None, manifest=None, conservative=None):
        self.raw = raw or FileDouble("raw")
        self.retained = retained or FileDouble("retained")
        self.manifest = manifest or FileDouble("manifest")
        self.conservative = conservative or FileDouble("conservative")
        self.tempdir = TemporaryDirectory()
        self.raw_path = Path(self.tempdir.name) / "esp32_sse_test.ndjson"

    def cleanup(self):
        self.tempdir.cleanup()

    def patches(self, request_side_effect, mode="current", **extra):
        outputs = [self.manifest, self.raw, self.retained]
        if mode == "canary":
            outputs.append(self.conservative)
        opened = iter(outputs)
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
    def make_harness(self, raw=None, retained=None, manifest=None, conservative=None):
        harness = CollectorHarness(raw, retained, manifest, conservative)
        self.addCleanup(harness.cleanup)
        return harness

    def run_until_interrupt(
        self, harness, responses, mode="current", **extra_patches
    ):
        patches = harness.patches(
            [*responses, KeyboardInterrupt()],
            mode=mode,
            **extra_patches,
        )
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            for extra in patches[5:]:
                extra.start()
            try:
                with self.assertRaises(KeyboardInterrupt):
                    esp32_sse.collect(
                        0,
                        retention_mode=mode,
                        collector_version=(
                            "test-version" if mode != "current" else None
                        ),
                    )
            finally:
                for extra in reversed(patches[5:]):
                    extra.stop()

    def test_raw_is_flushed_before_retained_processing_and_records_match(self):
        events = []
        harness = self.make_harness(
            FileDouble("raw", events),
            FileDouble("retained", events),
        )

        def retain_after_raw(record, monotonic_now):
            self.assertEqual(events[-1], "raw_flush")
            return "pass_through"

        self.run_until_interrupt(
            harness,
            [FakeResponse([sse_event("text_sensor-00_current_status", "On")])],
            retain=patch.object(
                esp32_sse.CurrentESP32RetentionPolicy,
                "retention_reason",
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
        self.assertEqual(
            esp32_sse.conservative_output_path(raw),
            Path(
                "evidence/esp32/"
                "esp32_sse_20260714_120000Z_"
                "retained_esp32-conservative-v1.ndjson"
            ),
        )
        self.assertEqual(
            esp32_sse.manifest_output_path(raw),
            Path("evidence/esp32/esp32_sse_20260714_120000Z_manifest.ndjson"),
        )

    def test_explicit_output_directory_preserves_default_naming(self):
        output_dir = Path("isolated/capture/esp32")
        with patch.object(esp32_sse, "datetime") as mocked_datetime:
            mocked_datetime.now.return_value.strftime.return_value = (
                "20260718_120000Z"
            )
            output = esp32_sse.new_output_path(output_dir)

        self.assertEqual(
            output,
            output_dir / "esp32_sse_20260718_120000Z.ndjson",
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

    def test_both_policy_states_survive_one_stream_reconnect(self):
        harness = self.make_harness()
        responses = [
            FakeResponse([sse_event("sensor-01_gen_frequency", 60.00)]),
            FakeResponse(
                [
                    sse_event("sensor-01_gen_frequency", 60.03),
                    sse_event("sensor-01_gen_frequency", 60.04),
                ],
                interrupt=True,
            ),
        ]
        self.run_until_interrupt(harness, responses, mode="canary")

        expected = [60.0, 60.04]
        self.assertEqual(
            [json.loads(line)["value"] for line in harness.retained.lines],
            expected,
        )
        self.assertEqual(
            [json.loads(line)["value"] for line in harness.conservative.lines],
            expected,
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
        self.assertTrue(harness.manifest.closed)
        manifest = [json.loads(line) for line in harness.manifest.lines]
        self.assertEqual([item["event"] for item in manifest], ["start", "completion"])
        self.assertEqual(manifest[0]["retained_outputs"][0]["policy_id"], "esp32-frequency-v1")

    def test_keyboard_interrupt_closes_both_outputs(self):
        harness = self.make_harness()
        self.run_until_interrupt(harness, [FakeResponse(interrupt=True)])

        self.assertTrue(harness.raw.closed)
        self.assertTrue(harness.retained.closed)
        self.assertTrue(harness.manifest.closed)
        manifest = [json.loads(line) for line in harness.manifest.lines]
        self.assertEqual(manifest[-1]["event"], "interruption")
        self.assertEqual(manifest[-1]["stop_reason"], "keyboard_interrupt")

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
                return harness.manifest
            if open_count == 2:
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
                    esp32_sse.CurrentESP32RetentionPolicy,
                    "retention_reason",
                    side_effect=ValueError("private record value"),
                ),
            )

        self.assertEqual(len(harness.raw.lines), 2)
        self.assertEqual(harness.retained.lines, [])

    def test_canary_uses_one_stream_and_independent_retained_writers(self):
        harness = self.make_harness()
        response = FakeResponse(
            [
                sse_event("sensor-01_gen_frequency", 60.0),
                sse_event("text_sensor-00_current_status", "NORMAL"),
            ],
            interrupt=True,
        )
        self.run_until_interrupt(harness, [response], mode="canary")

        self.assertEqual(len(harness.raw.lines), 2)
        self.assertEqual(len(harness.retained.lines), 2)
        self.assertEqual(len(harness.conservative.lines), 2)
        manifest = [json.loads(line) for line in harness.manifest.lines]
        self.assertTrue(manifest[0]["canary"])
        self.assertEqual(manifest[0]["collector_version"], "test-version")
        self.assertEqual(
            [item["policy_id"] for item in manifest[0]["retained_outputs"]],
            ["esp32-frequency-v1", "esp32-conservative-v1"],
        )
        self.assertTrue(harness.retained.closed)
        self.assertTrue(harness.conservative.closed)

    def test_conservative_failure_does_not_disable_current_output(self):
        conservative = FileDouble("conservative", fail_write=True)
        harness = self.make_harness(conservative=conservative)
        response = FakeResponse(
            [
                sse_event("text_sensor-00_current_status", "One"),
                sse_event("text_sensor-00_current_status", "Two"),
            ],
            interrupt=True,
        )
        with redirect_stdout(StringIO()):
            self.run_until_interrupt(harness, [response], mode="canary")

        self.assertEqual(len(harness.raw.lines), 2)
        self.assertEqual(len(harness.retained.lines), 2)
        self.assertEqual(conservative.events.count("conservative_write"), 1)
        manifest = [json.loads(line) for line in harness.manifest.lines]
        candidate = manifest[-1]["retained_outputs"][1]
        self.assertEqual(candidate["status"], "disabled")
        self.assertEqual(candidate["error_type"], "OSError")

    def test_current_failure_does_not_disable_conservative_output(self):
        retained = FileDouble("retained", fail_write=True)
        harness = self.make_harness(retained=retained)
        response = FakeResponse(
            [
                sse_event("text_sensor-00_current_status", "One"),
                sse_event("text_sensor-00_current_status", "Two"),
            ],
            interrupt=True,
        )
        with redirect_stdout(StringIO()):
            self.run_until_interrupt(harness, [response], mode="canary")

        self.assertEqual(len(harness.raw.lines), 2)
        self.assertEqual(len(harness.conservative.lines), 2)

    def test_both_retained_failures_leave_raw_collection_active(self):
        harness = self.make_harness(
            retained=FileDouble("retained", fail_write=True),
            conservative=FileDouble("conservative", fail_write=True),
        )
        response = FakeResponse(
            [
                sse_event("text_sensor-00_current_status", "One"),
                sse_event("text_sensor-00_current_status", "Two"),
            ],
            interrupt=True,
        )
        with redirect_stdout(StringIO()):
            self.run_until_interrupt(harness, [response], mode="canary")

        self.assertEqual(len(harness.raw.lines), 2)
        final = json.loads(harness.manifest.lines[-1])
        self.assertEqual(
            [item["status"] for item in final["retained_outputs"]],
            ["disabled", "disabled"],
        )

    def test_retained_failure_is_not_manifested_as_normal_completion(self):
        harness = self.make_harness(retained=FileDouble("retained", fail_write=True))
        response = FakeResponse(
            [sse_event("text_sensor-00_current_status", "One")]
        )
        patches = harness.patches([response])
        monotonic = patch.object(
            esp32_sse.time,
            "monotonic",
            side_effect=[0.0, 0.0, 0.0, 0.1, 1.0],
        )
        with (
            patches[0],
            patches[1],
            patches[2],
            patches[3],
            patches[4],
            monotonic,
            redirect_stdout(StringIO()),
        ):
            esp32_sse.collect(1.0)

        final = json.loads(harness.manifest.lines[-1])
        self.assertEqual(final["event"], "retained_output_failure")
        self.assertEqual(final["stop_reason"], "retained_output_disabled")
        self.assertEqual(len(harness.raw.lines), 1)

    def test_opt_in_modes_require_explicit_collector_version(self):
        with self.assertRaisesRegex(ValueError, "collector_version"):
            esp32_sse.collect(1, retention_mode="canary")

    def test_default_mode_does_not_open_conservative_output(self):
        harness = self.make_harness()
        self.run_until_interrupt(
            harness,
            [FakeResponse([sse_event("text_sensor-00_current_status", "One")])],
        )
        self.assertEqual(harness.conservative.lines, [])
        self.assertFalse(harness.conservative.closed)
        start = json.loads(harness.manifest.lines[0])
        self.assertFalse(start["canary"])
        self.assertEqual(start["retention_mode"], "current")

    def test_any_existing_canary_path_refuses_before_network_or_truncation(self):
        with TemporaryDirectory() as directory:
            raw = Path(directory) / "esp32_sse_collision.ndjson"
            paths = [
                raw,
                esp32_sse.retained_output_path(raw),
                esp32_sse.conservative_output_path(raw),
                esp32_sse.manifest_output_path(raw),
            ]
            for existing in paths:
                with self.subTest(existing=existing.name):
                    for path in paths:
                        path.unlink(missing_ok=True)
                    existing.write_text("preserve-me")
                    with (
                        patch.object(
                            esp32_sse, "new_output_path", return_value=raw
                        ),
                        patch.object(esp32_sse.requests, "get") as get,
                        self.assertRaisesRegex(FileExistsError, "already exists"),
                    ):
                        esp32_sse.collect(
                            1,
                            retention_mode="canary",
                            collector_version="test-version",
                        )
                    get.assert_not_called()
                    self.assertEqual(existing.read_text(), "preserve-me")

    def test_raw_write_failure_is_manifested_and_stops_collection(self):
        raw = FileDouble("raw", fail_write=True)
        harness = self.make_harness(raw=raw)
        response = FakeResponse(
            [sse_event("text_sensor-00_current_status", "One")]
        )
        patches = harness.patches([response])
        with (
            patches[0],
            patches[1],
            patches[2],
            patches[3],
            patches[4],
            self.assertRaises(OSError),
        ):
            esp32_sse.collect(0)
        manifest = [json.loads(line) for line in harness.manifest.lines]
        self.assertEqual(manifest[-1]["event"], "failure")
        self.assertEqual(manifest[-1]["stop_reason"], "OSError")


if __name__ == "__main__":
    unittest.main()
