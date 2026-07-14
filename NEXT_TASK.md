# Next Task

## Objective

Implement the smallest safe standalone read-only SolarAssistant REST
telemetry collector.

## Context

SolarAssistant is reachable at `192.168.3.12`.

Software version `2026-07-02` exposes the authenticated read-only endpoint:

`GET /api/v1/metrics`

The API returns live JK BMS metrics but no source timestamps. Collection must
therefore assign canonical UTC receipt timestamps using the `solardt` clock.

SolarAssistant/JK BMS data is the trusted battery source. EG4 SOC remains a
separate inverter-reported comparison value.

## Scope

- use authenticated read-only REST requests
- obtain the password without committing or displaying it
- define an explicit allowlist of approved battery topics
- preserve combined, Battery 1, and Battery 2 measurements
- assign canonical UTC receipt timestamps
- write raw NDJSON only under ignored `evidence/`
- use bounded polling and request timeouts
- verify a short manual collection run

## Exclusions

- no portal changes
- no SQLite schema changes
- no systemd service
- no control or configuration requests
- no committed evidence or secrets
- no SOC alert threshold yet

## Success

A short manual run records valid timestamped SolarAssistant battery telemetry
without changing SolarAssistant, the portal, or the database.
