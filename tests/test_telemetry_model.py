import json
import unittest
from copy import deepcopy

from solar_digital_twin.telemetry import (
    ContractValidationError,
    LineageHop,
    validate_record,
)


class TelemetryModelTests(unittest.TestCase):
    def setUp(self):
        self.record = {
            "contract_version": "solar-digital-twin.telemetry-observation.v1",
            "record_kind": "observation",
            "observation": {"product_kind": "root"},
            "record_id": "test-record:root",
            "observation_id": "test-observation:root",
            "metric_id": "solarassistant.jk_bms.combined.state_of_charge",
            "source": {
                "system": "solarassistant",
                "device": "jk_bms_bank",
                "metric_id": "total/battery_state_of_charge",
                "role": "authority",
                "transport": "solarassistant_rest_v1",
                "lineage": [{
                    "system": "solarassistant",
                    "instance": "jk_bms_bank",
                    "role": "root",
                    "reference": "total/battery_state_of_charge",
                    "transformation_id": None,
                    "unresolved": False,
                }],
            },
            "time": {
                "source_at": None,
                "source_at_raw": None,
                "source_changed_at": None,
                "received_at": "2026-01-15T18:00:01.123Z",
                "observed_at": "2026-01-15T18:00:01.123Z",
                "basis": "solardt_receipt",
                "source_timezone": None,
                "precision": "millisecond",
                "clock_quality": "unknown",
                "uncertainty_ms": None,
            },
            "sequence": {"ingest": 3, "source": None},
            "value": {
                "raw_present": True,
                "raw": 0,
                "raw_type": "number",
                "normalized": 0,
                "raw_unit": "%",
                "canonical_unit": "%",
                "source_nature": "measured",
                "result_nature": "source_value",
                "raw_unit_basis": "source_supplied",
                "raw_unit_mapping": None,
            },
            "availability": "available",
            "validity": "valid",
            "capability": "supported",
            "quality": {
                "categories": ["direct", "clock_uncertain"],
                "reasons": ["source_time_absent"],
            },
            "transformation": {"id": None, "version": None, "method": None},
            "parents": [],
            "producer": {"name": "test_adapter", "version": "test-v1"},
            "evidence": {
                "synthetic": True,
                "capture_id": "test-capture",
                "record_ref": "test-record",
            },
            "retention": {"stream": "raw", "policy_id": None},
            "diagnostics": {"reason_codes": []},
        }

    def assert_reason(self, record, reason):
        with self.assertRaises(ContractValidationError) as raised:
            validate_record(record)
        self.assertEqual(raised.exception.reason_code, reason)

    def test_complete_root_profile_is_json_compatible_and_detached(self):
        original = deepcopy(self.record)
        validated = validate_record(self.record)
        json.dumps(validated, allow_nan=False)
        self.assertEqual(self.record, original)
        validated["value"]["raw"] = 50
        self.assertEqual(self.record["value"]["raw"], 0)

    def test_lineage_construction_is_immutable_and_json_compatible(self):
        hop = LineageHop(
            system="solarassistant",
            instance="jk_bms_bank",
            role="root",
            reference="total/battery_state_of_charge",
        )
        with self.assertRaises(AttributeError):
            hop.system = "direct_jk"
        self.assertEqual(hop.as_mapping(), self.record["source"]["lineage"][0])
        json.dumps(hop.as_mapping(), allow_nan=False)

    def test_unsupported_record_product_and_time_enums_fail_safely(self):
        cases = (
            ("record_kind", ["future"], "unsupported_record_kind"),
            ("product_kind", "future", "unsupported_product_kind"),
            ("basis", "future", "unsupported_time_basis"),
            ("basis", ["future"], "unsupported_time_basis"),
        )
        for field, value, reason in cases:
            with self.subTest(field=field):
                record = deepcopy(self.record)
                if field == "record_kind":
                    record[field] = value
                elif field == "product_kind":
                    record["observation"][field] = value
                else:
                    record["time"][field] = value
                self.assert_reason(record, reason)

    def test_root_profile_rejects_wrong_source_or_transformation(self):
        record = deepcopy(self.record)
        record["source"]["transport"] = "direct_jk"
        self.assert_reason(record, "invalid_source_transport")

        record = deepcopy(self.record)
        record["transformation"]["id"] = "no-op"
        self.assert_reason(record, "unexpected_transformation")

        record = deepcopy(self.record)
        record["status"] = {"scope": "source", "state": "unreachable"}
        self.assert_reason(record, "invalid_root_profile")

    def test_exact_registry_profiles_reject_cross_source_substitution(self):
        esp32 = deepcopy(self.record)
        esp32["metric_id"] = "esp32.esphome.forensic_probe.generator_frequency"
        esp32["source"] = {
            "system": "esp32",
            "device": "forensic_probe",
            "metric_id": "sensor-01_gen_frequency",
            "role": "forensic",
            "transport": "http_sse",
            "lineage": [
                {
                    "system": "esp32",
                    "instance": "forensic_probe",
                    "role": "root",
                    "reference": "sensor-01_gen_frequency",
                    "transformation_id": None,
                    "unresolved": False,
                }
            ],
        }
        esp32["value"].update(
            {
                "raw": 30000,
                "normalized": 30000,
                "raw_unit": "Hz",
                "canonical_unit": "Hz",
                "raw_unit_basis": "adapter_specified",
                "raw_unit_mapping": {
                    "id": "esp32.esphome.sensor-01_gen_frequency.unit",
                    "version": "1",
                },
            }
        )
        esp32["evidence"]["source_fields"] = {
            "id": "sensor-01_gen_frequency",
            "name": "01 GEN Frequency",
            "domain": "sensor",
            "value": 30000,
            "state": "30000 Hz",
            "source_url": "http://synthetic.invalid/events",
        }
        validate_record(esp32)

        mixed = deepcopy(esp32)
        mixed["source"]["role"] = "authority"
        self.assert_reason(mixed, "invalid_source_role")

        mixed = deepcopy(esp32)
        mixed["value"]["raw_unit_basis"] = "source_supplied"
        self.assert_reason(mixed, "invalid_raw_unit_basis")

        mixed = deepcopy(self.record)
        mixed["source"]["system"] = "esp32"
        self.assert_reason(mixed, "invalid_source_system")

        mixed = deepcopy(self.record)
        mixed["value"]["raw_unit_mapping"] = {
            "id": "esp32.esphome.sensor-01_gen_frequency.unit",
            "version": "1",
        }
        self.assert_reason(mixed, "unexpected_unit_mapping")

    def test_invalid_json_value_and_time_are_bounded(self):
        record = deepcopy(self.record)
        record["value"]["raw"] = float("nan")
        self.assert_reason(record, "invalid_root_value")

        record = deepcopy(self.record)
        record["time"]["received_at"] = "2026-01-15T18:00:01Z"
        self.assert_reason(record, "invalid_received_at")

    def test_required_nullable_root_fields_cannot_be_omitted(self):
        cases = (
            ("source_at", "time", "incomplete_root_time"),
            ("source_timezone", "time", "incomplete_root_time"),
            ("raw_unit_mapping", "value", "incomplete_root_value"),
            ("id", "transformation", "incomplete_root_transformation"),
            ("policy_id", "retention", "incomplete_root_retention"),
        )
        for field, section, reason in cases:
            with self.subTest(section=section, field=field):
                record = deepcopy(self.record)
                del record[section][field]
                self.assert_reason(record, reason)

    def test_source_status_requires_nullable_fields_and_prohibits_observation_fields(self):
        status = {
            "contract_version": "solar-digital-twin.telemetry-observation.v1",
            "record_kind": "status",
            "record_id": "test-record:status",
            "metric_id": None,
            "status": {"scope": "source", "state": "unreachable"},
            "source": {
                "system": "solarassistant",
                "device": None,
                "metric_id": None,
                "role": "operational",
                "transport": "solarassistant_rest_v1",
                "lineage": [{
                    "system": "solarassistant",
                    "instance": "solarassistant",
                    "role": "root",
                    "reference": "solarassistant_rest_v1",
                    "transformation_id": None,
                    "unresolved": False,
                }],
            },
            "time": {
                "source_at": None,
                "source_at_raw": None,
                "source_changed_at": None,
                "received_at": "2026-01-15T18:00:02.000Z",
                "observed_at": "2026-01-15T18:00:02.000Z",
                "basis": "status_detection",
                "source_timezone": None,
                "precision": "millisecond",
                "clock_quality": "unknown",
                "uncertainty_ms": None,
            },
            "sequence": {"ingest": 4, "source": None},
            "producer": {"name": "test_adapter", "version": "test-v1"},
            "evidence": {"synthetic": True},
            "diagnostics": {"reason_codes": ["source_transport_unreachable"]},
        }
        validate_record(status)

        missing = deepcopy(status)
        del missing["source"]["device"]
        self.assert_reason(missing, "incomplete_status_source")

        missing = deepcopy(status)
        del missing["time"]["source_at"]
        self.assert_reason(missing, "incomplete_status_time")

        for field, value in (
            ("observation", {"product_kind": "root"}),
            ("value", {}),
            ("availability", "unavailable"),
            ("retention", {"stream": "raw", "policy_id": None}),
        ):
            with self.subTest(prohibited=field):
                invalid = deepcopy(status)
                invalid[field] = value
                self.assert_reason(invalid, "invalid_status_profile")


if __name__ == "__main__":
    unittest.main()
