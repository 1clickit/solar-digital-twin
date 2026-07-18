"""Versioned ESP32 retained-output policies."""

from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from solar_digital_twin.collectors.retention import FrequencyRetentionPolicy

CURRENT_POLICY_ID = "esp32-frequency-v1"
CONSERVATIVE_POLICY_ID = "esp32-conservative-v1"
CONSERVATIVE_HEARTBEAT_SECONDS = 60.0
FREQUENCY_ID = "sensor-01_gen_frequency"

CONSERVATIVE_NUMERIC_DEADBANDS = {
    "sensor-01_estimated_total_ac-coupled_power": 10.0,
    "sensor-01_estimated_active_microinverters": 0.1,
    "sensor-01_estimated_curtailment_percent": 0.5,
    FREQUENCY_ID: 0.04,
    "sensor-01_gen_l1_current": 0.1,
    "sensor-01_estimated_gen_l1-l2_voltage": 0.1,
    "sensor-01_estimated_total_ac-coupled_energy": 10.0,
    "sensor-02_power_ramp_rate": 10.0,
    "sensor-02_frequency_ramp_rate": 0.04,
    "sensor-02_largest_power_drop_since_reset": 10.0,
    "sensor-02_total_events_since_reset": 1.0,
}

UNAVAILABLE_TEXT = frozenset({"unavailable", "unknown", "none", "nan", "null"})
_MISSING = object()


def _unavailable_value(value: Any) -> bool:
    return value is None or (
        isinstance(value, str) and value.strip().lower() in UNAVAILABLE_TEXT
    )


def record_is_unavailable(record: dict[str, Any]) -> bool:
    """Normalize only documented unavailable representations."""
    value = record.get("value", _MISSING)
    state = record.get("state", _MISSING)
    return (
        value is not _MISSING and _unavailable_value(value)
    ) or (
        state is not _MISSING and _unavailable_value(state)
    )


def _numeric(value: Any) -> Decimal | None:
    if isinstance(value, bool):
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None
    return result if result.is_finite() else None


def _value_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


class CurrentESP32RetentionPolicy:
    """The existing frequency-only selective policy."""

    policy_id = CURRENT_POLICY_ID

    def __init__(self) -> None:
        self.frequency = FrequencyRetentionPolicy()

    def retention_reason(
        self, record: dict[str, Any], monotonic_now: float
    ) -> str | None:
        if record.get("id") != FREQUENCY_ID:
            return "pass_through"
        if self.frequency.should_retain(record.get("value"), monotonic_now):
            return "change_or_heartbeat"
        return None


@dataclass
class _EntityState:
    seen: bool = False
    unavailable: bool = False
    last_value_key: str | None = None
    last_numeric: Decimal | None = None
    last_retained_at: float | None = None


class ConservativeESP32RetentionPolicy:
    """The adopted per-entity deadband and heartbeat policy."""

    policy_id = CONSERVATIVE_POLICY_ID
    heartbeat_seconds = CONSERVATIVE_HEARTBEAT_SECONDS
    numeric_deadbands = CONSERVATIVE_NUMERIC_DEADBANDS

    def __init__(self) -> None:
        self._states: dict[str, _EntityState] = {}

    def retention_reason(
        self, record: dict[str, Any], monotonic_now: float
    ) -> str | None:
        entity = record.get("id")
        if not isinstance(entity, str) or not entity:
            raise ValueError("ESP32 retention record requires an entity id")

        state = self._states.setdefault(entity, _EntityState())
        value = record.get("value")
        current_unavailable = record_is_unavailable(record)
        current_numeric = None if current_unavailable else _numeric(value)
        reason: str | None = None

        if not state.seen:
            reason = "first"
        elif current_unavailable != state.unavailable:
            reason = "availability_transition"
        elif current_unavailable:
            pass
        elif current_numeric is not None and entity in self.numeric_deadbands:
            if state.last_numeric is None or abs(
                current_numeric - state.last_numeric
            ) >= Decimal(str(self.numeric_deadbands[entity])):
                reason = "change"
        elif _value_key(value) != state.last_value_key:
            reason = "change"

        if (
            reason is None
            and state.last_retained_at is not None
            and monotonic_now - state.last_retained_at >= self.heartbeat_seconds
        ):
            reason = "heartbeat"

        if reason is None:
            return None

        state.seen = True
        state.unavailable = current_unavailable
        state.last_value_key = _value_key(value)
        if current_numeric is not None:
            state.last_numeric = current_numeric
        state.last_retained_at = monotonic_now
        return reason
