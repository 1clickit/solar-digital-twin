# Next Task

## Objective

Implement the smallest safe standalone read-only ESP32 SSE telemetry collector.

## Context

The reviewed collection design is documented in
`docs/ESP32_FORENSIC_TELEMETRY_PLAN.md`.

The ESPHome `/events` stream has been verified from `solardt` over IPv4.
Required telemetry arrives at approximately one-second intervals.

Because SSE updates do not contain complete timestamps, the collector must
assign synchronized receipt timestamps using the `solardt` clock.

## Scope

- connect read-only to `http://192.168.3.13/events`
- filter an explicit allowlist of approved public entities
- assign canonical UTC receipt timestamps
- preserve entity name, numeric value, state text, and domain
- append raw newline-delimited JSON under ignored `evidence/`
- reconnect using bounded backoff
- stop cleanly without corrupting evidence
- verify a short manual collection run

## Exclusions

- no ESP32 firmware or threshold changes
- no EG4 collector or SQLite schema changes
- no EG4-to-ESP32 correlation yet
- no permanent systemd service yet
- no committed evidence or secrets

## Success

A short manual run records valid timestamped ESP32 telemetry without changing
the ESP32, EG4 collector, database, or generated-artifact policy.
