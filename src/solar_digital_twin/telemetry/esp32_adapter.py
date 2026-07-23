"""I/O-free adapter for synthetic ESP32 generator-frequency SSE records."""

from __future__ import annotations

import json
import math
from copy import deepcopy
from datetime import datetime
from typing import Any, Mapping

from solar_digital_twin.telemetry.adapters import AdapterContext, AdapterError
from solar_digital_twin.telemetry.model import CONTRACT_VERSION, LineageHop, validate_record
from solar_digital_twin.telemetry.registry import (
    ESP32_FREQUENCY_ENTITY,
    REGISTRY_VERSION,
    MetricDefinition,
    metric_for,
)


REASON_CODES = frozenset(
    {
        "explicit_null",
        "invalid_contract_version",
        "invalid_domain",
        "invalid_evidence",
        "invalid_ingest_sequence",
        "invalid_numeric_boolean",
        "invalid_numeric_non_finite",
        "invalid_observation_id",
        "invalid_receipt_time",
        "invalid_record_id",
        "invalid_retention",
        "malformed_input",
        "missing_state",
        "missing_value",
        "registry_mismatch",
        "source_unavailable",
        "source_unknown",
        "unapproved_entity",
        "unsupported_value",
    }
)


def _valid_id(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_utc_millisecond(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 24 or not value.endswith("Z"):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return False
    return len(value.rsplit(".", 1)[-1][:-1]) == 3


def _valid_sequence(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value >= 0


def _json_compatible(value: Any) -> bool:
    try:
        json.dumps(value, allow_nan=False, separators=(",", ":"))
    except (TypeError, ValueError):
        return False
    return True


def _valid_evidence(value: Any, occurrence_id: Any) -> bool:
    if not isinstance(value, Mapping) or value.get("synthetic") is not True:
        return False
    required_ids = (
        "capture_id",
        "manifest_ref",
        "file_ref",
        "record_ref",
        "source_occurrence_id",
    )
    if any(not _valid_id(value.get(field)) for field in required_ids):
        return False
    if value.get("source_occurrence_id") != occurrence_id:
        return False
    return _json_compatible(value)


def _lineage(reference: str) -> list[dict[str, Any]]:
    return [
        LineageHop(
            system="esp32",
            instance="forensic_probe",
            role="root",
            reference=reference,
        ).as_mapping()
    ]


def _time(received_at: str, basis: str) -> dict[str, Any]:
    return {
        "source_at": None,
        "source_at_raw": None,
        "source_changed_at": None,
        "received_at": received_at,
        "observed_at": received_at,
        "basis": basis,
        "source_timezone": None,
        "precision": "millisecond",
        "clock_quality": "unknown",
        "uncertainty_ms": None,
    }


class Esp32GeneratorFrequencyAdapter:
    """Adapt only the approved ESPHome generator-frequency entity."""

    def adapt(
        self,
        input_record: Mapping[str, Any],
        context: AdapterContext,
        evidence_reference: Mapping[str, Any],
        ingest_sequence: int,
        *,
        retention_stream: str = "raw",
        retention_policy_id: str | None = None,
        detection_time: str | None = None,
    ) -> tuple[dict[str, Any], ...]:
        self._validate_context(context)
        received_candidate = (
            input_record.get("received_at_utc")
            if isinstance(input_record, Mapping)
            else None
        )
        detected_at = detection_time or received_candidate
        if not _valid_utc_millisecond(detected_at):
            raise AdapterError("invalid_detection_time")

        reason = self._input_reason(
            input_record,
            context,
            evidence_reference,
            ingest_sequence,
            retention_stream,
            retention_policy_id,
        )
        if reason is not None:
            return (
                self._rejection(
                    context,
                    reason,
                    detected_at,
                    evidence_reference,
                    ingest_sequence,
                ),
            )

        assert isinstance(input_record, Mapping)
        metric = metric_for(context.registry_version, input_record["id"])
        assert metric is not None
        observation_descriptor = {
            "contract_version": context.contract_version,
            "registry_version": context.registry_version,
            "source_system": metric.source_system,
            "telemetry_namespace": metric.telemetry_namespace,
            "source_device": metric.source_device,
            "source_metric_id": metric.native_metric_id,
            "metric_id": metric.metric_id,
            "transport": metric.source_transport,
            "source_occurrence_id": input_record["source_occurrence_id"],
            "observed_at": input_record["received_at_utc"],
            "ingest_sequence": ingest_sequence,
        }
        observation_id = context.observation_id_provider.observation_id_for(
            deepcopy(observation_descriptor)
        )
        if not _valid_id(observation_id):
            return (
                self._rejection(
                    context,
                    "invalid_observation_id",
                    detected_at,
                    evidence_reference,
                    ingest_sequence,
                ),
            )

        output_evidence = deepcopy(dict(evidence_reference))
        output_evidence["source_fields"] = {
            "id": deepcopy(input_record["id"]),
            "name": deepcopy(input_record["name"]),
            "domain": deepcopy(input_record["domain"]),
            "value": deepcopy(input_record["value"]),
            "state": deepcopy(input_record["state"]),
            "source_url": deepcopy(input_record["source_url"]),
        }
        record_descriptor = {
            "record_kind": "observation",
            "observation_id": observation_id,
            "product_kind": "root",
            "producer": {
                "name": context.producer_name,
                "version": context.producer_version,
            },
            "retention": {
                "stream": retention_stream,
                "policy_id": retention_policy_id,
            },
            "evidence": deepcopy(output_evidence),
        }
        record_id = context.record_id_provider.record_id_for(deepcopy(record_descriptor))
        if not _valid_id(record_id):
            return (
                self._rejection(
                    context,
                    "invalid_record_id",
                    detected_at,
                    evidence_reference,
                    ingest_sequence,
                ),
            )
        record = self._root_record(
            input_record,
            context,
            metric,
            observation_id,
            record_id,
            output_evidence,
            ingest_sequence,
            retention_stream,
            retention_policy_id,
        )
        return (validate_record(record),)

    @staticmethod
    def _validate_context(context: AdapterContext) -> None:
        if context.contract_version != CONTRACT_VERSION:
            raise AdapterError("invalid_contract_version")
        if not _valid_id(context.producer_name) or not _valid_id(context.producer_version):
            raise AdapterError("invalid_producer")
        if not hasattr(context.observation_id_provider, "observation_id_for"):
            raise AdapterError("invalid_observation_id_provider")
        if not hasattr(context.record_id_provider, "record_id_for"):
            raise AdapterError("invalid_record_id_provider")

    @staticmethod
    def _input_reason(
        input_record: Any,
        context: AdapterContext,
        evidence_reference: Any,
        ingest_sequence: Any,
        retention_stream: Any,
        retention_policy_id: Any,
    ) -> str | None:
        if not isinstance(input_record, Mapping):
            return "malformed_input"
        if context.registry_version != REGISTRY_VERSION:
            return "registry_mismatch"
        if not _valid_sequence(ingest_sequence):
            return "invalid_ingest_sequence"
        if retention_stream not in {"raw", "retained"}:
            return "invalid_retention"
        if retention_stream == "raw" and retention_policy_id is not None:
            return "invalid_retention"
        if retention_stream == "retained" and not _valid_id(retention_policy_id):
            return "invalid_retention"
        if not _valid_utc_millisecond(input_record.get("received_at_utc")):
            return "invalid_receipt_time"
        if not _valid_id(input_record.get("source_occurrence_id")):
            return "invalid_evidence"
        if not _valid_evidence(
            evidence_reference, input_record.get("source_occurrence_id")
        ):
            return "invalid_evidence"
        if "name" not in input_record or not isinstance(input_record["name"], str):
            return "malformed_input"
        if input_record.get("source_url") != "http://synthetic.invalid/events":
            return "invalid_evidence"
        if input_record.get("id") != ESP32_FREQUENCY_ENTITY:
            return "unapproved_entity"
        if input_record.get("domain") != "sensor":
            return "invalid_domain"
        if metric_for(context.registry_version, input_record.get("id")) is None:
            return "registry_mismatch"
        if "value" not in input_record:
            return "missing_value"
        if "state" not in input_record:
            return "missing_state"
        value = input_record["value"]
        if isinstance(value, bool):
            return "invalid_numeric_boolean"
        if value is not None and not (
            isinstance(value, str) and value in {"unknown", "unavailable"}
        ) and not isinstance(value, (int, float)):
            return "unsupported_value"
        if isinstance(value, (int, float)) and not math.isfinite(value):
            return "invalid_numeric_non_finite"
        if input_record["state"] is not None and not isinstance(
            input_record["state"], str
        ):
            return "unsupported_value"
        return None

    @staticmethod
    def _root_record(
        input_record: Mapping[str, Any],
        context: AdapterContext,
        metric: MetricDefinition,
        observation_id: str,
        record_id: str,
        evidence: Mapping[str, Any],
        ingest_sequence: int,
        retention_stream: str,
        retention_policy_id: str | None,
    ) -> dict[str, Any]:
        value = input_record["value"]
        if value is None:
            raw_type = "null"
            normalized = None
            source_nature = "state"
            availability = "unknown"
            state_reason = "explicit_null"
        elif isinstance(value, str):
            raw_type = "string"
            normalized = None
            source_nature = "state"
            availability = value
            state_reason = f"source_{value}"
        else:
            raw_type = "number"
            normalized = value
            source_nature = metric.source_nature
            availability = "available"
            state_reason = None
        return {
            "contract_version": CONTRACT_VERSION,
            "record_kind": "observation",
            "observation": {"product_kind": "root"},
            "record_id": record_id,
            "observation_id": observation_id,
            "metric_id": metric.metric_id,
            "source": {
                "system": metric.source_system,
                "device": metric.source_device,
                "metric_id": metric.native_metric_id,
                "role": metric.source_role,
                "transport": metric.source_transport,
                "lineage": _lineage(metric.native_metric_id),
            },
            "time": _time(input_record["received_at_utc"], "solardt_receipt"),
            "sequence": {"ingest": ingest_sequence, "source": None},
            "value": {
                "raw_present": True,
                "raw": deepcopy(value),
                "raw_type": raw_type,
                "normalized": deepcopy(normalized),
                "raw_unit": metric.raw_unit,
                "canonical_unit": metric.raw_unit,
                "source_nature": source_nature,
                "result_nature": metric.result_nature,
                "raw_unit_basis": metric.raw_unit_basis,
                "raw_unit_mapping": {
                    "id": metric.raw_unit_mapping_id,
                    "version": metric.raw_unit_mapping_version,
                },
            },
            "availability": availability,
            "validity": "valid",
            "capability": "supported",
            "quality": {
                "categories": ["direct", "clock_uncertain"],
                "reasons": [
                    "source_time_absent",
                    *([state_reason] if state_reason is not None else []),
                ],
            },
            "transformation": {"id": None, "version": None, "method": None},
            "parents": [],
            "producer": {
                "name": context.producer_name,
                "version": context.producer_version,
            },
            "evidence": deepcopy(dict(evidence)),
            "retention": {
                "stream": retention_stream,
                "policy_id": retention_policy_id,
            },
            "diagnostics": {
                "reason_codes": [] if state_reason is None else [state_reason]
            },
        }

    def _rejection(
        self,
        context: AdapterContext,
        reason: str,
        detected_at: str,
        evidence_reference: Any,
        ingest_sequence: Any,
    ) -> dict[str, Any]:
        if reason not in REASON_CODES:
            raise AdapterError("unsupported_rejection_reason")
        sequence = ingest_sequence if _valid_sequence(ingest_sequence) else 0
        evidence = (
            deepcopy(dict(evidence_reference))
            if isinstance(evidence_reference, Mapping)
            and evidence_reference.get("synthetic") is True
            and _json_compatible(evidence_reference)
            else None
        )
        descriptor = {
            "record_kind": "rejection",
            "reason_code": reason,
            "source_system": "esp32",
            "detected_at": detected_at,
            "producer": {
                "name": context.producer_name,
                "version": context.producer_version,
            },
            "evidence": evidence,
        }
        record_id = context.record_id_provider.record_id_for(deepcopy(descriptor))
        if not _valid_id(record_id):
            raise AdapterError("invalid_record_id")
        record = {
            "contract_version": CONTRACT_VERSION,
            "record_kind": "rejection",
            "record_id": record_id,
            "metric_id": None,
            "source": {
                "system": "esp32",
                "device": None,
                "metric_id": None,
                "role": "operational",
                "transport": "http_sse",
                "lineage": _lineage(ESP32_FREQUENCY_ENTITY),
            },
            "time": _time(detected_at, "status_detection"),
            "sequence": {"ingest": sequence, "source": None},
            "validity": "rejected",
            "producer": {
                "name": context.producer_name,
                "version": context.producer_version,
            },
            "evidence": evidence,
            "diagnostics": {"reason_codes": [reason]},
        }
        return validate_record(record)
