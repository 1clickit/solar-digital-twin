"""Versioned metric registry for the first synthetic telemetry slice."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, Mapping


REGISTRY_VERSION: Final = "1"
COMBINED_SOC_TOPIC: Final = "total/battery_state_of_charge"
ESP32_FREQUENCY_ENTITY: Final = "sensor-01_gen_frequency"


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
    raw_unit_mapping_id: str | None = None
    raw_unit_mapping_version: str | None = None


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

ESP32_GENERATOR_FREQUENCY: Final = MetricDefinition(
    native_metric_id=ESP32_FREQUENCY_ENTITY,
    metric_id="esp32.esphome.forensic_probe.generator_frequency",
    source_system="esp32",
    source_device="forensic_probe",
    source_role="forensic",
    source_transport="http_sse",
    telemetry_namespace="esphome",
    raw_unit="Hz",
    raw_unit_basis="adapter_specified",
    source_nature="measured",
    result_nature="source_value",
    raw_unit_mapping_id="esp32.esphome.sensor-01_gen_frequency.unit",
    raw_unit_mapping_version="1",
)

REGISTRY_V1: Final[Mapping[str, MetricDefinition]] = MappingProxyType(
    {
        COMBINED_SOC_TOPIC: COMBINED_SOC,
        ESP32_FREQUENCY_ENTITY: ESP32_GENERATOR_FREQUENCY,
    }
)


def metric_for(version: str, native_metric_id: str) -> MetricDefinition | None:
    """Resolve an exact native ID from the only implemented registry version."""
    if version != REGISTRY_VERSION:
        return None
    return REGISTRY_V1.get(native_metric_id)
