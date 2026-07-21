# Telemetry Source Roles

## Status

Initial source-role decisions agreed during read-only discovery.

The owner-accepted canonical representation of these roles alongside
observation, timestamp, freshness, quality, and lineage semantics is
`TELEMETRY_OBSERVATION_CONTRACT.md`. This document remains the authority for
source-role decisions.

## Battery Authority

SolarAssistant data from the two JK BMS devices is the trusted battery source.

Use:

- `total/battery_state_of_charge` for trusted combined battery SOC
- `battery_1/*` for Battery 1 measurements
- `battery_2/*` for Battery 2 measurements

Preserve individual SOC, voltage, current, power, cell voltage, temperature,
capacity, health, and cycle measurements whenever available.

## EG4 Battery SOC

EG4-reported SOC is an inverter estimate and must not replace the trusted
SolarAssistant/JK BMS SOC.

Retain EG4 SOC as a separate comparison value.

The difference between trusted SOC and EG4 SOC may be useful for identifying
estimation drift or loss of alignment.

The disagreement is variable rather than a fixed offset. A difference greater
than 40 percentage points has been observed, while near full charge EG4 was
within approximately 3 percentage points of the trusted SOC.

Do not apply a fixed correction. Preserve and compare the difference over time
and under different charging and discharging conditions. No alert threshold has
been established.

## ESP32 Role

The ESP32 forensic logger is an electrical and AC-couple evidence source.

It is not a battery SOC authority.

## EG4 transport lineage

EG4 cloud data in the solardt collector and HA EG4 Web Monitor are two
presentations of the same upstream cloud/inverter source, not independent
physical corroboration. Future local Wi-Fi-dongle data would be another
transport from that same inverter and must remain labeled `EG4 local Wi-Fi
dongle`.

Home Assistant currently reads the ESP32 directly. If selected Solar Digital
Twin metrics are later exported to HA, those exported copies must retain origin
and transformation lineage and must never be re-ingested or counted as a new
independent source.

## Display Principles

- never silently merge or substitute values from different sources
- label each value with its source and measurement role
- show both JK battery measurements separately where useful
- show trusted SolarAssistant SOC beside EG4 estimated SOC
- preserve raw differences for later analysis
- do not define alerts until sufficient evidence has been reviewed
