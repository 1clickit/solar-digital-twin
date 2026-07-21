import builtins
import json
import sqlite3
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from solar_digital_twin.telemetry import AdapterContext, AdapterError
from solar_digital_twin.telemetry.registry import REGISTRY_V1
from solar_digital_twin.telemetry.solarassistant_adapter import (
    SolarAssistantSocAdapter,
)


FIXTURE = Path(__file__).parent / "fixtures" / "telemetry" / "solarassistant_combined_soc.json"


class SyntheticObservationIds:
    def __init__(self):
        self.descriptors = []

    def observation_id_for(self, descriptor):
        self.descriptors.append(deepcopy(descriptor))
        return f"test-observation:{descriptor['poll_group_id']}"


class SyntheticRecordIds:
    def __init__(self):
        self.descriptors = []

    def record_id_for(self, descriptor):
        self.descriptors.append(deepcopy(descriptor))
        if descriptor["record_kind"] == "observation":
            retention = descriptor["retention"]["stream"]
            reference = descriptor["evidence"]["record_ref"]
            return f"test-record:{retention}:{reference}"
        if descriptor["record_kind"] == "status":
            return "test-record:status:outage"
        return f"test-record:rejection:{descriptor['reason_code']}"


class InvalidObservationIds:
    def observation_id_for(self, descriptor):
        return ""


class InvalidObservationRecordIds(SyntheticRecordIds):
    def record_id_for(self, descriptor):
        if descriptor["record_kind"] == "observation":
            return ""
        return super().record_id_for(descriptor)


class InvalidAllRecordIds:
    def record_id_for(self, descriptor):
        return ""


class SolarAssistantSocAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def setUp(self):
        self.observation_ids = SyntheticObservationIds()
        self.record_ids = SyntheticRecordIds()
        self.context = AdapterContext(
            registry_version="1",
            producer_name="solarassistant_soc_adapter",
            producer_version="test-v1",
            observation_id_provider=self.observation_ids,
            record_id_provider=self.record_ids,
        )
        self.adapter = SolarAssistantSocAdapter()

    def adapt(self, record=None, evidence=None, **kwargs):
        return self.adapter.adapt(
            deepcopy(self.fixture["valid_poll"] if record is None else record),
            self.context,
            deepcopy(self.fixture["raw_evidence"] if evidence is None else evidence),
            kwargs.pop("ingest_sequence", 7),
            **kwargs,
        )

    def test_registry_contains_exactly_the_accepted_metric(self):
        self.assertEqual(tuple(REGISTRY_V1), ("total/battery_state_of_charge",))
        metric = REGISTRY_V1["total/battery_state_of_charge"]
        self.assertEqual(metric.metric_id, "solarassistant.jk_bms.combined.state_of_charge")
        self.assertEqual(metric.source_system, "solarassistant")
        self.assertEqual(metric.source_device, "jk_bms_bank")
        self.assertEqual(metric.source_role, "authority")
        self.assertEqual(metric.source_transport, "solarassistant_rest_v1")
        self.assertEqual(metric.telemetry_namespace, "jk_bms")

    def test_valid_input_yields_one_root_observation_and_no_normalized_product(self):
        source = deepcopy(self.fixture["valid_poll"])
        records = self.adapt(source)
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["record_kind"], "observation")
        self.assertEqual(record["observation"], {"product_kind": "root"})
        self.assertNotEqual(record["observation"]["product_kind"], "normalized")
        self.assertEqual(record["metric_id"], "solarassistant.jk_bms.combined.state_of_charge")
        self.assertEqual(record["source"], {
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
        })
        self.assertNotIn("jk_bms", {hop["system"] for hop in record["source"]["lineage"]})
        self.assertEqual(record["time"]["observed_at"], source["received_at_utc"])
        self.assertEqual(record["time"]["basis"], "solardt_receipt")
        self.assertEqual(record["value"]["raw"], 82.375)
        self.assertEqual(record["value"]["normalized"], 82.375)
        self.assertEqual(record["value"]["raw_unit"], "%")
        self.assertEqual(record["value"]["canonical_unit"], "%")
        self.assertEqual(record["value"]["raw_unit_basis"], "source_supplied")
        self.assertEqual(record["value"]["source_nature"], "measured")
        self.assertEqual(record["value"]["result_nature"], "source_value")
        self.assertEqual(record["transformation"], {"id": None, "version": None, "method": None})
        self.assertEqual(record["sequence"]["ingest"], 7)
        self.assertEqual(record["evidence"]["poll_group_id"], "synthetic-poll-001")
        json.dumps(record, allow_nan=False)

    def test_zero_and_boundaries_remain_valid_without_rounding(self):
        for value in (0, 0.125, 100):
            with self.subTest(value=value):
                source = deepcopy(self.fixture["valid_poll"])
                source["value"] = value
                record = self.adapt(source)[0]
                self.assertEqual(record["value"]["raw"], value)
                self.assertEqual(record["value"]["normalized"], value)
                self.assertEqual(record["validity"], "valid")

    def test_missing_value_rejects_but_explicit_states_are_observations(self):
        missing = deepcopy(self.fixture["valid_poll"])
        del missing["value"]
        rejection = self.adapt(missing)[0]
        self.assertEqual(rejection["record_kind"], "rejection")
        self.assertEqual(rejection["diagnostics"]["reason_codes"], ["missing_value"])
        self.assertNotIn("observation_id", rejection)

        cases = (
            (None, "null", "unknown", "explicit_null"),
            ("unknown", "string", "unknown", "source_unknown"),
            ("unavailable", "string", "unavailable", "source_unavailable"),
        )
        for value, raw_type, availability, reason in cases:
            with self.subTest(reason=reason):
                source = deepcopy(self.fixture["valid_poll"])
                source["value"] = value
                record = self.adapt(source)[0]
                self.assertEqual(record["record_kind"], "observation")
                self.assertEqual(record["observation"], {"product_kind": "root"})
                self.assertEqual(record["value"]["raw"], value)
                self.assertEqual(record["value"]["raw_type"], raw_type)
                self.assertIsNone(record["value"]["normalized"])
                self.assertEqual(record["value"]["source_nature"], "state")
                self.assertEqual(record["value"]["result_nature"], "source_value")
                self.assertEqual(record["value"]["raw_unit"], "%")
                self.assertEqual(record["value"]["canonical_unit"], "%")
                self.assertEqual(record["value"]["raw_unit_basis"], "source_supplied")
                self.assertIsNone(record["value"]["raw_unit_mapping"])
                self.assertEqual(record["availability"], availability)
                self.assertEqual(record["validity"], "valid")
                self.assertEqual(record["capability"], "supported")
                self.assertEqual(record["diagnostics"]["reason_codes"], [reason])
                self.assertEqual(
                    record["quality"]["reasons"], ["source_time_absent", reason]
                )
                self.assertEqual(
                    record["transformation"],
                    {"id": None, "version": None, "method": None},
                )
                self.assertEqual(record["parents"], [])

    def test_raw_and_retained_state_copies_share_observation_identity(self):
        source = deepcopy(self.fixture["valid_poll"])
        source["value"] = "unavailable"
        raw = self.adapter.adapt(
            source, self.context, self.fixture["raw_evidence"], 5
        )[0]
        retained = self.adapter.adapt(
            source,
            self.context,
            self.fixture["retained_evidence"],
            5,
            retention_stream="retained",
            retention_policy_id="solarassistant-retention-v1",
        )[0]
        self.assertEqual(raw["observation_id"], retained["observation_id"])
        self.assertNotEqual(raw["record_id"], retained["record_id"])
        self.assertNotEqual(raw["evidence"], retained["evidence"])

    def test_explicit_states_still_require_the_source_unit(self):
        for value in (None, "unknown", "unavailable"):
            with self.subTest(value=value):
                source = deepcopy(self.fixture["valid_poll"])
                source["value"] = value
                del source["unit"]
                rejection = self.adapt(source)[0]
                self.assertEqual(
                    rejection["diagnostics"]["reason_codes"], ["missing_unit"]
                )

    def test_malformed_and_invalid_values_have_bounded_reasons(self):
        cases = (
            (True, "invalid_numeric_boolean"),
            (float("nan"), "invalid_numeric_non_finite"),
            (float("inf"), "invalid_numeric_non_finite"),
            (-0.1, "invalid_numeric_range"),
            (100.1, "invalid_numeric_range"),
            ("82", "unsupported_value"),
        )
        for value, reason in cases:
            with self.subTest(reason=reason):
                source = deepcopy(self.fixture["valid_poll"])
                source["value"] = value
                rejection = self.adapt(source)[0]
                self.assertEqual(rejection["diagnostics"]["reason_codes"], [reason])
                self.assertNotIn(str(value), rejection["diagnostics"]["reason_codes"])

    def test_topic_unit_time_registry_sequence_and_provenance_rejections(self):
        cases = []
        source = deepcopy(self.fixture["valid_poll"])
        source["topic"] = "battery_1/state_of_charge"
        cases.append((source, self.fixture["raw_evidence"], {}, "unapproved_topic"))
        source = deepcopy(self.fixture["valid_poll"])
        del source["unit"]
        cases.append((source, self.fixture["raw_evidence"], {}, "missing_unit"))
        source = deepcopy(self.fixture["valid_poll"])
        source["unit"] = "percent"
        cases.append((source, self.fixture["raw_evidence"], {}, "unit_mismatch"))
        source = deepcopy(self.fixture["valid_poll"])
        source["received_at_utc"] = "bad-time"
        cases.append((source, self.fixture["raw_evidence"], {"detection_time": "2026-01-15T18:00:02.000Z"}, "invalid_receipt_time"))
        cases.append((self.fixture["valid_poll"], {"synthetic": True}, {}, "invalid_evidence"))
        conflicting_evidence = deepcopy(self.fixture["raw_evidence"])
        conflicting_evidence["poll_group_id"] = "another-poll"
        cases.append((self.fixture["valid_poll"], conflicting_evidence, {}, "invalid_evidence"))
        cases.append((self.fixture["valid_poll"], self.fixture["raw_evidence"], {"ingest_sequence": -1}, "invalid_ingest_sequence"))
        for source, evidence, kwargs, reason in cases:
            with self.subTest(reason=reason):
                rejection = self.adapt(source, evidence, **kwargs)[0]
                self.assertEqual(rejection["diagnostics"]["reason_codes"], [reason])

        bad_context = AdapterContext(
            registry_version="future",
            producer_name="solarassistant_soc_adapter",
            producer_version="test-v1",
            observation_id_provider=self.observation_ids,
            record_id_provider=self.record_ids,
        )
        rejection = self.adapter.adapt(
            self.fixture["valid_poll"],
            bad_context,
            self.fixture["raw_evidence"],
            1,
        )[0]
        self.assertEqual(rejection["diagnostics"]["reason_codes"], ["registry_mismatch"])

    def test_raw_and_retained_share_observation_id_but_not_record_id(self):
        raw = self.adapter.adapt(
            self.fixture["valid_poll"], self.context, self.fixture["raw_evidence"], 5
        )[0]
        retained = self.adapter.adapt(
            self.fixture["valid_poll"],
            self.context,
            self.fixture["retained_evidence"],
            5,
            retention_stream="retained",
            retention_policy_id="solarassistant-retention-v1",
        )[0]
        self.assertEqual(raw["observation_id"], retained["observation_id"])
        self.assertNotEqual(raw["record_id"], retained["record_id"])
        self.assertNotEqual(raw["evidence"], retained["evidence"])
        self.assertEqual(raw["retention"], {"stream": "raw", "policy_id": None})
        self.assertEqual(retained["retention"], {
            "stream": "retained",
            "policy_id": "solarassistant-retention-v1",
        })
        for descriptor in self.observation_ids.descriptors:
            self.assertNotIn("retention", descriptor)
            self.assertNotIn("evidence", descriptor)
            self.assertNotIn("producer_version", descriptor)

    def test_separate_injected_id_providers_and_invalid_ids(self):
        context = AdapterContext(
            registry_version="1",
            producer_name="solarassistant_soc_adapter",
            producer_version="test-v1",
            observation_id_provider=InvalidObservationIds(),
            record_id_provider=SyntheticRecordIds(),
        )
        rejection = self.adapter.adapt(
            self.fixture["valid_poll"], context, self.fixture["raw_evidence"], 1
        )[0]
        self.assertEqual(rejection["diagnostics"]["reason_codes"], ["invalid_observation_id"])

        context = AdapterContext(
            registry_version="1",
            producer_name="solarassistant_soc_adapter",
            producer_version="test-v1",
            observation_id_provider=SyntheticObservationIds(),
            record_id_provider=InvalidObservationRecordIds(),
        )
        rejection = self.adapter.adapt(
            self.fixture["valid_poll"], context, self.fixture["raw_evidence"], 1
        )[0]
        self.assertEqual(rejection["diagnostics"]["reason_codes"], ["invalid_record_id"])

        context = AdapterContext(
            registry_version="1",
            producer_name="solarassistant_soc_adapter",
            producer_version="test-v1",
            observation_id_provider=SyntheticObservationIds(),
            record_id_provider=InvalidAllRecordIds(),
        )
        with self.assertRaisesRegex(AdapterError, "invalid_record_id"):
            self.adapter.adapt(
                self.fixture["valid_poll"], context, self.fixture["raw_evidence"], 1
            )

    def test_source_outage_is_one_source_scoped_status(self):
        records = self.adapter.transport_outage(
            self.context,
            "2026-01-15T18:00:02.000Z",
            self.fixture["status_evidence"],
            9,
        )
        self.assertEqual(len(records), 1)
        status = records[0]
        self.assertEqual(status["record_kind"], "status")
        self.assertEqual(status["status"], {"scope": "source", "state": "unreachable"})
        self.assertIsNone(status["metric_id"])
        self.assertNotIn("observation_id", status)
        self.assertIsNone(status["source"]["device"])
        self.assertEqual(status["source"]["transport"], "solarassistant_rest_v1")
        self.assertEqual(status["source"]["lineage"][0]["instance"], "solarassistant")

    def test_malformed_input_rejects_without_echoing_payload(self):
        rejection = self.adapter.adapt(
            ["not", "a", "mapping"],
            self.context,
            self.fixture["raw_evidence"],
            1,
            detection_time="2026-01-15T18:00:02.000Z",
        )[0]
        self.assertEqual(rejection["diagnostics"]["reason_codes"], ["malformed_input"])
        self.assertNotIn("not", json.dumps(rejection))

    def test_input_is_immutable_and_output_is_deterministic(self):
        source = deepcopy(self.fixture["valid_poll"])
        evidence = deepcopy(self.fixture["raw_evidence"])
        original_source = deepcopy(source)
        original_evidence = deepcopy(evidence)
        first = self.adapt(source, evidence)
        second = self.adapt(source, evidence)
        self.assertEqual(first, second)
        self.assertEqual(source, original_source)
        self.assertEqual(evidence, original_evidence)

    def test_adaptation_performs_no_file_database_or_network_io(self):
        source = deepcopy(self.fixture["valid_poll"])
        evidence = deepcopy(self.fixture["raw_evidence"])
        with (
            patch.object(builtins, "open", side_effect=AssertionError("file I/O")),
            patch.object(sqlite3, "connect", side_effect=AssertionError("database I/O")),
            patch("socket.create_connection", side_effect=AssertionError("network I/O")),
        ):
            records = self.adapt(source, evidence)
        self.assertEqual(len(records), 1)


if __name__ == "__main__":
    unittest.main()
