import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import requests

from solar_digital_twin.collectors import solarassistant


class FakeClock:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def monotonic(self):
        return self.now

    def sleep(self, delay):
        self.sleeps.append(delay)
        self.now += delay


class FakeResponse:
    def __init__(self, status=200, rows=None, json_error=None):
        self.status_code = status
        self.rows = [] if rows is None else rows
        self.json_error = json_error
        self.closed = False

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("safe synthetic HTTP error")

    def json(self):
        if self.json_error is not None:
            raise self.json_error
        return self.rows

    def close(self):
        self.closed = True


class FakeSession:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.calls = []

    def get(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        outcome = next(self.outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class SolarAssistantCollectorTests(unittest.TestCase):
    def run_collect(self, session, output, clock, duration=1.0, password="synthetic-secret"):
        with (
            patch.object(solarassistant.requests, "Session", return_value=session),
            patch.object(solarassistant, "new_output_path", return_value=output),
            patch.object(solarassistant.time, "monotonic", side_effect=clock.monotonic),
            patch.object(solarassistant.time, "sleep", side_effect=clock.sleep),
            patch.object(solarassistant, "receipt_timestamp", return_value="2026-07-15T12:00:00.000Z"),
        ):
            return solarassistant.collect(duration, 1.0, password)

    def test_401_and_403_close_and_stop_without_retry_or_sleep(self):
        for status in (401, 403):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                response = FakeResponse(status=status)
                session = FakeSession([response])
                clock = FakeClock()
                output = Path(directory) / "solarassistant_test.ndjson"

                with self.assertRaises(solarassistant.AuthenticationRejected):
                    self.run_collect(session, output, clock, duration=0)

                self.assertEqual(len(session.calls), 1)
                self.assertEqual(clock.sleeps, [])
                self.assertTrue(response.closed)
                self.assertEqual(output.read_text(), "")

    def test_temporary_failures_retain_exponential_backoff(self):
        response = FakeResponse(rows=[])
        session = FakeSession([
            requests.ConnectionError("temporary"),
            requests.Timeout("temporary"),
            response,
        ])
        clock = FakeClock()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "solarassistant_test.ndjson"
            self.run_collect(session, output, clock, duration=3.1)

        self.assertEqual(clock.sleeps[:2], [1.0, 2.0])
        self.assertLessEqual(max(clock.sleeps), solarassistant.MAX_BACKOFF_SECONDS)
        self.assertEqual(len(session.calls), 3)
        self.assertTrue(response.closed)

    def test_success_preserves_raw_record_format_filtering_and_secret_exclusion(self):
        rows = [
            {
                "topic": "total/battery_voltage", "device": "Battery", "number": 1,
                "group": "Total", "name": "Voltage", "value": 52.1, "unit": "V",
            },
            {"topic": "unapproved/private", "value": "synthetic-secret"},
        ]
        response = FakeResponse(rows=rows)
        session = FakeSession([response])
        clock = FakeClock()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "solarassistant_test.ndjson"
            _, written = self.run_collect(session, output, clock)
            records = [json.loads(line) for line in output.read_text().splitlines()]
            retained = solarassistant.retained_output_path(output).read_text()

        self.assertTrue(response.closed)
        self.assertEqual(written, 1)
        self.assertEqual(records, [{
            "received_at_utc": "2026-07-15T12:00:00.000Z",
            "source_url": solarassistant.METRICS_URL,
            "topic": "total/battery_voltage",
            "device": "Battery",
            "number": 1,
            "group": "Total",
            "name": "Voltage",
            "value": 52.1,
            "unit": "V",
        }])
        self.assertNotIn("synthetic-secret", json.dumps(records))
        self.assertEqual(retained, "")

    def test_invalid_json_and_top_level_structure_close_response(self):
        cases = (
            FakeResponse(json_error=requests.JSONDecodeError("bad", "", 0)),
            FakeResponse(rows={"topic": "not-a-list"}),
        )
        for response in cases:
            with self.subTest(response=response), tempfile.TemporaryDirectory() as directory:
                session = FakeSession([response])
                clock = FakeClock()
                output = Path(directory) / "solarassistant_test.ndjson"
                self.run_collect(session, output, clock)
                self.assertTrue(response.closed)
                self.assertEqual(len(session.calls), 1)

    def test_processing_failure_still_closes_response(self):
        response = FakeResponse(rows=[{
            "topic": "total/battery_voltage", "value": object(),
        }])
        session = FakeSession([response])
        clock = FakeClock()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "solarassistant_test.ndjson"
            with self.assertRaises(TypeError):
                self.run_collect(session, output, clock)
        self.assertTrue(response.closed)

    def test_cli_authentication_failure_is_safe_and_non_success(self):
        output = io.StringIO()
        with (
            patch.object(solarassistant, "parse_args"),
            patch.object(solarassistant, "get_password", return_value="synthetic-secret"),
            patch.object(solarassistant, "collect", side_effect=solarassistant.AuthenticationRejected),
            redirect_stdout(output),
        ):
            with self.assertRaisesRegex(SystemExit, "1"):
                solarassistant.main()

        message = output.getvalue()
        self.assertIn("authentication failed", message)
        self.assertIn("correct the credential", message)
        self.assertNotIn("synthetic-secret", message)


if __name__ == "__main__":
    unittest.main()
