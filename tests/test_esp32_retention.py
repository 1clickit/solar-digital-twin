import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from solar_digital_twin.collectors.esp32_retention import (
    CONSERVATIVE_HEARTBEAT_SECONDS,
    CONSERVATIVE_NUMERIC_DEADBANDS,
    CONSERVATIVE_POLICY_ID,
    CURRENT_POLICY_ID,
    ConservativeESP32RetentionPolicy,
    CurrentESP32RetentionPolicy,
    record_is_unavailable,
)
from solar_digital_twin.analysis.correlation_adapters import (
    AdapterError,
    iter_esp32_records,
)


def record(entity, value, state=None):
    result = {"id": entity, "value": value}
    if state is not None:
        result["state"] = state
    return result


class ESP32PolicyIdentityTests(unittest.TestCase):
    def test_policy_identity_and_exact_candidate_definition(self):
        self.assertEqual(CURRENT_POLICY_ID, "esp32-frequency-v1")
        self.assertEqual(CONSERVATIVE_POLICY_ID, "esp32-conservative-v1")
        self.assertEqual(CONSERVATIVE_HEARTBEAT_SECONDS, 60.0)
        self.assertEqual(
            CONSERVATIVE_NUMERIC_DEADBANDS,
            {
                "sensor-01_estimated_total_ac-coupled_power": 10.0,
                "sensor-01_estimated_active_microinverters": 0.1,
                "sensor-01_estimated_curtailment_percent": 0.5,
                "sensor-01_gen_frequency": 0.04,
                "sensor-01_gen_l1_current": 0.1,
                "sensor-01_estimated_gen_l1-l2_voltage": 0.1,
                "sensor-01_estimated_total_ac-coupled_energy": 10.0,
                "sensor-02_power_ramp_rate": 10.0,
                "sensor-02_frequency_ramp_rate": 0.04,
                "sensor-02_largest_power_drop_since_reset": 10.0,
                "sensor-02_total_events_since_reset": 1.0,
            },
        )

    def test_every_numeric_deadband_both_directions(self):
        for entity, deadband in CONSERVATIVE_NUMERIC_DEADBANDS.items():
            with self.subTest(entity=entity, direction="up"):
                policy = ConservativeESP32RetentionPolicy()
                self.assertEqual(policy.retention_reason(record(entity, 0), 0), "first")
                self.assertIsNone(
                    policy.retention_reason(record(entity, deadband / 2), 1)
                )
                self.assertEqual(
                    policy.retention_reason(record(entity, deadband), 2), "change"
                )
            with self.subTest(entity=entity, direction="down"):
                policy = ConservativeESP32RetentionPolicy()
                self.assertEqual(policy.retention_reason(record(entity, 0), 0), "first")
                self.assertEqual(
                    policy.retention_reason(record(entity, -deadband), 1), "change"
                )

    def test_conservative_and_current_heartbeats_are_distinct(self):
        entity = "sensor-01_gen_frequency"
        conservative = ConservativeESP32RetentionPolicy()
        current = CurrentESP32RetentionPolicy()
        self.assertEqual(conservative.retention_reason(record(entity, 60), 0), "first")
        self.assertIsNone(conservative.retention_reason(record(entity, 60), 59.9))
        self.assertEqual(
            conservative.retention_reason(record(entity, 60), 60), "heartbeat"
        )
        self.assertIsNotNone(current.retention_reason(record(entity, 60), 0))
        self.assertIsNone(current.retention_reason(record(entity, 60), 29.9))
        self.assertIsNotNone(current.retention_reason(record(entity, 60), 30))

    def test_policy_instances_have_independent_state(self):
        entity = "sensor-01_estimated_total_ac-coupled_power"
        first = ConservativeESP32RetentionPolicy()
        second = ConservativeESP32RetentionPolicy()
        self.assertEqual(first.retention_reason(record(entity, 100), 0), "first")
        self.assertIsNone(first.retention_reason(record(entity, 105), 1))
        self.assertEqual(second.retention_reason(record(entity, 105), 1), "first")


class ESP32AvailabilityAndStateTests(unittest.TestCase):
    def test_exact_text_and_binary_changes(self):
        for entity, values in (
            ("text_sensor-00_current_status", ("NORMAL", "EVENT")),
            ("binary_sensor-03_large_power_drop_active", (False, True)),
        ):
            with self.subTest(entity=entity):
                policy = ConservativeESP32RetentionPolicy()
                self.assertEqual(policy.retention_reason(record(entity, values[0]), 0), "first")
                self.assertIsNone(policy.retention_reason(record(entity, values[0]), 1))
                self.assertEqual(
                    policy.retention_reason(record(entity, values[1]), 2), "change"
                )

    def test_unavailable_entry_and_equal_value_restoration_are_retained(self):
        entity = "sensor-01_gen_frequency"
        policy = ConservativeESP32RetentionPolicy()
        self.assertEqual(
            policy.retention_reason(record(entity, 60.0, "60.0"), 0), "first"
        )
        self.assertEqual(
            policy.retention_reason(record(entity, 60.0, "unavailable"), 1),
            "availability_transition",
        )
        self.assertIsNone(
            policy.retention_reason(record(entity, 60.0, "unavailable"), 2)
        )
        self.assertEqual(
            policy.retention_reason(record(entity, 60.0, "60.0"), 3),
            "availability_transition",
        )

    def test_only_documented_unavailable_values_are_normalized(self):
        for value in (None, "unavailable", "UNKNOWN", "none", "nan", "null"):
            self.assertTrue(record_is_unavailable({"value": value}))
        for value in (0, False, "available", "none-ish", "unknown mode"):
            self.assertFalse(record_is_unavailable({"value": value}))

    def test_availability_is_entity_local(self):
        policy = ConservativeESP32RetentionPolicy()
        self.assertEqual(policy.retention_reason(record("sensor-a", 1), 0), "first")
        self.assertEqual(
            policy.retention_reason(record("sensor-a", None), 1),
            "availability_transition",
        )
        self.assertEqual(policy.retention_reason(record("sensor-b", 1), 2), "first")


class ESP32ParserCompatibilityTests(unittest.TestCase):
    def test_conservative_telemetry_parses_and_manifest_stays_separate(self):
        telemetry = {
            "received_at_utc": "2026-07-16T00:00:00.000Z",
            "id": "sensor-01_gen_frequency",
            "value": 60.0,
            "state": "60.0",
        }
        manifest = {
            "manifest_schema": "solar-digital-twin.esp32-capture.v1",
            "event": "start",
        }
        start = datetime(2026, 7, 15, tzinfo=timezone.utc)
        end = datetime(2026, 7, 17, tzinfo=timezone.utc)
        with TemporaryDirectory() as directory:
            retained = Path(directory) / "retained.ndjson"
            manifest_path = Path(directory) / "manifest.ndjson"
            retained.write_text(json.dumps(telemetry) + "\n")
            manifest_path.write_text(json.dumps(manifest) + "\n")
            parsed = list(
                iter_esp32_records(
                    retained, start, end, stream_kind="retained"
                )
            )
            with self.assertRaises(AdapterError):
                list(
                    iter_esp32_records(
                        manifest_path, start, end, stream_kind="retained"
                    )
                )

        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0].values["metric_id"], telemetry["id"])


if __name__ == "__main__":
    unittest.main()
