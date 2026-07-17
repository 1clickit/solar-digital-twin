import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.analyze_esp32_retention import analyze


def record(timestamp, entity, value):
    return {
        "received_at_utc": timestamp,
        "id": entity,
        "value": value,
    }


class Esp32RetentionAnalysisTests(unittest.TestCase):
    def test_streaming_summary_and_candidates(self):
        raw_records = [
            record("2026-07-16T00:00:00.000Z", "sensor-01_gen_frequency", 60.00),
            record("2026-07-16T00:00:01.000Z", "sensor-01_gen_frequency", 60.01),
            record("2026-07-16T00:00:31.000Z", "sensor-01_gen_frequency", 60.01),
            record("2026-07-16T00:00:00.000Z", "text_sensor-00_current_status", "OK"),
            record("2026-07-16T00:00:01.000Z", "text_sensor-00_current_status", "OK"),
        ]
        retained_records = [raw_records[0], raw_records[2], raw_records[3], raw_records[4]]
        with TemporaryDirectory() as directory:
            raw = Path(directory) / "raw.ndjson"
            retained = Path(directory) / "retained.ndjson"
            raw.write_text("".join(json.dumps(item) + "\n" for item in raw_records))
            retained.write_text(
                "".join(json.dumps(item) + "\n" for item in retained_records)
            )
            result = analyze(raw, retained)

        frequency = result["entities"]["sensor-01_gen_frequency"]
        self.assertEqual(frequency["raw"], 3)
        self.assertEqual(frequency["retained"], 2)
        self.assertEqual(frequency["repeats"], 1)
        self.assertEqual(result["raw"]["records"], 5)
        self.assertEqual(result["candidates"]["current"]["records"], 4)
        self.assertLess(
            result["candidates"]["exact_change_120s"]["records"],
            result["candidates"]["current"]["records"],
        )

    def test_availability_transition_is_preserved_by_candidates(self):
        records = [
            record("2026-07-16T00:00:00.000Z", "sensor-test", "unavailable"),
            record("2026-07-16T00:00:01.000Z", "sensor-test", 1.0),
        ]
        with TemporaryDirectory() as directory:
            raw = Path(directory) / "raw.ndjson"
            retained = Path(directory) / "retained.ndjson"
            content = "".join(json.dumps(item) + "\n" for item in records)
            raw.write_text(content)
            retained.write_text(content)
            result = analyze(raw, retained)

        combined = result["candidates"]["conservative_combined_60s"]
        self.assertEqual(combined["reasons"]["availability_transition"], 1)


if __name__ == "__main__":
    unittest.main()
