import hashlib
import json
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from solar_digital_twin.analysis.correlation_adapters import (
    APPROVED_ESP32_IDS,
    AdapterError,
    _readonly_connection,
    iter_eg4_day_records,
    iter_eg4_runtime_records,
    iter_esp32_records,
    iter_solarassistant_records,
)
from solar_digital_twin.analysis.forensic_correlation import analyze_correlation
from solar_digital_twin.collectors.esp32_sse import APPROVED_IDS


UTC = timezone.utc
START = datetime(2026, 2, 3, 18, 0, tzinfo=UTC)
END = START + timedelta(minutes=10)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CorrelationAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.database = self.root / "synthetic.sqlite"
        self.solar = self.root / "synthetic_solar.ndjson"
        self.esp = self.root / "synthetic_esp.ndjson"
        self._create_database()

    def tearDown(self):
        self.temporary.cleanup()

    def _create_database(self):
        connection = sqlite3.connect(self.database)
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
            ("unit-a", "2026-02-03 12:00:00", 600, 0, 100, 700, 50, 3200, "{}"),
            ("unit-a", "2026-02-03 12:01:00", 610, 0, 120, 720, 49, 900, "{}"),
            ("unit-a", "2026-02-03 12:02:00", 620, 0, 110, 710, 49, 950, "{}"),
            ("unit-a", "2026-02-03 12:03:00", 630, 0, 90, 690, 48, 3100, "{}"),
            ("unit-a", "2026-02-03 13:00:00", 0, 0, 0, 0, 48, 0, "{}"),
        ]
        connection.executemany(
            "INSERT INTO day_multiline_samples VALUES (?,?,?,?,?,?,?,?,?)", rows
        )
        connection.execute(
            "INSERT INTO runtime_snapshots VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                "unit-a",
                "2026-02-03 18:01:00",
                "2026-02-03 12:01:00",
                "synthetic",
                "normal",
                49,
                51.2,
                60.0,
                60.0,
                720,
                900,
                20,
                21,
                json.dumps({"warningCode": 0, "faultCode": 0, "workMode": "normal"}),
                "2026-02-03 12:01:05",
            ),
        )
        connection.commit()
        connection.close()

    def _write_ndjson(self, path, rows):
        path.write_text(
            "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
        )

    def _solar_rows(self):
        timestamp = "2026-02-03T18:01:00.000Z"
        return [
            {
                "received_at_utc": timestamp,
                "topic": "total/battery_state_of_charge",
                "value": 55,
                "unit": "%",
            },
            {
                "received_at_utc": timestamp,
                "topic": "battery_1/state_of_charge",
                "value": 56,
                "unit": "%",
            },
            {
                "received_at_utc": timestamp,
                "topic": "battery_2/state_of_charge",
                "value": 54,
                "unit": "%",
            },
            {
                "received_at_utc": timestamp,
                "topic": "total/battery_voltage",
                "value": 51.4,
                "unit": "V",
            },
        ]

    def _esp_rows(self):
        return [
            {
                "received_at_utc": "2026-02-03T18:00:59.000Z",
                "id": "sensor-01_gen_frequency",
                "name": "Frequency",
                "domain": "sensor",
                "value": 60.0,
                "state": "60.0",
            },
            {
                "received_at_utc": "2026-02-03T18:01:00.000Z",
                "id": "binary_sensor-03_large_power_drop_active",
                "name": "Drop",
                "domain": "binary_sensor",
                "value": "ON",
                "state": "ON",
            },
            {
                "received_at_utc": "2026-02-03T18:01:01.000Z",
                "id": "sensor-01_gen_frequency",
                "name": "Frequency",
                "domain": "sensor",
                "value": 60.06,
                "state": "60.06",
            },
        ]

    def test_valid_eg4_rows_and_bounded_query(self):
        records = list(iter_eg4_day_records(self.database, START, END, batch_size=2))
        self.assertEqual(len(records), 4)
        self.assertEqual(records[0].values["ac_couple_power_w"], 3200)
        self.assertEqual(records[0].values["estimated_soc_percent"], 50)
        self.assertEqual(records[0].timestamp_utc, START)
        self.assertEqual(records[0].timestamp_kind, "cloud_source_time")
        self.assertEqual(records[0].provenance["table"], "day_multiline_samples")

    def test_eg4_database_is_opened_read_only(self):
        connection = _readonly_connection(self.database)
        try:
            with self.assertRaises(sqlite3.OperationalError):
                connection.execute("CREATE TABLE forbidden (value TEXT)")
        finally:
            connection.close()

    def test_missing_eg4_table_or_field_fails_clearly(self):
        missing = self.root / "missing.sqlite"
        sqlite3.connect(missing).close()
        with self.assertRaisesRegex(AdapterError, "missing required fields"):
            list(iter_eg4_day_records(missing, START, END))
        connection = sqlite3.connect(self.root / "partial.sqlite")
        connection.execute("CREATE TABLE day_multiline_samples (sample_time TEXT)")
        connection.close()
        with self.assertRaisesRegex(AdapterError, "ac_couple_power_w"):
            list(iter_eg4_day_records(self.root / "partial.sqlite", START, END))

    def test_runtime_context_preserves_selected_fields_and_provenance(self):
        record = next(iter_eg4_runtime_records(self.database, START, END))
        self.assertEqual(record.values["operating_state"], "normal")
        self.assertEqual(record.values["warning"], 0)
        self.assertEqual(record.values["fault"], 0)
        self.assertEqual(record.values["grid_frequency_hz"], 60.0)
        self.assertEqual(record.timestamp_utc, START + timedelta(minutes=1))
        self.assertEqual(record.original_timestamp, "2026-02-03 18:01:00")
        self.assertEqual(record.provenance["table"], "runtime_snapshots")

    def test_valid_solarassistant_poll_groups_scopes_and_trusted_soc(self):
        self._write_ndjson(self.solar, self._solar_rows())
        records = list(iter_solarassistant_records(self.solar, START, END))
        self.assertEqual(len(records), 1)
        values = records[0].values
        self.assertEqual(values["trusted_soc_percent"], 55)
        self.assertEqual(values["battery_1_state_of_charge"], 56)
        self.assertEqual(values["battery_2_state_of_charge"], 54)
        self.assertEqual(values["metrics"]["total/battery_voltage"]["unit"], "V")

    def test_malformed_solarassistant_line_is_payload_free(self):
        self.solar.write_text("not-secret-but-malformed\n", encoding="utf-8")
        with self.assertRaises(AdapterError) as caught:
            list(iter_solarassistant_records(self.solar, START, END))
        self.assertEqual(str(caught.exception), "SolarAssistant line 1: malformed JSON")
        self.assertNotIn("not-secret", str(caught.exception))

    def test_valid_esp32_raw_and_retained_records(self):
        self._write_ndjson(self.esp, self._esp_rows())
        raw = list(iter_esp32_records(self.esp, START, END, stream_kind="raw"))
        retained = list(
            iter_esp32_records(self.esp, START, END, stream_kind="retained")
        )
        self.assertEqual(raw[0].values["frequency_hz"], 60.0)
        self.assertEqual(retained[0].provenance["stream_kind"], "retained")
        self.assertEqual(raw[0].timestamp_kind, "solardt_receipt_time")

    def test_adapter_allowlist_matches_collector_allowlist(self):
        self.assertEqual(APPROVED_ESP32_IDS, frozenset(APPROVED_IDS))

    def test_esp32_availability_transition_is_preserved(self):
        rows = self._esp_rows()
        rows[0]["available"] = True
        rows[2]["available"] = False
        self._write_ndjson(self.esp, rows)
        records = list(iter_esp32_records(self.esp, START, END, stream_kind="raw"))
        self.assertEqual(
            [records[0].values["available"], records[2].values["available"]],
            [True, False],
        )

    def test_malformed_or_unapproved_esp32_record_fails_safely(self):
        self.esp.write_text("{bad\n", encoding="utf-8")
        with self.assertRaisesRegex(AdapterError, "ESP32 line 1: malformed JSON"):
            list(iter_esp32_records(self.esp, START, END, stream_kind="raw"))
        self._write_ndjson(
            self.esp,
            [
                {
                    "received_at_utc": "2026-02-03T18:00:00.000Z",
                    "id": "sensor-unapproved",
                    "value": 1,
                }
            ],
        )
        with self.assertRaisesRegex(AdapterError, "entity id is not approved"):
            list(iter_esp32_records(self.esp, START, END, stream_kind="raw"))

    def test_receipt_timestamp_must_be_canonical_utc(self):
        row = self._solar_rows()[0]
        row["received_at_utc"] = "2026-02-03T12:01:00"
        self._write_ndjson(self.solar, [row])
        with self.assertRaisesRegex(AdapterError, "canonical UTC"):
            list(iter_solarassistant_records(self.solar, START, END))

    def test_naive_bounds_are_rejected(self):
        naive = datetime(2026, 2, 3, 18, 0)
        with self.assertRaisesRegex(AdapterError, "explicit timezone"):
            list(iter_eg4_day_records(self.database, naive, END))

    def test_inputs_remain_unchanged(self):
        self._write_ndjson(self.solar, self._solar_rows())
        self._write_ndjson(self.esp, self._esp_rows())
        before = {path: digest(path) for path in (self.database, self.solar, self.esp)}
        list(iter_eg4_day_records(self.database, START, END))
        list(iter_solarassistant_records(self.solar, START, END))
        list(iter_esp32_records(self.esp, START, END, stream_kind="raw"))
        self.assertEqual(before, {path: digest(path) for path in before})

    def test_ndjson_processing_is_lazy_and_line_oriented(self):
        rows = self._esp_rows()[:1]
        self.esp.write_text(json.dumps(rows[0]) + "\n{bad\n", encoding="utf-8")
        iterator = iter_esp32_records(self.esp, START, END, stream_kind="raw")
        self.assertEqual(next(iterator).values["frequency_hz"], 60.0)
        with self.assertRaisesRegex(AdapterError, "line 2"):
            next(iterator)

    def test_missing_and_out_of_window_records(self):
        self._write_ndjson(self.solar, self._solar_rows())
        later = START + timedelta(hours=2)
        self.assertEqual(
            list(
                iter_solarassistant_records(
                    self.solar, later, later + timedelta(minutes=1)
                )
            ),
            [],
        )
        self.assertEqual(
            list(
                iter_eg4_day_records(
                    self.database, later, later + timedelta(minutes=1)
                )
            ),
            [],
        )

    def test_synthetic_end_to_end_adapters_feed_analyzer(self):
        self._write_ndjson(self.solar, self._solar_rows())
        self._write_ndjson(self.esp, self._esp_rows())
        eg4 = iter_eg4_day_records(self.database, START, END)
        runtime = iter_eg4_runtime_records(self.database, START, END)
        solar = iter_solarassistant_records(self.solar, START, END)
        esp = iter_esp32_records(self.esp, START, END, stream_kind="raw")
        report = analyze_correlation(eg4, solar, esp, eg4_context_records=runtime)
        self.assertEqual(report["event_count"], 1)
        event = report["events"][0]
        self.assertEqual(event["event_type"], "partial_collapse")
        self.assertEqual(event["eg4_before"]["values"]["estimated_soc_percent"], 50)
        solar_context = event["solarassistant_context"]["record"]
        self.assertEqual(solar_context["values"]["trusted_soc_percent"], 55)
        self.assertEqual(solar_context["provenance"]["input_name"], self.solar.name)
        self.assertEqual(event["esp32_nearest"]["status"], "exact")
        self.assertEqual(
            event["aligned_context"]["eg4_runtime"]["during"]["record"]["values"]
            ["operating_state"],
            "normal",
        )

    def test_out_of_tolerance_context_remains_missing_end_to_end(self):
        solar_rows = self._solar_rows()
        for row in solar_rows:
            row["received_at_utc"] = "2026-02-03T18:01:30.000Z"
        self._write_ndjson(self.solar, solar_rows)
        self._write_ndjson(
            self.esp,
            [
                {
                    "received_at_utc": "2026-02-03T18:01:05.000Z",
                    "id": "sensor-01_gen_frequency",
                    "value": 60.0,
                    "state": "60.0",
                }
            ],
        )
        report = analyze_correlation(
            iter_eg4_day_records(self.database, START, END),
            iter_solarassistant_records(self.solar, START, END),
            iter_esp32_records(self.esp, START, END, stream_kind="raw"),
        )
        event = report["events"][0]
        self.assertEqual(event["solarassistant_context"]["reason"], "out_of_tolerance")
        self.assertEqual(event["esp32_nearest"]["reason"], "out_of_tolerance")


if __name__ == "__main__":
    unittest.main()
