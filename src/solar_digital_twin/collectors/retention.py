"""Pure helpers for selective telemetry retention."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


class FrequencyRetentionPolicy:
    """Retain numeric frequency changes and periodic heartbeats."""

    def __init__(self, deadband_hz: float = 0.04, heartbeat_seconds: float = 30):
        if deadband_hz < 0:
            raise ValueError("deadband_hz must not be negative")
        if heartbeat_seconds <= 0:
            raise ValueError("heartbeat_seconds must be positive")

        self.deadband_hz = Decimal(str(deadband_hz))
        self.heartbeat_seconds = heartbeat_seconds
        self.last_value: Decimal | None = None
        self.last_retained_at: float | None = None

    def should_retain(self, value: Any, monotonic_now: float) -> bool:
        """Return whether a frequency observation belongs in retained output."""
        if isinstance(value, bool):
            return False

        try:
            current = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            return False

        if not current.is_finite():
            return False

        first = self.last_value is None
        changed = (
            not first
            and abs(current - self.last_value) >= self.deadband_hz
        )
        heartbeat = (
            self.last_retained_at is not None
            and monotonic_now - self.last_retained_at >= self.heartbeat_seconds
        )

        if not (first or changed or heartbeat):
            return False

        self.last_value = current
        self.last_retained_at = monotonic_now
        return True


def meaningful_change(
    previous: Any,
    current: Any,
    deadband: float = 0.0,
) -> bool:
    """Return whether a telemetry value changed by the deadband or more."""
    if deadband < 0:
        raise ValueError("deadband must not be negative")

    if previous is None:
        return True

    try:
        difference = abs(Decimal(str(current)) - Decimal(str(previous)))
        threshold = Decimal(str(deadband))
    except (InvalidOperation, TypeError, ValueError):
        return current != previous

    if difference == 0:
        return False

    return difference >= threshold


def heartbeat_due(
    seconds_since_retained: float | None,
    heartbeat_seconds: float,
) -> bool:
    """Return whether an unchanged metric needs a retained heartbeat."""
    if heartbeat_seconds <= 0:
        raise ValueError("heartbeat_seconds must be positive")

    if seconds_since_retained is None:
        return True

    if seconds_since_retained < 0:
        raise ValueError("seconds_since_retained must not be negative")

    return seconds_since_retained >= heartbeat_seconds


def retention_reason(
    previous: Any,
    current: Any,
    deadband: float,
    seconds_since_retained: float | None,
    heartbeat_seconds: float,
) -> str | None:
    """Return why a telemetry value should be retained, if at all."""
    if meaningful_change(previous, current, deadband):
        return "change"

    if heartbeat_due(seconds_since_retained, heartbeat_seconds):
        return "heartbeat"

    return None
