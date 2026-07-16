import json
import os
import signal
import subprocess
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch

from solar_digital_twin.reporting import solarassistant_monitor as monitor


BASE_TIME = datetime(2026, 7, 16, 12, 0, tzinfo=timezone.utc)


class FakeTime:
    def __init__(self, now=BASE_TIME):
        self.now = now
        self.monotonic_now = 0.0

    def clock(self):
        return self.now

    def monotonic(self):
        return self.monotonic_now


def record(timestamp, topic, value, unit="V", name="Synthetic <metric>"):
    return {
        "received_at_utc": timestamp,
        "source_url": "http://synthetic.invalid/api",
        "topic": topic,
        "device": "Synthetic battery",
        "number": 1,
        "group": "Synthetic",
        "name": name,
        "value": value,
        "unit": unit,
    }


def line(value):
    return (json.dumps(value, separators=(",", ":")) + "\n").encode()


class StateFixture(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.directory = Path(self.tempdir.name)
        self.raw = self.directory / "solarassistant_20260716_120000Z.ndjson"
        self.raw.write_bytes(b"")
        self.fake = FakeTime()
        self.state = monitor.MonitorState(
            self.directory, self.raw, 86_400, 30,
            clock=self.fake.clock, monotonic=self.fake.monotonic,
        )

    def add(self, timestamp, topic, value, unit="V"):
        self.state.ingest_complete_line(line(record(timestamp, topic, value, unit)))


class SelectionTests(unittest.TestCase):
    def test_safe_cli_defaults(self):
        args = monitor.parse_args([])
        self.assertEqual(args.bind, "127.0.0.1")
        self.assertEqual(args.port, 8792)
        self.assertEqual(args.capture_duration, 86_400)
        self.assertEqual(args.freshness_seconds, 30)

    def test_newest_raw_non_retained_file_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old = root / "solarassistant_20260716_100000Z.ndjson"
            newest = root / "solarassistant_20260716_110000Z.ndjson"
            retained = root / "solarassistant_20260716_120000Z_retained.ndjson"
            for index, path in enumerate((old, newest, retained), start=1):
                path.write_text("{}\n", encoding="utf-8")
                os.utime(path, ns=(index, index))
            self.assertEqual(monitor.newest_raw_file(root), newest)

    def test_explicit_raw_file_must_be_raw_and_inside_directory(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            raw = root / "solarassistant_test.ndjson"
            retained = root / "solarassistant_test_retained.ndjson"
            external = Path(outside) / "solarassistant_external.ndjson"
            for path in (raw, retained, external):
                path.write_text("", encoding="utf-8")
            self.assertEqual(monitor.validate_raw_file(root, raw), raw.resolve())
            with self.assertRaisesRegex(ValueError, "retained"):
                monitor.validate_raw_file(root, retained)
            with self.assertRaisesRegex(ValueError, "inside"):
                monitor.validate_raw_file(root, external)

    def test_no_file_is_nonfatal(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertIsNone(monitor.newest_raw_file(Path(directory)))


class EvidenceStateTests(StateFixture):
    def test_bootstrap_counts_records_polls_ranges_groups_and_preserves_file(self):
        t1 = "2026-07-16T12:00:00.000Z"
        t2 = "2026-07-16T12:00:10.000Z"
        content = b"".join((
            line(record(t1, "total/battery_voltage", 52.1)),
            line(record(t1, "battery_1/state_of_charge", 79, "%")),
            line(record(t1, "battery_2/state_of_charge", 77, "%")),
            line(record(t2, "total/battery_voltage", 53.2)),
        ))
        self.raw.write_bytes(content)
        before = self.raw.stat()
        offset = self.state.bootstrap()
        after = self.raw.stat()
        status = self.state.status_dict()
        self.assertEqual(offset, len(content))
        self.assertEqual(status["raw_record_count"], 4)
        self.assertEqual(status["poll_count"], 2)
        self.assertEqual(status["groups"]["Combined"]["voltage"]["value"], 53.2)
        self.assertNotIn("state_of_charge", status["groups"]["Battery 1"])
        self.assertEqual(status["numeric_ranges"]["total/battery_voltage"], {"minimum": "52.1", "maximum": "53.2"})
        self.assertEqual(self.raw.read_bytes(), content)
        self.assertEqual((before.st_size, before.st_mtime_ns), (after.st_size, after.st_mtime_ns))

    def test_new_append_updates_without_rereading_existing_records(self):
        first = line(record("2026-07-16T12:00:00.000Z", "total/battery_voltage", 52))
        self.raw.write_bytes(first)
        tailer = monitor.EvidenceTailer(self.state, threading.Event())
        tailer.offset = self.state.bootstrap()
        with self.raw.open("ab") as handle:
            handle.write(line(record("2026-07-16T12:00:10.000Z", "total/battery_voltage", 53)))
        tailer._read_growth()
        self.state.flush_pending(force=True)
        self.assertEqual(self.state.raw_record_count, 2)
        self.assertEqual(self.state.latest_snapshot["total/battery_voltage"]["value"], 53)

    def test_partial_line_waits_and_malformed_complete_line_counts_once(self):
        complete = line(record("2026-07-16T12:00:00.000Z", "total/battery_voltage", 52))
        partial = json.dumps(record("2026-07-16T12:00:10.000Z", "total/battery_voltage", 53)).encode()
        self.raw.write_bytes(complete + partial)
        tailer = monitor.EvidenceTailer(self.state, threading.Event())
        tailer.offset = self.state.bootstrap()
        self.assertEqual(self.state.invalid_record_count, 0)
        self.assertEqual(self.state.raw_record_count, 1)
        with self.raw.open("ab") as handle:
            handle.write(b"\nnot-json\n")
        tailer._read_growth()
        self.state.flush_pending(force=True)
        self.assertEqual(self.state.raw_record_count, 2)
        self.assertEqual(self.state.invalid_record_count, 1)

    def test_snapshot_updates_atomically_on_next_timestamp(self):
        t1, t2, t3 = (f"2026-07-16T12:00:{second:02d}.000Z" for second in (0, 10, 20))
        self.add(t1, "total/battery_voltage", 51)
        self.state.flush_pending(force=True)
        self.add(t2, "total/battery_voltage", 52)
        self.add(t2, "battery_1/voltage", 52.1)
        self.assertEqual(self.state.latest_snapshot["total/battery_voltage"]["value"], 51)
        self.add(t3, "total/battery_voltage", 53)
        self.assertEqual(self.state.latest_snapshot["total/battery_voltage"]["value"], 52)
        self.assertEqual(self.state.latest_snapshot["battery_1/voltage"]["value"], 52.1)
        self.assertTrue(self.state.status_dict()["assembling_newer_poll"])

    def test_quiet_delay_completes_pending_snapshot(self):
        self.add("2026-07-16T12:00:00.000Z", "total/battery_voltage", 52)
        self.fake.monotonic_now = monitor.SNAPSHOT_COMPLETION_DELAY - 0.01
        self.assertFalse(self.state.flush_pending())
        self.fake.monotonic_now += 0.02
        self.assertTrue(self.state.flush_pending())
        self.assertEqual(self.state.poll_count, 1)

    def test_missing_topics_are_absent_not_zero(self):
        self.add("2026-07-16T12:00:00.000Z", "battery_1/voltage", 0)
        self.state.flush_pending(force=True)
        grouped = self.state.status_dict()["groups"]
        self.assertEqual(grouped["Battery 1"]["voltage"]["value"], 0)
        self.assertNotIn("current", grouped["Battery 1"])
        self.assertEqual(grouped["Battery 2"], {})

    def test_retained_count_bootstraps_and_tails(self):
        retained = monitor.retained_sibling(self.raw)
        retained.write_bytes(b"{}\n{}\npartial")
        self.state.bootstrap_retained()
        self.assertEqual(self.state.retained_record_count, 2)
        with retained.open("ab") as handle:
            handle.write(b"-complete\n{}\n")
        self.state.update_retained_count()
        self.assertEqual(self.state.retained_record_count, 4)


class CountdownTests(StateFixture):
    def test_countdown_progress_and_zero_floor(self):
        self.add(BASE_TIME.isoformat(), "total/battery_voltage", 52)
        self.state.flush_pending(force=True)
        self.fake.now = BASE_TIME + timedelta(hours=1)
        value = self.state.countdown()
        self.assertEqual(value["elapsed"], "01:00:00")
        self.assertEqual(value["remaining"], "23:00:00")
        self.fake.now = BASE_TIME + timedelta(days=2)
        value = self.state.countdown()
        self.assertEqual(value["remaining"], "00:00:00")
        self.assertEqual(value["progress_percent"], 100)

    def test_early_stop_and_fresh_stale_status(self):
        self.add(BASE_TIME.isoformat(), "total/battery_voltage", 52)
        self.state.flush_pending(force=True)
        self.state.collector_identity = monitor.ProcessIdentity(10, os.getuid(), "1", ("python",))
        self.assertEqual(self.state.status_dict()["capture_status"], "Fresh")
        self.fake.now = BASE_TIME + timedelta(seconds=31)
        self.assertEqual(self.state.status_dict()["capture_status"], "Stale")
        self.state.collector_identity = None
        self.state.collector_seen = True
        self.state.stop_requested_at = BASE_TIME
        result = self.state.status_dict()
        self.assertEqual(result["capture_status"], "Stopped")
        self.assertTrue(result["countdown"]["stopped_early"])


class AbortSafetyTests(StateFixture):
    def matching_identity(self, pid=321, start="900"):
        command = ("python", "-m", monitor.COLLECTOR_MODULE, "--output-dir", str(self.directory))
        return monitor.ProcessIdentity(pid, os.getuid(), start, command)

    def write_fake_process(self, proc_root, pid, start="900"):
        process = proc_root / str(pid)
        process.mkdir()
        command = self.matching_identity(pid, start).command
        process.joinpath("cmdline").write_bytes(b"\0".join(part.encode() for part in command) + b"\0")
        fields_after_comm = ["S"] + ["0"] * 18 + [start]
        process.joinpath("stat").write_text(
            f"{pid} (synthetic collector) " + " ".join(fields_after_comm),
            encoding="utf-8",
        )

    def test_missing_or_ambiguous_discovery_disables_abort(self):
        controller = monitor.AbortController(self.state)
        with patch.object(monitor, "discover_collector", return_value=(None, "ambiguous")):
            controller.refresh()
        self.assertFalse(self.state.status_dict()["abort_enabled"])
        self.assertEqual(controller.abort()[0], False)

    def test_command_match_requires_module_directory_same_uid_and_not_self(self):
        identity = self.matching_identity()
        self.assertTrue(monitor.command_matches(identity, self.directory, own_pid=999))
        self.assertFalse(monitor.command_matches(identity, self.directory / "other", own_pid=999))
        self.assertFalse(monitor.command_matches(identity, self.directory, own_pid=identity.pid))

    def test_proc_discovery_requires_exactly_one_match_and_records_start_identity(self):
        proc_root = self.directory / "proc"
        proc_root.mkdir()
        self.write_fake_process(proc_root, 321, "900")
        found, _ = monitor.discover_collector(self.directory, proc_root=proc_root, own_pid=999)
        self.assertEqual((found.pid, found.start_ticks), (321, "900"))
        self.write_fake_process(proc_root, 322, "901")
        found, reason = monitor.discover_collector(self.directory, proc_root=proc_root, own_pid=999)
        self.assertIsNone(found)
        self.assertIn("More than one", reason)

    def test_pid_reuse_or_identity_mismatch_prevents_signal(self):
        expected = self.matching_identity()
        self.state.collector_identity = expected
        kill = Mock()
        controller = monitor.AbortController(self.state, kill=kill)
        replacement = self.matching_identity(start="901")
        with patch.object(monitor, "inspect_process", return_value=replacement):
            accepted, _ = controller.abort()
        self.assertFalse(accepted)
        kill.assert_not_called()

    def test_valid_abort_sends_exactly_one_sigterm_and_no_shell(self):
        expected = self.matching_identity()
        self.state.collector_identity = expected
        kill = Mock()
        controller = monitor.AbortController(self.state, kill=kill)
        with patch.object(monitor, "inspect_process", return_value=expected), patch("subprocess.run") as run:
            accepted, _ = controller.abort()
        self.assertTrue(accepted)
        kill.assert_called_once_with(expected.pid, signal.SIGTERM)
        run.assert_not_called()
        self.assertTrue(self.state.stopping)


class HttpTests(StateFixture):
    def setUp(self):
        super().setUp()
        self.add(BASE_TIME.isoformat(), "total/battery_voltage", '<secret>&"', "V")
        self.state.flush_pending(force=True)
        self.abort = Mock()
        self.abort.abort.return_value = (True, "accepted")
        app = monitor.MonitorApplication(self.state, self.abort, control_token="test-control-token")
        self.server = monitor.ThreadingHTTPServer(("127.0.0.1", 0), app.handler_class())
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def request(self, path, method="GET", headers=None):
        request = urllib.request.Request(self.base + path, method=method, headers=headers or {})
        try:
            response = urllib.request.urlopen(request, timeout=2)
        except urllib.error.HTTPError as exc:
            response = exc
        return response.status, dict(response.headers), response.read()

    def test_status_is_sanitized_and_security_headers_present(self):
        status, headers, body = self.request("/api/status")
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertEqual(data["control_token"], "test-control-token")
        self.assertNotIn("source_url", body.decode())
        self.assertNotIn("password", body.decode().lower())
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertIn("default-src 'none'", headers["Content-Security-Policy"])

    def test_report_is_escaped_and_does_not_modify_evidence(self):
        before = (self.raw.read_bytes(), self.raw.stat().st_mtime_ns)
        status, _, body = self.request("/report")
        after = (self.raw.read_bytes(), self.raw.stat().st_mtime_ns)
        text = body.decode()
        self.assertEqual(status, 200)
        self.assertIn("&lt;secret&gt;&amp;&quot;", text)
        self.assertNotIn('<secret>&"', text)
        self.assertEqual(before, after)

    def test_get_missing_invalid_token_and_wrong_origin_cannot_abort(self):
        self.assertEqual(self.request("/api/abort")[0], 405)
        self.assertEqual(self.request("/api/abort", "POST")[0], 403)
        headers = {"Origin": self.base, "X-Control-Token": "wrong"}
        self.assertEqual(self.request("/api/abort", "POST", headers)[0], 403)
        self.abort.abort.assert_not_called()

    def test_valid_same_origin_abort_is_accepted(self):
        headers = {"Origin": self.base, "X-Control-Token": "test-control-token"}
        status, _, body = self.request("/api/abort", "POST", headers)
        self.assertEqual(status, 202)
        self.assertTrue(json.loads(body)["accepted"])
        self.abort.abort.assert_called_once()

    def test_unknown_paths_are_not_file_served(self):
        self.assertEqual(self.request("/etc/passwd")[0], 404)


class LauncherTests(unittest.TestCase):
    def test_nonprivileged_check_passes_without_runtime_inputs(self):
        result = subprocess.run(
            ["bash", "scripts/run_solarassistant_monitor.sh", "--check"],
            cwd=Path(__file__).resolve().parents[1], text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("no root, credential, evidence, collector, device, service, or network action", result.stdout)

    def test_launcher_refuses_password_like_arguments_before_operation(self):
        result = subprocess.run(
            ["bash", "scripts/run_solarassistant_monitor.sh", "--password-file", "synthetic"],
            cwd=Path(__file__).resolve().parents[1], text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("credential-like", result.stdout)


if __name__ == "__main__":
    unittest.main()
