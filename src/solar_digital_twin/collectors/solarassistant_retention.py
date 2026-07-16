"""SolarAssistant topic policy for the first retained-output slice."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

from solar_digital_twin.collectors.retention import retention_reason


SOC_HEARTBEAT_SECONDS = 300.0
DAILY_HEARTBEAT_SECONDS = 86_400.0

SOC_TOPICS = {
    "total/battery_state_of_charge",
    "battery_1/state_of_charge",
    "battery_2/state_of_charge",
}

DAILY_TOPICS = {
    "total/battery_state_of_health",
    "battery_1/state_of_health",
    "battery_2/state_of_health",
    "battery_1/capacity",
    "battery_2/capacity",
    "battery_1/charge_capacity",
    "battery_2/charge_capacity",
    "battery_1/cycles",
    "battery_2/cycles",
}

# These approved raw topics need numeric deadbands before they can be retained.
MEANINGFUL_CHANGE_TOPICS = {
    "total/battery_voltage",
    "total/battery_current",
    "total/battery_power",
    "total/battery_temperature",
    "total/battery_cell_voltage_-_average",
    "total/battery_cell_voltage_-_highest",
    "total/battery_cell_voltage_-_lowest",
    "total/battery_cell_imbalance_-_average",
    *{
        f"{prefix}/{suffix}"
        for prefix in ("battery_1", "battery_2")
        for suffix in (
            "voltage",
            "current",
            "power",
            "cell_voltage_-_average",
            "cell_voltage_-_highest",
            "cell_voltage_-_lowest",
            "cell_voltage_-_imbalance",
            "temperature",
            "temperature_1",
            "temperature_2",
            "temperature_mos",
        )
    },
}

IDENTITY_FIELDS = ("topic", "device", "number", "group", "name", "unit")


def metric_identity(record: dict[str, Any]) -> tuple[Any, ...]:
    """Return stable source identity without observation value or timestamps."""
    return tuple(record.get(field) for field in IDENTITY_FIELDS)


def valid_numeric(value: Any) -> Decimal | None:
    if isinstance(value, bool):
        return None
    try:
        numeric = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None
    return numeric if numeric.is_finite() else None


class SolarAssistantRetentionPolicy:
    """Track exact-change and heartbeat state independently per metric."""

    def __init__(self) -> None:
        self._last_retained: dict[tuple[Any, ...], tuple[Decimal, float]] = {}

    def retention_reason(
        self,
        record: dict[str, Any],
        monotonic_now: float,
    ) -> str | None:
        topic = record.get("topic")
        if topic in SOC_TOPICS:
            heartbeat_seconds = SOC_HEARTBEAT_SECONDS
        elif topic in DAILY_TOPICS:
            heartbeat_seconds = DAILY_HEARTBEAT_SECONDS
        else:
            return None

        current = valid_numeric(record.get("value"))
        if current is None:
            return None

        identity = metric_identity(record)
        retained = self._last_retained.get(identity)
        previous = None if retained is None else retained[0]
        elapsed = None if retained is None else monotonic_now - retained[1]
        reason = retention_reason(
            previous,
            current,
            deadband=0.0,
            seconds_since_retained=elapsed,
            heartbeat_seconds=heartbeat_seconds,
        )
        if reason is not None:
            self._last_retained[identity] = (current, monotonic_now)
        return reason
