"""Versioned metric registry for the first synthetic telemetry slice."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, Mapping


REGISTRY_VERSION: Final = "1"
COMBINED_SOC_TOPIC: Final = "total/battery_state_of_charge"


@dataclass(frozen=True)
class MetricDefinition:
    """Immutable mapping from one native metric to canonical identity."""

    native_metric_id: str
    metric_id: str
    source_system: str
    source_device: str
    source_role: str
    source_transport: str
    telemetry_namespace: str
    raw_unit: str
    raw_unit_basis: str
    source_nature: str
    result_nature: str


COMBINED_SOC: Final = MetricDefinition(
    native_metric_id=COMBINED_SOC_TOPIC,
    metric_id="solarassistant.jk_bms.combined.state_of_charge",
    source_system="solarassistant",
    source_device="jk_bms_bank",
    source_role="authority",
    source_transport="solarassistant_rest_v1",
    telemetry_namespace="jk_bms",
    raw_unit="%",
    raw_unit_basis="source_supplied",
    source_nature="measured",
    result_nature="source_value",
)

REGISTRY_V1: Final[Mapping[str, MetricDefinition]] = MappingProxyType(
    {COMBINED_SOC_TOPIC: COMBINED_SOC}
)


def metric_for(version: str, native_metric_id: str) -> MetricDefinition | None:
    """Resolve an exact native ID from the only implemented registry version."""
    if version != REGISTRY_VERSION:
        return None
    return REGISTRY_V1.get(native_metric_id)
