"""Minimal validator for the implemented canonical telemetry profiles."""

from __future__ import annotations

import json
import math
import re
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from solar_digital_twin.telemetry.registry import (
    ESP32_FREQUENCY_ENTITY,
    REGISTRY_VERSION,
    metric_for,
)

CONTRACT_VERSION = "solar-digital-twin.telemetry-observation.v1"
SUPPORTED_RECORD_KINDS = frozenset({"observation", "status", "rejection"})
SUPPORTED_PRODUCT_KINDS = frozenset({"root"})
SUPPORTED_TIME_BASES = frozenset({"solardt_receipt", "status_detection"})
SUPPORTED_RETENTION_STREAMS = frozenset({"raw", "retained"})
UTC_MILLISECOND_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"
)


@dataclass(frozen=True)
class LineageHop:
    """Immutable lineage construction with JSON-compatible output."""

    system: str
    instance: str
    role: str
    reference: str
    transformation_id: str | None = None
    unresolved: bool = False

    def as_mapping(self) -> dict[str, Any]:
        return {
            "system": self.system,
            "instance": self.instance,
            "role": self.role,
            "reference": self.reference,
            "transformation_id": self.transformation_id,
            "unresolved": self.unresolved,
        }


class ContractValidationError(ValueError):
    """Bounded validation failure containing only a stable reason code."""

    def __init__(self, reason_code: str):
        super().__init__(reason_code)
        self.reason_code = reason_code


def _fail(reason_code: str) -> None:
    raise ContractValidationError(reason_code)


def _mapping(value: Any, reason_code: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail(reason_code)
    return value


def _require_fields(
    mapping: Mapping[str, Any], fields: tuple[str, ...], reason_code: str
) -> None:
    if any(field not in mapping for field in fields):
        _fail(reason_code)


def _prohibit_fields(
    mapping: Mapping[str, Any], fields: tuple[str, ...], reason_code: str
) -> None:
    if any(field in mapping for field in fields):
        _fail(reason_code)


def _nonempty_string(value: Any, reason_code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(reason_code)
    return value


def _nonnegative_integer(value: Any, reason_code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        _fail(reason_code)
    return value


def _utc_timestamp(value: Any, reason_code: str) -> str:
    text = _nonempty_string(value, reason_code)
    if not UTC_MILLISECOND_PATTERN.fullmatch(text):
        _fail(reason_code)
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00")
    except ValueError:
        _fail(reason_code)
    if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        _fail(reason_code)
    return text


def _common(record: Mapping[str, Any]) -> tuple[str, Mapping[str, Any]]:
    _require_fields(
        record,
        (
            "contract_version",
            "record_kind",
            "record_id",
            "source",
            "time",
            "sequence",
            "producer",
            "evidence",
            "diagnostics",
        ),
        "incomplete_record_profile",
    )
    if record.get("contract_version") != CONTRACT_VERSION:
        _fail("unsupported_contract_version")
    kind = record.get("record_kind")
    if not isinstance(kind, str) or kind not in SUPPORTED_RECORD_KINDS:
        _fail("unsupported_record_kind")
    _nonempty_string(record.get("record_id"), "invalid_record_id")
    source = _mapping(record.get("source"), "invalid_source")
    _nonempty_string(source.get("system"), "invalid_source_system")
    lineage = source.get("lineage")
    if not isinstance(lineage, list) or not lineage:
        _fail("invalid_lineage")
    for hop in lineage:
        hop_map = _mapping(hop, "invalid_lineage")
        _nonempty_string(hop_map.get("system"), "invalid_lineage")
        _nonempty_string(hop_map.get("role"), "invalid_lineage")
        if not isinstance(hop_map.get("unresolved"), bool):
            _fail("invalid_lineage")

    time = _mapping(record.get("time"), "invalid_time")
    received = _utc_timestamp(time.get("received_at"), "invalid_received_at")
    observed = _utc_timestamp(time.get("observed_at"), "invalid_observed_at")
    basis = time.get("basis")
    if not isinstance(basis, str) or basis not in SUPPORTED_TIME_BASES:
        _fail("unsupported_time_basis")
    _nonnegative_integer(
        _mapping(record.get("sequence"), "invalid_sequence").get("ingest"),
        "invalid_ingest_sequence",
    )
    producer = _mapping(record.get("producer"), "invalid_producer")
    _nonempty_string(producer.get("name"), "invalid_producer")
    _nonempty_string(producer.get("version"), "invalid_producer")
    if "evidence" not in record:
        _fail("missing_evidence")
    diagnostics = _mapping(record.get("diagnostics"), "invalid_diagnostics")
    reasons = diagnostics.get("reason_codes")
    if not isinstance(reasons, list) or any(
        not isinstance(reason, str) or not reason for reason in reasons
    ):
        _fail("invalid_diagnostics")
    return kind, {"received_at": received, "observed_at": observed}


def _validate_root(record: Mapping[str, Any]) -> None:
    _require_fields(
        record,
        (
            "observation",
            "observation_id",
            "metric_id",
            "value",
            "availability",
            "validity",
            "capability",
            "quality",
            "transformation",
            "parents",
            "retention",
        ),
        "incomplete_root_profile",
    )
    _prohibit_fields(record, ("status",), "invalid_root_profile")
    observation = _mapping(record.get("observation"), "invalid_observation_profile")
    product_kind = observation.get("product_kind")
    if not isinstance(product_kind, str) or product_kind not in SUPPORTED_PRODUCT_KINDS:
        _fail("unsupported_product_kind")
    _nonempty_string(record.get("observation_id"), "invalid_observation_id")
    _nonempty_string(record.get("metric_id"), "invalid_metric_id")
    source = _mapping(record["source"], "invalid_source")
    _require_fields(
        source,
        ("system", "device", "metric_id", "role", "transport", "lineage"),
        "incomplete_root_source",
    )
    for field in ("device", "metric_id", "role", "transport"):
        _nonempty_string(source.get(field), f"invalid_source_{field}")
    metric = metric_for(REGISTRY_VERSION, source.get("metric_id"))
    if metric is None:
        _fail("invalid_source_metric_id")
    if source.get("system") != metric.source_system:
        _fail("invalid_source_system")
    if source.get("device") != metric.source_device:
        _fail("invalid_source_device")
    if source.get("role") != metric.source_role:
        _fail("invalid_source_role")
    if source.get("transport") != metric.source_transport:
        _fail("invalid_source_transport")
    if record.get("metric_id") != metric.metric_id:
        _fail("invalid_metric_id")
    if source.get("lineage") != [
        {
            "system": metric.source_system,
            "instance": metric.source_device,
            "role": "root",
            "reference": metric.native_metric_id,
            "transformation_id": None,
            "unresolved": False,
        }
    ]:
        _fail("invalid_lineage")

    time = _mapping(record["time"], "invalid_time")
    _require_fields(
        time,
        (
            "source_at",
            "source_at_raw",
            "received_at",
            "observed_at",
            "basis",
            "source_timezone",
            "precision",
            "clock_quality",
            "uncertainty_ms",
        ),
        "incomplete_root_time",
    )
    if time.get("source_at") is not None or time.get("source_at_raw") is not None:
        _fail("unexpected_source_time")
    if time.get("basis") != "solardt_receipt":
        _fail("invalid_observation_time_basis")
    if time.get("received_at") != time.get("observed_at"):
        _fail("receipt_observation_time_mismatch")
    if time.get("source_timezone") is not None:
        _fail("unexpected_source_timezone")
    if any(
        field in time
        for field in ("derived_at", "window_start", "window_end", "anchor_at")
    ):
        _fail("unexpected_derived_time")
    if time.get("precision") != "millisecond":
        _fail("invalid_time_precision")
    clock_quality = time.get("clock_quality")
    if not isinstance(clock_quality, str) or clock_quality not in {
        "synchronized",
        "unknown",
    }:
        _fail("unsupported_clock_quality")
    if time.get("uncertainty_ms") is not None:
        uncertainty = time.get("uncertainty_ms")
        if (
            isinstance(uncertainty, bool)
            or not isinstance(uncertainty, (int, float))
            or not math.isfinite(uncertainty)
            or uncertainty < 0
        ):
            _fail("invalid_time_uncertainty")

    value = _mapping(record.get("value"), "invalid_value")
    _require_fields(
        value,
        (
            "raw_present",
            "raw",
            "raw_type",
            "normalized",
            "raw_unit",
            "canonical_unit",
            "source_nature",
            "result_nature",
            "raw_unit_basis",
            "raw_unit_mapping",
        ),
        "incomplete_root_value",
    )
    if value.get("raw_present") is not True:
        _fail("invalid_root_value")
    raw = value.get("raw")
    normalized = value.get("normalized")
    raw_type = value.get("raw_type")
    if raw_type == "number":
        if (
            isinstance(raw, bool)
            or not isinstance(raw, (int, float))
            or not math.isfinite(raw)
            or normalized != raw
        ):
            _fail("invalid_root_value")
        if metric.native_metric_id != ESP32_FREQUENCY_ENTITY and not 0 <= raw <= 100:
            _fail("invalid_root_value")
        expected_source_nature = "measured"
        expected_availability = "available"
        expected_reason = None
    elif raw_type == "null" and raw is None and normalized is None:
        expected_source_nature = "state"
        expected_availability = "unknown"
        expected_reason = "explicit_null"
    elif raw_type == "string" and raw in {"unknown", "unavailable"} and normalized is None:
        expected_source_nature = "state"
        expected_availability = raw
        expected_reason = f"source_{raw}"
    else:
        _fail("invalid_root_value")
    if (
        value.get("raw_unit") != metric.raw_unit
        or value.get("canonical_unit") != metric.raw_unit
    ):
        _fail("invalid_root_unit")
    if value.get("raw_unit_basis") != metric.raw_unit_basis:
        _fail("invalid_raw_unit_basis")
    if metric.raw_unit_basis == "source_supplied":
        if value.get("raw_unit_mapping") is not None:
            _fail("unexpected_unit_mapping")
    elif value.get("raw_unit_mapping") != {
        "id": metric.raw_unit_mapping_id,
        "version": metric.raw_unit_mapping_version,
    }:
        _fail("invalid_unit_mapping")
    if value.get("source_nature") != expected_source_nature:
        _fail("invalid_source_nature")
    if value.get("result_nature") != metric.result_nature:
        _fail("invalid_result_nature")

    if metric.native_metric_id == ESP32_FREQUENCY_ENTITY:
        evidence = _mapping(record.get("evidence"), "invalid_evidence")
        source_fields = _mapping(
            evidence.get("source_fields"), "invalid_source_fields"
        )
        _require_fields(
            source_fields,
            ("id", "name", "domain", "value", "state", "source_url"),
            "incomplete_source_fields",
        )
        if (
            source_fields.get("id") != metric.native_metric_id
            or not isinstance(source_fields.get("name"), str)
            or source_fields.get("domain") != "sensor"
            or source_fields.get("source_url") != "http://synthetic.invalid/events"
        ):
            _fail("invalid_source_fields")
        if source_fields.get("value") != raw:
            _fail("source_value_mismatch")
        if source_fields.get("state") is not None and not isinstance(
            source_fields.get("state"), str
        ):
            _fail("invalid_source_state")

    if record.get("availability") != expected_availability:
        _fail("invalid_availability")
    if record.get("validity") != "valid":
        _fail("invalid_validity")
    if record.get("capability") != "supported":
        _fail("invalid_capability")
    quality = _mapping(record.get("quality"), "invalid_quality")
    _require_fields(quality, ("categories", "reasons"), "incomplete_root_quality")
    expected_quality_categories = ["direct", "clock_uncertain"]
    if metric.result_nature == "normalized_source_value":
        expected_quality_categories = ["direct", "normalized", "clock_uncertain"]
    if quality.get("categories") != expected_quality_categories:
        _fail("invalid_quality")
    expected_quality_reasons = ["source_time_absent"]
    if expected_reason is not None:
        expected_quality_reasons.append(expected_reason)
    if quality.get("reasons") != expected_quality_reasons:
        _fail("invalid_quality")
    transformation = _mapping(record.get("transformation"), "invalid_transformation")
    _require_fields(
        transformation,
        ("id", "version", "method"),
        "incomplete_root_transformation",
    )
    if any(transformation.get(field) is not None for field in ("id", "version", "method")):
        _fail("unexpected_transformation")
    if record.get("parents") != []:
        _fail("unexpected_parents")
    retention = _mapping(record.get("retention"), "invalid_retention")
    _require_fields(
        retention, ("stream", "policy_id"), "incomplete_root_retention"
    )
    stream = retention.get("stream")
    if not isinstance(stream, str) or stream not in SUPPORTED_RETENTION_STREAMS:
        _fail("unsupported_retention_stream")
    if retention.get("stream") == "raw" and retention.get("policy_id") is not None:
        _fail("unexpected_raw_retention_policy")
    if retention.get("stream") == "retained":
        _nonempty_string(retention.get("policy_id"), "missing_retention_policy")
    expected_diagnostics = [] if expected_reason is None else [expected_reason]
    if record["diagnostics"].get("reason_codes") != expected_diagnostics:
        _fail("invalid_root_diagnostics")


def _validate_status(record: Mapping[str, Any]) -> None:
    _require_fields(record, ("metric_id", "status"), "incomplete_status_profile")
    _prohibit_fields(
        record,
        (
            "observation_id",
            "observation",
            "value",
            "availability",
            "validity",
            "capability",
            "quality",
            "transformation",
            "parents",
            "retention",
        ),
        "invalid_status_profile",
    )
    if record.get("metric_id") is not None:
        _fail("invalid_source_status_metric")
    status = _mapping(record.get("status"), "invalid_status_profile")
    if status.get("scope") != "source" or status.get("state") != "unreachable":
        _fail("unsupported_status")
    source = _mapping(record["source"], "invalid_source")
    _require_fields(
        source,
        ("system", "device", "metric_id", "role", "transport", "lineage"),
        "incomplete_status_source",
    )
    if source.get("device") is not None or source.get("metric_id") is not None:
        _fail("invalid_source_status_identity")
    if source.get("role") != "operational":
        _fail("invalid_source_status_role")
    if source.get("system") != "solarassistant":
        _fail("invalid_source_system")
    if source.get("transport") != "solarassistant_rest_v1":
        _fail("invalid_source_transport")
    if source.get("lineage") != [
        {
            "system": "solarassistant",
            "instance": "solarassistant",
            "role": "root",
            "reference": "solarassistant_rest_v1",
            "transformation_id": None,
            "unresolved": False,
        }
    ]:
        _fail("invalid_lineage")
    time = _mapping(record["time"], "invalid_time")
    _require_fields(
        time,
        (
            "source_at",
            "source_at_raw",
            "received_at",
            "observed_at",
            "basis",
            "source_timezone",
            "precision",
            "clock_quality",
            "uncertainty_ms",
        ),
        "incomplete_status_time",
    )
    _prohibit_fields(
        time,
        ("derived_at", "window_start", "window_end", "anchor_at"),
        "invalid_status_profile",
    )
    if time.get("source_at") is not None or time.get("source_at_raw") is not None:
        _fail("unexpected_source_time")
    if time.get("source_timezone") is not None:
        _fail("unexpected_source_timezone")
    if time.get("basis") != "status_detection":
        _fail("invalid_status_time_basis")
    if time.get("received_at") != time.get("observed_at"):
        _fail("status_time_mismatch")
    if time.get("precision") != "millisecond":
        _fail("invalid_time_precision")
    if time.get("clock_quality") not in {"synchronized", "unknown"}:
        _fail("unsupported_clock_quality")
    if time.get("uncertainty_ms") is not None:
        uncertainty = time.get("uncertainty_ms")
        if (
            isinstance(uncertainty, bool)
            or not isinstance(uncertainty, (int, float))
            or not math.isfinite(uncertainty)
            or uncertainty < 0
        ):
            _fail("invalid_time_uncertainty")


def _validate_rejection(record: Mapping[str, Any]) -> None:
    if "observation_id" in record or "observation" in record or "status" in record:
        _fail("invalid_rejection_profile")
    if record.get("validity") != "rejected":
        _fail("invalid_rejection_validity")
    time = _mapping(record["time"], "invalid_time")
    if time.get("basis") != "status_detection":
        _fail("invalid_rejection_time_basis")
    if time.get("received_at") != time.get("observed_at"):
        _fail("rejection_time_mismatch")


def validate_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and return a detached JSON-compatible record mapping."""
    if not isinstance(record, Mapping):
        _fail("record_not_mapping")
    kind, _ = _common(record)
    if kind == "observation":
        _validate_root(record)
    elif kind == "status":
        _validate_status(record)
    else:
        _validate_rejection(record)
    try:
        json.dumps(record, allow_nan=False, separators=(",", ":"))
    except (TypeError, ValueError):
        _fail("record_not_json_compatible")
    return deepcopy(dict(record))
