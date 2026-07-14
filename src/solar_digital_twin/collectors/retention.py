"""Pure helpers for selective telemetry retention."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


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
