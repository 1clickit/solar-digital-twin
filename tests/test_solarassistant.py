import io
import json
import os
import tempfile
import unittest
from argparse import Namespace
from contextlib import nullcontext, redirect_stdout
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

    def test_password_file_precedes_environment_and_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            password_file = Path(directory) / "password"
            password_file.write_bytes(b"file-value\r\n")
            with (
                patch.dict(os.environ, {"SOLARASSISTANT_PASSWORD": "environment-value"}),
                patch.object(solarassistant.getpass, "getpass") as prompt,
            ):
                self.assertEqual(
                    solarassistant.get_password(password_file),
                    "file-value",
                )
        prompt.assert_not_called()

    def test_password_file_strips_only_one_trailing_line_ending(self):
        with tempfile.TemporaryDirectory() as directory:
            password_file = Path(directory) / "password"
            password_file.write_bytes(b"value-with-space \n")
            self.assertEqual(
                solarassistant.get_password(password_file),
                "value-with-space ",
            )

    def test_environment_and_prompt_password_sources_remain_available(self):
        with (
            patch.dict(os.environ, {"SOLARASSISTANT_PASSWORD": "environment-value"}),
            patch.object(solarassistant.getpass, "getpass") as prompt,
        ):
            self.assertEqual(solarassistant.get_password(), "environment-value")
            prompt.assert_not_called()

        with (
            patch.dict(os.environ, {}, clear=True),
            patch.object(
                solarassistant.getpass,
                "getpass",
                return_value="prompt-value",
            ) as prompt,
        ):
            self.assertEqual(solarassistant.get_password(), "prompt-value")
            prompt.assert_called_once()

    def test_invalid_password_files_stop_before_collection_without_secret_output(self):
        cases = ("missing", "empty", "whitespace", "unreadable")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                password_file = Path(directory) / "password"
                if case == "empty":
                    password_file.write_text("", encoding="utf-8")
                elif case == "whitespace":
                    password_file.write_text("  \t\n", encoding="utf-8")

                args = Namespace(
                    duration=0,
                    interval=1.0,
                    password_file=password_file,
                    output_dir=Path(directory) / "evidence",
                )
                output = io.StringIO()
                read_patch = (
                    patch.object(Path, "read_bytes", side_effect=PermissionError)
                    if case == "unreadable"
                    else nullcontext()
                )
                with (
                    patch.object(solarassistant, "parse_args", return_value=args),
                    patch.object(solarassistant, "collect") as collect,
                    read_patch,
                    redirect_stdout(output),
                ):
                    with self.assertRaisesRegex(SystemExit, "1"):
                        solarassistant.main()

                collect.assert_not_called()
                self.assertIn("credential file could not be read", output.getvalue())
                self.assertNotIn("environment-value", output.getvalue())

    def test_selected_output_directory_preserves_file_relationship(self):
        response = FakeResponse(rows=[])
        session = FakeSession([response])
        clock = FakeClock()
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "external-evidence"
            with (
                patch.object(solarassistant.requests, "Session", return_value=session),
                patch.object(solarassistant.time, "monotonic", side_effect=clock.monotonic),
                patch.object(solarassistant.time, "sleep", side_effect=clock.sleep),
            ):
                raw, _ = solarassistant.collect(
                    1.0,
                    1.0,
                    "synthetic-secret",
                    output_dir=output_dir,
                )

            retained = solarassistant.retained_output_path(raw)
            self.assertEqual(raw.parent, output_dir)
            self.assertTrue(raw.exists())
            self.assertTrue(retained.exists())
            self.assertEqual(
                retained.name,
                f"{raw.stem}_retained{raw.suffix}",
            )
            self.assertTrue(response.closed)

    def test_output_directory_failure_stops_before_session_or_request(self):
        output_dir = Path("/synthetic/unavailable")
        with (
            patch.object(Path, "mkdir", side_effect=PermissionError),
            patch.object(solarassistant.requests, "Session") as session,
        ):
            with self.assertRaises(PermissionError):
                solarassistant.collect(
                    1.0,
                    1.0,
                    "synthetic-secret",
                    output_dir=output_dir,
                )
        session.assert_not_called()

    def test_default_output_directory_remains_compatible(self):
        path = solarassistant.new_output_path()
        self.assertEqual(path.parent, Path("evidence/solarassistant"))
        self.assertRegex(
            path.name,
            r"^solarassistant_\d{8}_\d{6}Z\.ndjson$",
        )

    def test_cli_passes_password_file_and_output_directory(self):
        args = Namespace(
            duration=12.0,
            interval=10.0,
            password_file=Path("/synthetic/password"),
            output_dir=Path("/synthetic/evidence"),
        )
        with (
            patch.object(solarassistant, "parse_args", return_value=args),
            patch.object(
                solarassistant,
                "get_password",
                return_value="synthetic-secret",
            ) as get_password,
            patch.object(
                solarassistant,
                "collect",
                return_value=(Path("/synthetic/evidence/raw.ndjson"), 0),
            ) as collect,
            redirect_stdout(io.StringIO()),
        ):
            solarassistant.main()

        get_password.assert_called_once_with(args.password_file)
        collect.assert_called_once_with(
            duration=12.0,
            interval=10.0,
            password="synthetic-secret",
            output_dir=args.output_dir,
        )


if __name__ == "__main__":
    unittest.main()
