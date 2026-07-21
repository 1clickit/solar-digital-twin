"""Small, I/O-free protocols shared by canonical telemetry adapters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, runtime_checkable

from solar_digital_twin.telemetry.model import CONTRACT_VERSION


class AdapterError(ValueError):
    """A bounded, payload-free adapter failure that cannot become a record."""

    def __init__(self, reason_code: str):
        super().__init__(reason_code)
        self.reason_code = reason_code


@runtime_checkable
class ObservationIdProvider(Protocol):
    """Inject semantic observation IDs without selecting an encoding."""

    def observation_id_for(self, descriptor: Mapping[str, Any]) -> str:
        """Return an ID for one semantic observation occurrence."""


@runtime_checkable
class RecordIdProvider(Protocol):
    """Inject persisted-record IDs without selecting an encoding."""

    def record_id_for(self, descriptor: Mapping[str, Any]) -> str:
        """Return an ID for one canonical record instance."""


@dataclass(frozen=True)
class AdapterContext:
    """Explicit immutable configuration for one adaptation call."""

    registry_version: str
    producer_name: str
    producer_version: str
    observation_id_provider: ObservationIdProvider
    record_id_provider: RecordIdProvider
    contract_version: str = CONTRACT_VERSION


@runtime_checkable
class SourceAdapter(Protocol):
    """Adapt one explicit source record into bounded canonical output."""

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
        """Return observation, status, or rejection records."""
