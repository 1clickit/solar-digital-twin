"""I/O-free adapter for synthetic SolarAssistant combined-SOC records."""

from __future__ import annotations

import json
import math
from copy import deepcopy
from datetime import datetime
from typing import Any, Mapping

from solar_digital_twin.telemetry.adapters import AdapterContext, AdapterError
from solar_digital_twin.telemetry.model import (
    CONTRACT_VERSION,
    LineageHop,
    validate_record,
)
from solar_digital_twin.telemetry.registry import (
    COMBINED_SOC_TOPIC,
    REGISTRY_VERSION,
    MetricDefinition,
    metric_for,
)


REASON_CODES = frozenset(
    {
        "explicit_null",
        "invalid_contract_version",
        "invalid_evidence",
        "invalid_ingest_sequence",
        "invalid_numeric_boolean",
        "invalid_numeric_non_finite",
        "invalid_numeric_range",
        "invalid_observation_id",
        "invalid_poll_group",
        "invalid_receipt_time",
        "invalid_record_id",
        "invalid_retention",
        "malformed_input",
        "missing_unit",
        "missing_value",
        "registry_mismatch",
        "source_unavailable",
        "source_unknown",
        "unit_mismatch",
        "unapproved_topic",
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


def _valid_evidence(value: Any) -> bool:
    if not isinstance(value, Mapping) or value.get("synthetic") is not True:
        return False
    if not _valid_id(value.get("capture_id")) or not _valid_id(value.get("record_ref")):
        return False
    return _json_compatible(value)


def _lineage(reference: str) -> list[dict[str, Any]]:
    return [
        LineageHop(
            system="solarassistant",
            instance="jk_bms_bank",
            role="root",
            reference=reference,
        ).as_mapping()
    ]


def _source_lineage() -> list[dict[str, Any]]:
    return [
        LineageHop(
            system="solarassistant",
            instance="solarassistant",
            role="root",
            reference="solarassistant_rest_v1",
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


class SolarAssistantSocAdapter:
    """Adapt only SolarAssistant-reported combined battery SOC."""

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
        """Return exactly one root observation or one bounded rejection."""
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
                    input_record,
                ),
            )

        assert isinstance(input_record, Mapping)
        metric = metric_for(context.registry_version, input_record["topic"])
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
            "poll_group_id": input_record["poll_group_id"],
            "observed_at": input_record["received_at_utc"],
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
                    input_record,
                ),
            )

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
            "evidence": deepcopy(dict(evidence_reference)),
        }
        record_id = context.record_id_provider.record_id_for(
            deepcopy(record_descriptor)
        )
        if not _valid_id(record_id):
            return (
                self._rejection(
                    context,
                    "invalid_record_id",
                    detected_at,
                    evidence_reference,
                    ingest_sequence,
                    input_record,
                ),
            )

        record = self._root_record(
            input_record,
            context,
            metric,
            observation_id,
            record_id,
            evidence_reference,
            ingest_sequence,
            retention_stream,
            retention_policy_id,
        )
        return (validate_record(record),)

    def transport_outage(
        self,
        context: AdapterContext,
        detected_at: str,
        evidence_reference: Mapping[str, Any],
        ingest_sequence: int,
    ) -> tuple[dict[str, Any], ...]:
        """Return one source-scoped SolarAssistant REST outage status."""
        self._validate_context(context)
        if not _valid_utc_millisecond(detected_at):
            raise AdapterError("invalid_detection_time")
        if not _valid_sequence(ingest_sequence):
            raise AdapterError("invalid_ingest_sequence")
        if not _valid_evidence(evidence_reference):
            raise AdapterError("invalid_evidence")
        descriptor = {
            "record_kind": "status",
            "scope": "source",
            "state": "unreachable",
            "source_system": "solarassistant",
            "transport": "solarassistant_rest_v1",
            "detected_at": detected_at,
            "evidence": deepcopy(dict(evidence_reference)),
        }
        record_id = context.record_id_provider.record_id_for(deepcopy(descriptor))
        if not _valid_id(record_id):
            raise AdapterError("invalid_record_id")
        record = {
            "contract_version": CONTRACT_VERSION,
            "record_kind": "status",
            "record_id": record_id,
            "metric_id": None,
            "status": {"scope": "source", "state": "unreachable"},
            "source": {
                "system": "solarassistant",
                "device": None,
                "metric_id": None,
                "role": "operational",
                "transport": "solarassistant_rest_v1",
                "lineage": _source_lineage(),
            },
            "time": _time(detected_at, "status_detection"),
            "sequence": {"ingest": ingest_sequence, "source": None},
            "producer": {
                "name": context.producer_name,
                "version": context.producer_version,
            },
            "evidence": deepcopy(dict(evidence_reference)),
            "diagnostics": {"reason_codes": ["source_transport_unreachable"]},
        }
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
        if not _valid_evidence(evidence_reference):
            return "invalid_evidence"
        if retention_stream not in {"raw", "retained"}:
            return "invalid_retention"
        if retention_stream == "raw" and retention_policy_id is not None:
            return "invalid_retention"
        if retention_stream == "retained" and not _valid_id(retention_policy_id):
            return "invalid_retention"
        if not _valid_utc_millisecond(input_record.get("received_at_utc")):
            return "invalid_receipt_time"
        if not _valid_id(input_record.get("poll_group_id")):
            return "invalid_poll_group"
        if evidence_reference.get("poll_group_id") != input_record.get("poll_group_id"):
            return "invalid_evidence"
        topic = input_record.get("topic")
        if topic != COMBINED_SOC_TOPIC:
            return "unapproved_topic"
        if metric_for(context.registry_version, topic) is None:
            return "registry_mismatch"
        if "value" not in input_record:
            return "missing_value"
        value = input_record["value"]
        if isinstance(value, bool):
            return "invalid_numeric_boolean"
        if value is not None and not (
            isinstance(value, str) and value in {"unknown", "unavailable"}
        ) and not isinstance(value, (int, float)):
            return "unsupported_value"
        if isinstance(value, (int, float)) and not math.isfinite(value):
            return "invalid_numeric_non_finite"
        if isinstance(value, (int, float)) and not 0 <= value <= 100:
            return "invalid_numeric_range"
        if "unit" not in input_record or input_record.get("unit") in (None, ""):
            return "missing_unit"
        if input_record.get("unit") != "%":
            return "unit_mismatch"
        return None

    @staticmethod
    def _root_record(
        input_record: Mapping[str, Any],
        context: AdapterContext,
        metric: MetricDefinition,
        observation_id: str,
        record_id: str,
        evidence_reference: Mapping[str, Any],
        ingest_sequence: int,
        retention_stream: str,
        retention_policy_id: str | None,
    ) -> dict[str, Any]:
        received_at = input_record["received_at_utc"]
        value = input_record["value"]
        if value is None:
            raw_type = "null"
            normalized = None
            source_nature = "state"
            availability = "unknown"
            state_reason = "explicit_null"
        elif isinstance(value, str) and value in {"unknown", "unavailable"}:
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
            "time": _time(received_at, "solardt_receipt"),
            "sequence": {"ingest": ingest_sequence, "source": None},
            "value": {
                "raw_present": True,
                "raw": value,
                "raw_type": raw_type,
                "normalized": normalized,
                "raw_unit": metric.raw_unit,
                "canonical_unit": metric.raw_unit,
                "source_nature": source_nature,
                "result_nature": metric.result_nature,
                "raw_unit_basis": metric.raw_unit_basis,
                "raw_unit_mapping": None,
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
            "evidence": deepcopy(dict(evidence_reference)),
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
        input_record: Any,
    ) -> dict[str, Any]:
        if reason not in REASON_CODES:
            raise AdapterError("unsupported_rejection_reason")
        sequence = ingest_sequence if _valid_sequence(ingest_sequence) else 0
        evidence = (
            deepcopy(dict(evidence_reference))
            if _valid_evidence(evidence_reference)
            else None
        )
        topic = input_record.get("topic") if isinstance(input_record, Mapping) else None
        known_metric = topic == COMBINED_SOC_TOPIC
        descriptor = {
            "record_kind": "rejection",
            "reason_code": reason,
            "detected_at": detected_at,
            "sequence": sequence,
            "source_metric_id": topic if known_metric else None,
            "evidence": evidence,
        }
        record_id = context.record_id_provider.record_id_for(deepcopy(descriptor))
        if not _valid_id(record_id):
            raise AdapterError("invalid_record_id")
        record = {
            "contract_version": CONTRACT_VERSION,
            "record_kind": "rejection",
            "record_id": record_id,
            "metric_id": (
                "solarassistant.jk_bms.combined.state_of_charge"
                if known_metric
                else None
            ),
            "source": {
                "system": "solarassistant",
                "device": "jk_bms_bank" if known_metric else None,
                "metric_id": topic if known_metric else None,
                "role": "operational",
                "transport": "solarassistant_rest_v1",
                "lineage": _lineage(topic) if known_metric else _source_lineage(),
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
