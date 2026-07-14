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
