import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.analyze_esp32_retention import analyze, replay_candidate
from solar_digital_twin.collectors.esp32_retention import (
    ConservativeESP32RetentionPolicy,
)


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

    def test_replay_candidate_writes_only_selected_unchanged_records(self):
        records = [
            record("2026-07-16T00:00:00.000Z", "sensor-test", 1.0),
            record("2026-07-16T00:00:01.000Z", "sensor-test", 1.0),
            record("2026-07-16T00:00:02.000Z", "sensor-test", "unavailable"),
            record("2026-07-16T00:00:03.000Z", "sensor-test", 2.0),
        ]
        with TemporaryDirectory() as directory:
            raw = Path(directory) / "raw.ndjson"
            output = Path(directory) / "candidate.ndjson"
            content = "".join(json.dumps(item) + "\n" for item in records)
            raw.write_text(content)
            before = raw.read_bytes()
            result = replay_candidate(raw, output)

            replayed = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual(raw.read_bytes(), before)

        self.assertEqual(replayed, [records[0], records[2], records[3]])
        self.assertEqual(result["records"], 3)
        self.assertEqual(result["reasons"]["first"], 1)
        self.assertEqual(result["reasons"]["availability_transition"], 2)
        self.assertEqual(result["entity_counts"], {"sensor-test": 3})
        self.assertEqual(result["first_timestamp_utc"], records[0]["received_at_utc"])
        self.assertEqual(result["last_timestamp_utc"], records[3]["received_at_utc"])

    def test_replay_candidate_rejects_backward_timestamps(self):
        records = [
            record("2026-07-16T00:00:01.000Z", "sensor-test", 1),
            record("2026-07-16T00:00:00.000Z", "sensor-test", 2),
        ]
        with TemporaryDirectory() as directory:
            raw = Path(directory) / "raw.ndjson"
            output = Path(directory) / "candidate.ndjson"
            raw.write_text("".join(json.dumps(item) + "\n" for item in records))
            with self.assertRaisesRegex(ValueError, "timestamp moved backward"):
                replay_candidate(raw, output)

    def test_replay_matches_canonical_policy_with_availability(self):
        records = [
            record("2026-07-16T00:00:00.000Z", "sensor-01_gen_frequency", 60.0),
            record("2026-07-16T00:00:01.000Z", "sensor-01_gen_frequency", 60.01),
            {
                **record(
                    "2026-07-16T00:00:02.000Z",
                    "sensor-01_gen_frequency",
                    60.0,
                ),
                "state": "unavailable",
            },
            {
                **record(
                    "2026-07-16T00:00:03.000Z",
                    "sensor-01_gen_frequency",
                    60.0,
                ),
                "state": "60.0",
            },
        ]
        policy = ConservativeESP32RetentionPolicy()
        expected = [
            item
            for second, item in enumerate(records)
            if policy.retention_reason(item, float(second)) is not None
        ]
        with TemporaryDirectory() as directory:
            raw = Path(directory) / "raw.ndjson"
            output = Path(directory) / "candidate.ndjson"
            raw.write_text("".join(json.dumps(item) + "\n" for item in records))
            replay_candidate(raw, output)
            actual = [json.loads(line) for line in output.read_text().splitlines()]

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
