# Telemetry Source Roles

## Status

Initial source-role decisions agreed during read-only discovery.

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

A difference greater than 40 percentage points has been observed, but no alert
threshold has been established.

## ESP32 Role

The ESP32 forensic logger is an electrical and AC-couple evidence source.

It is not a battery SOC authority.

## Display Principles

- never silently merge or substitute values from different sources
- label each value with its source and measurement role
- show both JK battery measurements separately where useful
- show trusted SolarAssistant SOC beside EG4 estimated SOC
- preserve raw differences for later analysis
- do not define alerts until sufficient evidence has been reviewed
