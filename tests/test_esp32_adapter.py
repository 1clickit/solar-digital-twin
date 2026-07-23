import builtins
import json
import sqlite3
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from solar_digital_twin.telemetry import (
    AdapterContext,
    AdapterError,
    Esp32GeneratorFrequencyAdapter,
)
from solar_digital_twin.telemetry.registry import (
    ESP32_FREQUENCY_ENTITY,
    REGISTRY_V1,
)


FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "telemetry"
    / "esp32_generator_frequency.json"
)


class SyntheticObservationIds:
    def __init__(self):
        self.descriptors = []

    def observation_id_for(self, descriptor):
        self.descriptors.append(deepcopy(descriptor))
        return f"test-observation:{descriptor['source_occurrence_id']}"


class SyntheticRecordIds:
    def __init__(self):
        self.descriptors = []

    def record_id_for(self, descriptor):
        self.descriptors.append(deepcopy(descriptor))
        if descriptor["record_kind"] == "observation":
            return "test-record:" + descriptor["evidence"]["record_ref"]
        return f"test-record:rejection:{descriptor['reason_code']}"


class EmptyObservationIds:
    def observation_id_for(self, descriptor):
        return ""


class EmptyObservationRecordIds(SyntheticRecordIds):
    def record_id_for(self, descriptor):
        if descriptor["record_kind"] == "observation":
            return ""
        return super().record_id_for(descriptor)


class EmptyAllRecordIds:
    def record_id_for(self, descriptor):
        return ""


class Esp32GeneratorFrequencyAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def setUp(self):
        self.observation_ids = SyntheticObservationIds()
        self.record_ids = SyntheticRecordIds()
        self.context = AdapterContext(
            registry_version="1",
            producer_name="esp32_frequency_adapter",
            producer_version="test-v1",
            observation_id_provider=self.observation_ids,
            record_id_provider=self.record_ids,
        )
        self.adapter = Esp32GeneratorFrequencyAdapter()

    def adapt(self, record=None, evidence=None, **kwargs):
        return self.adapter.adapt(
            deepcopy(self.fixture["base_record"] if record is None else record),
            kwargs.pop("context", self.context),
            deepcopy(self.fixture["raw_evidence"] if evidence is None else evidence),
            kwargs.pop("ingest_sequence", 7),
            **kwargs,
        )

    def test_registry_contains_exactly_two_immutable_exact_profiles(self):
        self.assertEqual(
            tuple(REGISTRY_V1),
            ("total/battery_state_of_charge", ESP32_FREQUENCY_ENTITY),
        )
        metric = REGISTRY_V1[ESP32_FREQUENCY_ENTITY]
        self.assertEqual(
            (
                metric.metric_id,
                metric.source_system,
                metric.source_device,
                metric.source_role,
                metric.source_transport,
                metric.telemetry_namespace,
            ),
            (
                "esp32.esphome.forensic_probe.generator_frequency",
                "esp32",
                "forensic_probe",
                "forensic",
                "http_sse",
                "esphome",
            ),
        )
        with self.assertRaises(TypeError):
            REGISTRY_V1["other"] = metric

    def test_valid_root_has_exact_identity_lineage_time_and_unit_provenance(self):
        record = self.adapt()[0]
        self.assertEqual(record["record_kind"], "observation")
        self.assertEqual(record["observation"], {"product_kind": "root"})
        self.assertEqual(
            record["metric_id"],
            "esp32.esphome.forensic_probe.generator_frequency",
        )
        self.assertEqual(
            record["source"],
            {
                "system": "esp32",
                "device": "forensic_probe",
                "metric_id": ESP32_FREQUENCY_ENTITY,
                "role": "forensic",
                "transport": "http_sse",
                "lineage": [
                    {
                        "system": "esp32",
                        "instance": "forensic_probe",
                        "role": "root",
                        "reference": ESP32_FREQUENCY_ENTITY,
                        "transformation_id": None,
                        "unresolved": False,
                    }
                ],
            },
        )
        self.assertEqual(record["time"]["source_at"], None)
        self.assertEqual(record["time"]["source_at_raw"], None)
        self.assertEqual(record["time"]["received_at"], "2026-01-15T18:00:01.123Z")
        self.assertEqual(record["time"]["observed_at"], record["time"]["received_at"])
        self.assertEqual(record["time"]["basis"], "solardt_receipt")
        self.assertEqual(record["time"]["precision"], "millisecond")
        self.assertEqual(record["time"]["clock_quality"], "unknown")
        self.assertEqual(record["value"]["raw_unit"], "Hz")
        self.assertEqual(record["value"]["canonical_unit"], "Hz")
        self.assertEqual(record["value"]["raw_unit_basis"], "adapter_specified")
        self.assertEqual(
            record["value"]["raw_unit_mapping"],
            {
                "id": "esp32.esphome.sensor-01_gen_frequency.unit",
                "version": "1",
            },
        )
        self.assertEqual(record["value"]["result_nature"], "source_value")
        self.assertEqual(
            record["transformation"], {"id": None, "version": None, "method": None}
        )

    def test_every_finite_frequency_is_preserved_without_plausibility_logic(self):
        for value in self.fixture["numeric_values"]:
            with self.subTest(value=value):
                source = deepcopy(self.fixture["base_record"])
                source["value"] = value
                source["state"] = f"display:{value}"
                record = self.adapt(source)[0]
                self.assertEqual(record["value"]["raw"], value)
                self.assertEqual(record["value"]["normalized"], value)
                self.assertEqual(record["validity"], "valid")
                self.assertEqual(
                    record["evidence"]["source_fields"]["value"],
                    value,
                )
                self.assertEqual(
                    record["evidence"]["source_fields"]["state"], f"display:{value}"
                )

    def test_raw_value_and_state_are_lossless_and_disagreement_is_not_reconciled(self):
        source = deepcopy(self.fixture["base_record"])
        source["value"] = 5000
        source["state"] = "59.99 Hz"
        record = self.adapt(source)[0]
        self.assertEqual(record["value"]["raw"], 5000)
        self.assertEqual(record["value"]["normalized"], 5000)
        self.assertEqual(record["evidence"]["source_fields"]["value"], 5000)
        self.assertEqual(record["evidence"]["source_fields"]["state"], "59.99 Hz")
        self.assertEqual(record["evidence"]["source_fields"]["id"], source["id"])
        self.assertEqual(record["evidence"]["source_fields"]["name"], source["name"])
        self.assertEqual(
            record["evidence"]["source_fields"]["domain"], source["domain"]
        )
        self.assertEqual(
            record["evidence"]["source_fields"]["source_url"], source["source_url"]
        )

    def test_null_unknown_and_unavailable_remain_distinct(self):
        expected = (
            ("null", "unknown", "explicit_null"),
            ("string", "unknown", "source_unknown"),
            ("string", "unavailable", "source_unavailable"),
        )
        for source_state, (raw_type, availability, reason) in zip(
            self.fixture["states"], expected
        ):
            source = deepcopy(self.fixture["base_record"])
            source.update(source_state)
            record = self.adapt(source)[0]
            self.assertEqual(record["value"]["raw"], source_state["value"])
            self.assertEqual(record["value"]["raw_type"], raw_type)
            self.assertIsNone(record["value"]["normalized"])
            self.assertEqual(record["availability"], availability)
            self.assertEqual(record["diagnostics"]["reason_codes"], [reason])
            self.assertEqual(
                record["evidence"]["source_fields"]["value"], source_state["value"]
            )
            self.assertEqual(
                record["evidence"]["source_fields"]["state"], source_state["state"]
            )

    def test_distinct_occurrences_with_equal_timestamps_do_not_collapse(self):
        first = self.adapt()[0]
        source = deepcopy(self.fixture["base_record"])
        source["source_occurrence_id"] = "synthetic-esp32-occurrence-002"
        evidence = deepcopy(self.fixture["raw_evidence"])
        evidence["source_occurrence_id"] = source["source_occurrence_id"]
        evidence["record_ref"] = "synthetic-raw-record-002"
        second = self.adapt(source, evidence, ingest_sequence=8)[0]
        self.assertEqual(first["time"]["received_at"], second["time"]["received_at"])
        self.assertNotEqual(first["observation_id"], second["observation_id"])
        self.assertNotEqual(first["sequence"]["ingest"], second["sequence"]["ingest"])

    def test_raw_current_and_conservative_copies_share_observation_not_record(self):
        copies = [
            self.adapt()[0],
            self.adapt(
                evidence=self.fixture["current_retained_evidence"],
                retention_stream="retained",
                retention_policy_id="esp32-frequency-v1",
            )[0],
            self.adapt(
                evidence=self.fixture["conservative_retained_evidence"],
                retention_stream="retained",
                retention_policy_id="esp32-conservative-v1",
            )[0],
        ]
        self.assertEqual(len({item["observation_id"] for item in copies}), 1)
        self.assertEqual(len({item["record_id"] for item in copies}), 3)
        self.assertEqual(
            [item["retention"]["policy_id"] for item in copies],
            [None, "esp32-frequency-v1", "esp32-conservative-v1"],
        )
        observation_descriptors = self.observation_ids.descriptors[-3:]
        self.assertEqual(
            observation_descriptors,
            [observation_descriptors[0]] * 3,
        )
        for descriptor in observation_descriptors:
            self.assertNotIn("retention", descriptor)
            self.assertNotIn("evidence", descriptor)
        for descriptor, copy in zip(self.record_ids.descriptors[-3:], copies):
            self.assertEqual(descriptor["observation_id"], copy["observation_id"])
            self.assertEqual(descriptor["retention"], copy["retention"])
            self.assertEqual(descriptor["evidence"], copy["evidence"])

    def test_rejections_are_bounded_payload_free_and_distinct(self):
        cases = []
        source = deepcopy(self.fixture["base_record"])
        del source["value"]
        cases.append((source, self.fixture["raw_evidence"], {}, "missing_value"))
        source = deepcopy(self.fixture["base_record"])
        del source["state"]
        cases.append((source, self.fixture["raw_evidence"], {}, "missing_state"))
        for value, reason in (
            (True, "invalid_numeric_boolean"),
            ("60", "unsupported_value"),
            (float("nan"), "invalid_numeric_non_finite"),
            (float("inf"), "invalid_numeric_non_finite"),
            (float("-inf"), "invalid_numeric_non_finite"),
        ):
            source = deepcopy(self.fixture["base_record"])
            source["value"] = value
            cases.append((source, self.fixture["raw_evidence"], {}, reason))
        source = deepcopy(self.fixture["base_record"])
        source["id"] = "sensor-01_other"
        cases.append((source, self.fixture["raw_evidence"], {}, "unapproved_entity"))
        source = deepcopy(self.fixture["base_record"])
        source["domain"] = "binary_sensor"
        cases.append((source, self.fixture["raw_evidence"], {}, "invalid_domain"))
        source = deepcopy(self.fixture["base_record"])
        source["received_at_utc"] = "bad-time"
        cases.append(
            (
                source,
                self.fixture["raw_evidence"],
                {"detection_time": "2026-01-15T18:00:02.000Z"},
                "invalid_receipt_time",
            )
        )
        cases.append(
            (
                self.fixture["base_record"],
                {"synthetic": True},
                {},
                "invalid_evidence",
            )
        )
        cases.append(
            (
                self.fixture["base_record"],
                self.fixture["raw_evidence"],
                {"retention_stream": "retained"},
                "invalid_retention",
            )
        )
        cases.append(
            (
                self.fixture["base_record"],
                self.fixture["raw_evidence"],
                {"ingest_sequence": -1},
                "invalid_ingest_sequence",
            )
        )
        for source, evidence, kwargs, reason in cases:
            with self.subTest(reason=reason):
                rejection = self.adapt(source, evidence, **kwargs)[0]
                self.assertEqual(rejection["record_kind"], "rejection")
                self.assertEqual(rejection["diagnostics"]["reason_codes"], [reason])
                diagnostics = json.dumps(rejection["diagnostics"])
                self.assertNotIn("sensor-01", diagnostics)
                self.assertNotIn("synthetic.invalid", diagnostics)

        malformed = self.adapter.adapt(
            ["payload"],
            self.context,
            self.fixture["raw_evidence"],
            1,
            detection_time="2026-01-15T18:00:02.000Z",
        )[0]
        self.assertEqual(malformed["diagnostics"]["reason_codes"], ["malformed_input"])
        self.assertNotIn("payload", json.dumps(malformed))

    def test_registry_version_and_injected_ids_fail_safely(self):
        future = AdapterContext(
            registry_version="future",
            producer_name="esp32_frequency_adapter",
            producer_version="test-v1",
            observation_id_provider=self.observation_ids,
            record_id_provider=self.record_ids,
        )
        self.assertEqual(
            self.adapt(context=future)[0]["diagnostics"]["reason_codes"],
            ["registry_mismatch"],
        )
        invalid_observation = AdapterContext(
            registry_version="1",
            producer_name="esp32_frequency_adapter",
            producer_version="test-v1",
            observation_id_provider=EmptyObservationIds(),
            record_id_provider=SyntheticRecordIds(),
        )
        self.assertEqual(
            self.adapt(context=invalid_observation)[0]["diagnostics"]["reason_codes"],
            ["invalid_observation_id"],
        )
        invalid_record = AdapterContext(
            registry_version="1",
            producer_name="esp32_frequency_adapter",
            producer_version="test-v1",
            observation_id_provider=SyntheticObservationIds(),
            record_id_provider=EmptyObservationRecordIds(),
        )
        self.assertEqual(
            self.adapt(context=invalid_record)[0]["diagnostics"]["reason_codes"],
            ["invalid_record_id"],
        )
        invalid_all = AdapterContext(
            registry_version="1",
            producer_name="esp32_frequency_adapter",
            producer_version="test-v1",
            observation_id_provider=SyntheticObservationIds(),
            record_id_provider=EmptyAllRecordIds(),
        )
        with self.assertRaisesRegex(AdapterError, "invalid_record_id"):
            self.adapt(context=invalid_all)

    def test_input_context_evidence_are_unchanged_and_output_detached(self):
        source = deepcopy(self.fixture["base_record"])
        evidence = deepcopy(self.fixture["raw_evidence"])
        context = self.context
        originals = (deepcopy(source), deepcopy(evidence), context)
        first = self.adapt(source, evidence)[0]
        second = self.adapt(source, evidence)[0]
        self.assertEqual(first, second)
        self.assertEqual((source, evidence, context), originals)
        first["evidence"]["source_fields"]["state"] = "changed"
        self.assertEqual(source["state"], "60.01 Hz")
        json.dumps(second, allow_nan=False)

    def test_import_and_adaptation_perform_no_operational_io(self):
        source = deepcopy(self.fixture["base_record"])
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
