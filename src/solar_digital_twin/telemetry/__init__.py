"""Canonical telemetry adaptation primitives."""

from solar_digital_twin.telemetry.adapters import (
    AdapterContext,
    AdapterError,
    ObservationIdProvider,
    RecordIdProvider,
    SourceAdapter,
)
from solar_digital_twin.telemetry.model import (
    CONTRACT_VERSION,
    ContractValidationError,
    LineageHop,
    validate_record,
)
from solar_digital_twin.telemetry.solarassistant_adapter import (
    SolarAssistantSocAdapter,
)

__all__ = [
    "AdapterContext",
    "AdapterError",
    "CONTRACT_VERSION",
    "ContractValidationError",
    "LineageHop",
    "ObservationIdProvider",
    "RecordIdProvider",
    "SolarAssistantSocAdapter",
    "SourceAdapter",
    "validate_record",
]
