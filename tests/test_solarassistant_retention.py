import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from solar_digital_twin.collectors import solarassistant
from solar_digital_twin.collectors.solarassistant_retention import (
    DAILY_HEARTBEAT_SECONDS,
    MEANINGFUL_CHANGE_TOPICS,
    SOC_HEARTBEAT_SECONDS,
    SolarAssistantRetentionPolicy,
)
from tests.test_solarassistant import FakeClock, FakeResponse, FakeSession


def record(topic, value, **identity):
    return {
        "received_at_utc": "2026-07-15T12:00:00.000Z",
        "source_url": solarassistant.METRICS_URL,
        "topic": topic,
        "device": identity.get("device", "Battery"),
        "number": identity.get("number", 1),
        "group": identity.get("group", "Battery"),
        "name": identity.get("name", topic),
        "value": value,
        "unit": identity.get("unit", "%"),
    }


class SolarAssistantPolicyTests(unittest.TestCase):
    def test_soc_first_change_suppression_and_heartbeat(self):
        policy = SolarAssistantRetentionPolicy()
        observation = record("total/battery_state_of_charge", 50)

        self.assertEqual(policy.retention_reason(observation, 0.0), "change")
        self.assertIsNone(policy.retention_reason(observation, 299.0))
        changed = dict(observation, value=51)
        self.assertEqual(policy.retention_reason(changed, 299.0), "change")
        self.assertIsNone(policy.retention_reason(changed, 598.9))
        self.assertEqual(
            policy.retention_reason(changed, 299.0 + SOC_HEARTBEAT_SECONDS),
            "heartbeat",
        )

    def test_suppressed_duplicate_does_not_reset_heartbeat(self):
        policy = SolarAssistantRetentionPolicy()
        observation = record("battery_1/state_of_charge", 70)

        self.assertEqual(policy.retention_reason(observation, 100.0), "change")
        self.assertIsNone(policy.retention_reason(observation, 399.0))
        self.assertEqual(policy.retention_reason(observation, 400.0), "heartbeat")

    def test_daily_topics_use_daily_heartbeat(self):
        for topic in (
            "total/battery_state_of_health",
            "battery_1/capacity",
            "battery_2/charge_capacity",
            "battery_1/cycles",
        ):
            with self.subTest(topic=topic):
                policy = SolarAssistantRetentionPolicy()
                observation = record(topic, 95)
                self.assertEqual(policy.retention_reason(observation, 0.0), "change")
                self.assertIsNone(
                    policy.retention_reason(observation, DAILY_HEARTBEAT_SECONDS - 0.1)
                )
                self.assertEqual(
                    policy.retention_reason(observation, DAILY_HEARTBEAT_SECONDS),
                    "heartbeat",
                )

    def test_distinct_metric_identities_have_independent_state(self):
        policy = SolarAssistantRetentionPolicy()
        first = record("battery_1/state_of_charge", 60, device="JK A", number=1)
        second = record("battery_1/state_of_charge", 60, device="JK B", number=2)

        self.assertEqual(policy.retention_reason(first, 0.0), "change")
        self.assertEqual(policy.retention_reason(second, 1.0), "change")
        self.assertIsNone(policy.retention_reason(first, 2.0))

    def test_meaningful_change_topics_are_explicitly_raw_only(self):
        policy = SolarAssistantRetentionPolicy()
        self.assertIn("total/battery_voltage", MEANINGFUL_CHANGE_TOPICS)
        self.assertIn("battery_1/temperature_mos", MEANINGFUL_CHANGE_TOPICS)
        for topic in MEANINGFUL_CHANGE_TOPICS:
            self.assertIsNone(policy.retention_reason(record(topic, 1), 0.0))

    def test_every_approved_topic_has_one_explicit_policy_classification(self):
        approved = solarassistant.COMBINED_TOPICS | {
            f"{prefix}/{suffix}"
            for prefix in ("battery_1", "battery_2")
            for suffix in solarassistant.INDIVIDUAL_SUFFIXES
        }
        from solar_digital_twin.collectors.solarassistant_retention import (
            DAILY_TOPICS,
            SOC_TOPICS,
        )

        classifications = (SOC_TOPICS, DAILY_TOPICS, MEANINGFUL_CHANGE_TOPICS)
        self.assertEqual(set().union(*classifications), approved)
        self.assertTrue(all(
            left.isdisjoint(right)
            for index, left in enumerate(classifications)
            for right in classifications[index + 1:]
        ))

    def test_invalid_values_do_not_mutate_state(self):
        policy = SolarAssistantRetentionPolicy()
        topic = "battery_2/state_of_charge"
        self.assertIsNone(policy.retention_reason(record(topic, "unknown"), 0.0))
        self.assertEqual(policy.retention_reason(record(topic, 80), 1.0), "change")


class SolarAssistantRetainedCollectorTests(unittest.TestCase):
    def test_raw_poll_coverage_separate_retained_file_and_request_count(self):
        rows = [
            {"topic": "total/battery_state_of_charge", "value": 50},
            {"topic": "total/battery_voltage", "value": 52.1},
            {"topic": "total/battery_state_of_health", "value": 99},
        ]
        responses = [FakeResponse(rows=rows), FakeResponse(rows=rows)]
        session = FakeSession(responses)
        clock = FakeClock()

        with tempfile.TemporaryDirectory() as directory:
            raw_path = Path(directory) / "solarassistant_test.ndjson"
            with (
                patch.object(solarassistant.requests, "Session", return_value=session),
                patch.object(solarassistant, "new_output_path", return_value=raw_path),
                patch.object(solarassistant.time, "monotonic", side_effect=clock.monotonic),
                patch.object(solarassistant.time, "sleep", side_effect=clock.sleep),
                patch.object(solarassistant, "receipt_timestamp", return_value="2026-07-15T12:00:00.000Z"),
            ):
                _, written = solarassistant.collect(2.0, 1.0, "synthetic-secret")

            retained_path = solarassistant.retained_output_path(raw_path)
            raw_records = [json.loads(line) for line in raw_path.read_text().splitlines()]
            retained_records = [
                json.loads(line) for line in retained_path.read_text().splitlines()
            ]

        self.assertNotEqual(raw_path, retained_path)
        self.assertEqual(len(session.calls), 2)
        self.assertTrue(all(response.closed for response in responses))
        self.assertEqual(written, 6)
        self.assertEqual(len(raw_records), 6)
        self.assertEqual(len(retained_records), 2)
        self.assertEqual(
            {item["topic"] for item in retained_records},
            {"total/battery_state_of_charge", "total/battery_state_of_health"},
        )
        self.assertTrue(all(item["retention_reason"] == "change" for item in retained_records))
        self.assertTrue(all("retention_reason" not in item for item in raw_records))
        self.assertEqual(
            set(raw_records[0]),
            {"received_at_utc", "source_url", "topic", "device", "number", "group", "name", "value", "unit"},
        )

    def test_raw_record_is_flushed_before_retention_processing(self):
        response = FakeResponse(rows=[
            {"topic": "total/battery_state_of_charge", "value": 50},
        ])
        session = FakeSession([response])
        clock = FakeClock()

        class FailingPolicy:
            def retention_reason(self, observation, monotonic_now):
                raise RuntimeError("synthetic retention failure")

        with tempfile.TemporaryDirectory() as directory:
            raw_path = Path(directory) / "solarassistant_test.ndjson"
            with (
                patch.object(solarassistant.requests, "Session", return_value=session),
                patch.object(solarassistant, "new_output_path", return_value=raw_path),
                patch.object(solarassistant, "SolarAssistantRetentionPolicy", return_value=FailingPolicy()),
                patch.object(solarassistant.time, "monotonic", side_effect=clock.monotonic),
                patch.object(solarassistant, "receipt_timestamp", return_value="2026-07-15T12:00:00.000Z"),
            ):
                with self.assertRaises(RuntimeError):
                    solarassistant.collect(1.0, 1.0, "synthetic-secret")

            raw_records = [json.loads(line) for line in raw_path.read_text().splitlines()]

        self.assertEqual(len(raw_records), 1)
        self.assertTrue(response.closed)


if __name__ == "__main__":
    unittest.main()
