# Next Task

## Objective

Discuss and choose the smallest safe operating mode for SolarAssistant
collection before any portal or systemd integration.

## Context

The standalone read-only SolarAssistant REST collector is implemented and
manually verified.

It records approved combined, Battery 1, and Battery 2 JK BMS metrics as
UTC-stamped NDJSON under ignored `evidence/solarassistant/`.

SolarAssistant/JK BMS remains the trusted battery source. EG4 SOC remains a
separate inverter-reported comparison estimate.

## Scope

Choose whether the next operating mode should be:

- manual collection only
- scheduled short collection runs
- a persistent background collector

Compare reliability, evidence volume, credential handling, recovery behavior,
and usefulness for later SOC and battery-voltage displays.

## Exclusions

- no portal changes yet
- no SQLite schema changes yet
- no systemd changes before discussion
- no committed evidence or credentials
- no SOC alert threshold yet

## Success

An agreed operating mode and implementation boundary exist before adding any
persistent SolarAssistant collection or display integration.
