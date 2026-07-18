import argparse
import json
import subprocess
import unittest
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import coordinated_capture as capture


class CoordinatedCaptureTests(unittest.TestCase):
    def test_capture_identifier_uses_canonical_utc_shape(self):
        value = capture.datetime(2026, 7, 18, 12, 34, 56, tzinfo=capture.timezone.utc)
        self.assertEqual(
            capture.default_capture_id(value),
            "solar-forensic-20260718T123456Z",
        )

    def test_manifest_lifecycle_is_appended(self):
        output = StringIO()
        with patch.object(capture, "utc_text", return_value="2026-07-18T00:00:00.000Z"):
            capture.append_manifest(output, "capture_started", capture_id="test")
            capture.append_manifest(output, "capture_terminal", state="completion")

        records = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(
            [record["event"] for record in records],
            ["capture_started", "capture_terminal"],
        )
        self.assertEqual(records[0]["schema"], capture.CAPTURE_SCHEMA)

    def test_environment_loader_is_narrow_and_does_not_log_values(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "eg4.env"
            path.write_text(
                "EG4_USERNAME='synthetic-user'\n"
                "EG4_PASSWORD='synthetic password'\n"
                "UNRELATED=ignored\n"
            )
            values = capture.load_environment_file(path)

        self.assertEqual(
            values,
            {
                "EG4_USERNAME": "synthetic-user",
                "EG4_PASSWORD": "synthetic password",
            },
        )

    def test_restore_starts_only_units_previously_active(self):
        prior = [
            {"unit": "eg4-refresh-report.timer", "active": "active"},
            {"unit": "eg4-refresh-report.service", "active": "inactive"},
        ]
        manifest = StringIO()
        completed = subprocess.CompletedProcess([], 0, b"", b"")
        with patch.object(capture.subprocess, "run", return_value=completed) as run:
            self.assertTrue(capture.restore_units(prior, manifest))

        run.assert_called_once_with(
            ["systemctl", "start", "eg4-refresh-report.timer"],
            check=False,
            capture_output=True,
        )

    def test_rehearsal_is_bounded_independent_and_exclusive(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            args = argparse.Namespace(
                capture_id="solar-forensic-20260718T123456Z",
                output_dir=root,
                duration=0.1,
            )
            self.assertEqual(capture.run_rehearsal(args), 0)
            run_dir = root / args.capture_id
            for source in ("esp32", "eg4", "solarassistant"):
                self.assertTrue((run_dir / source / "synthetic.ndjson").exists())
            records = [
                json.loads(line)
                for line in (run_dir / "coordinated_manifest.ndjson")
                .read_text()
                .splitlines()
            ]
            self.assertEqual(records[0]["event"], "capture_started")
            self.assertEqual(records[-1]["event"], "capture_terminal")
            self.assertEqual(records[-1]["state"], "completion")
            with self.assertRaises(FileExistsError):
                capture.run_rehearsal(args)

    def test_artifact_readiness_requires_each_independent_source(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            paths = {}
            for source in ("esp32", "eg4", "solarassistant"):
                paths[source] = root / source
                paths[source].mkdir()
            for name in (
                "esp32_sse_x.ndjson",
                "esp32_sse_x_retained.ndjson",
                "esp32_sse_x_retained_esp32-conservative-v1.ndjson",
                "esp32_sse_x_manifest.ndjson",
            ):
                (paths["esp32"] / name).write_text("{}\n")
            (paths["solarassistant"] / "solarassistant_x.ndjson").write_text("{}\n")
            (paths["solarassistant"] / "solarassistant_x_retained.ndjson").write_text("{}\n")
            (paths["eg4"] / "eg4_capture.sqlite").write_bytes(b"synthetic")
            evidence = paths["eg4"] / "evidence" / "run"
            evidence.mkdir(parents=True)
            (evidence / "runtime.json").write_text("{}")

            self.assertEqual(
                capture.artifacts_ready(paths),
                {"esp32": True, "solarassistant": True, "eg4": True},
            )


if __name__ == "__main__":
    unittest.main()
