import csv
import contextlib
import hashlib
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_coordinated_capture as runner


class CoordinatedAnalysisRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.evidence = self.root / "capture"
        self.evidence.mkdir()
        (self.evidence / "eg4").mkdir()
        (self.evidence / "esp32").mkdir()
        (self.evidence / "solarassistant").mkdir()
        self.eg4 = self.evidence / runner.INPUT_ARGUMENTS["eg4"]
        self.raw = self.evidence / runner.INPUT_ARGUMENTS["esp32_raw"]
        self.current = self.evidence / runner.INPUT_ARGUMENTS["esp32_current"]
        self.conservative = self.evidence / runner.INPUT_ARGUMENTS["esp32_conservative"]
        self.solar = self.evidence / runner.INPUT_ARGUMENTS["solarassistant_raw"]
        self.solar_retained = self.evidence / runner.INPUT_ARGUMENTS["solarassistant_retained"]
        self.inventory = self.root / "inventory.tsv"
        self._database()
        self._streams()
        self._write_inventory()

    def tearDown(self):
        self.temporary.cleanup()

    def _database(self):
        connection = sqlite3.connect(self.eg4)
        connection.executescript(
            """
            CREATE TABLE day_multiline_samples (
                serial_num TEXT, sample_time TEXT, solar_pv_w REAL,
                grid_power_w REAL, battery_discharging_w REAL,
                consumption_w REAL, soc REAL, ac_couple_power_w REAL,
                raw_json TEXT
            );
            CREATE TABLE runtime_snapshots (
                serial_num TEXT, server_time TEXT, device_time TEXT,
                fw_code TEXT, status_text TEXT, soc REAL, v_bat REAL,
                grid_freq_hz REAL, eps_freq_hz REAL,
                consumption_power_w REAL, ac_couple_power_w REAL,
                radiator1_c REAL, radiator2_c REAL, raw_json TEXT,
                captured_at TEXT
            );
            """
        )
        rows = [
            ("2026-02-03 06:00:00", 0),
            ("2026-02-03 06:04:00", 0),
            ("2026-02-03 06:08:00", 0),
            ("2026-02-03 08:00:00", 3000),
            ("2026-02-03 08:04:00", 3010),
            ("2026-02-03 08:08:00", 2995),
            ("2026-02-03 09:00:00", 4000),
            ("2026-02-03 09:04:00", 1000),
            ("2026-02-03 09:08:00", 1100),
            ("2026-02-03 09:12:00", 3900),
            ("2026-02-03 10:00:00", 2000),
            ("2026-02-03 10:04:00", 1800),
            ("2026-02-03 10:08:00", 1600),
        ]
        connection.executemany(
            "INSERT INTO day_multiline_samples VALUES (?,?,?,?,?,?,?,?,?)",
            [
                ("redacted", stamp, power, 0, 0, 900, 70, power, "{}")
                for stamp, power in rows
            ],
        )
        for hour in range(12, 17):
            connection.execute(
                "INSERT INTO runtime_snapshots VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "redacted",
                    f"2026-02-03 {hour:02d}:00:00",
                    "2026-02-03 06:00:00",
                    "test",
                    "normal",
                    70,
                    52.0,
                    60.0,
                    60.0,
                    900,
                    2000,
                    20,
                    20,
                    json.dumps({"warningCode": 0, "faultCode": 0, "workMode": "normal"}),
                    "2026-02-03 06:00:01",
                ),
            )
        connection.commit()
        connection.close()

    def _streams(self):
        esp_rows = []
        for minute in range(0, 241):
            stamp = f"2026-02-03T12:{minute:02d}:00.000Z" if minute < 60 else None
            if stamp is None:
                hour = 12 + minute // 60
                stamp = f"2026-02-03T{hour:02d}:{minute % 60:02d}:00.000Z"
            for entity, value in (
                ("sensor-01_gen_frequency", 60.0),
                ("sensor-01_estimated_gen_l1-l2_voltage", 240.0),
                ("sensor-01_estimated_total_ac-coupled_power", 2000.0),
                ("sensor-01_estimated_active_microinverters", 8.0),
            ):
                esp_rows.append(
                    {"received_at_utc": stamp, "id": entity, "value": value, "state": str(value)}
                )
        encoded = "".join(json.dumps(row, separators=(",", ":")) + "\n" for row in esp_rows)
        for path in (self.raw, self.current, self.conservative):
            path.write_text(encoded, encoding="utf-8")
        solar_rows = []
        for minute in range(0, 241):
            hour = 12 + minute // 60
            stamp = f"2026-02-03T{hour:02d}:{minute % 60:02d}:00.000Z"
            for topic, value, unit in (
                ("total/battery_state_of_charge", 70, "%"),
                ("total/battery_voltage", 52.0, "V"),
                ("total/battery_current", -5.0, "A"),
                ("total/battery_power", -260.0, "W"),
                ("battery_1/state_of_charge", 71, "%"),
                ("battery_2/state_of_charge", 69, "%"),
            ):
                solar_rows.append({"received_at_utc": stamp, "topic": topic, "value": value, "unit": unit})
        encoded_solar = "".join(json.dumps(row, separators=(",", ":")) + "\n" for row in solar_rows)
        self.solar.write_text(encoded_solar, encoding="utf-8")
        self.solar_retained.write_text(encoded_solar, encoding="utf-8")

    def _write_inventory(self):
        paths = (self.eg4, self.raw, self.current, self.conservative, self.solar, self.solar_retained)
        with self.inventory.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerow(("path", "bytes", "mtime_ns", "sha256"))
            for path in paths:
                stat = path.stat()
                writer.writerow(
                    (
                        str(path.relative_to(self.evidence)),
                        stat.st_size,
                        stat.st_mtime_ns,
                        hashlib.sha256(path.read_bytes()).hexdigest(),
                    )
                )

    def _args(self, suffix="one"):
        return runner.parse_args(
            [
                "--evidence-root", str(self.evidence),
                "--inventory", str(self.inventory),
                "--eg4", str(self.eg4),
                "--esp32-raw", str(self.raw),
                "--esp32-current", str(self.current),
                "--esp32-conservative", str(self.conservative),
                "--solarassistant-raw", str(self.solar),
                "--solarassistant-retained", str(self.solar_retained),
                "--start-utc", "2026-02-03T12:00:00Z",
                "--end-utc", "2026-02-03T16:00:00Z",
                "--analysis-commit", "synthetic",
                "--json-output", str(self.root / f"{suffix}.json"),
                "--tsv-output", str(self.root / f"{suffix}.tsv"),
                "--svg-output", str(self.root / f"{suffix}.svg"),
            ]
        )

    def test_real_runner_is_deterministic_bounded_and_preserves_classification(self):
        first = runner.run(self._args("first"))
        second = runner.run(self._args("second"))
        self.assertEqual(first, second)
        self.assertEqual(first["candidate_count"], 1)
        self.assertEqual(first["selected_event_count"], 1)
        self.assertEqual(first["control_count"], 3)
        event = first["contexts"][0]
        self.assertEqual(event["primary_event"]["event_type"], "partial_collapse")
        self.assertTrue(all(item["preservation"] == "preserved" for item in event["streams"].values()))
        self.assertLess(event["streams"]["esp32_raw"]["summary"]["records"], 4 * 241)
        self.assertNotIn("serial_num", (self.root / "first.json").read_text())
        self.assertEqual((self.root / "first.json").read_bytes(), (self.root / "second.json").read_bytes())
        self.assertEqual((self.root / "first.tsv").read_bytes(), (self.root / "second.tsv").read_bytes())
        self.assertEqual((self.root / "first.svg").read_bytes(), (self.root / "second.svg").read_bytes())
        svg = (self.root / "first.svg").read_text(encoding="utf-8")
        self.assertIn("Coordinated capture correlation overview", svg)
        self.assertIn("event-01", svg)
        self.assertIn("control-strong", svg)
        with (self.root / "first.tsv").open(newline="", encoding="utf-8") as handle:
            row = next(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual(row["eg4_load_before_w"], "900.0")
        self.assertEqual(row["esp32_estimated_power_w"], "2000.000..2000.000")
        self.assertEqual(row["battery_flow_transition"], "discharging")

    def test_identity_mismatch_stops_without_payload_disclosure(self):
        self.raw.write_text(self.raw.read_text() + "{}\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "identity does not match") as caught:
            runner.run(self._args())
        self.assertNotIn("received_at_utc", str(caught.exception))

    def test_output_beneath_evidence_is_refused(self):
        arguments = self._args()
        with self.assertRaisesRegex(ValueError, "must not be beneath"):
            runner.refuse_evidence_output(self.evidence / "derived.json", self.evidence)
        self.assertFalse(arguments.json_output.is_relative_to(self.evidence))

    def test_all_explicit_paths_are_required(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            runner.parse_args([])

    def test_readonly_sqlite_connection_remains_query_only(self):
        from solar_digital_twin.analysis.correlation_adapters import _readonly_connection

        connection = _readonly_connection(self.eg4)
        try:
            self.assertEqual(connection.execute("PRAGMA query_only").fetchone()[0], 1)
            with self.assertRaises(sqlite3.OperationalError):
                connection.execute("CREATE TABLE forbidden(value TEXT)")
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
