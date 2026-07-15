# Next Task

## Objective

Complete the smallest safe standalone SolarAssistant collector-hardening work
unit while preserving its existing raw evidence output.

## Context

Codex CLI setup and its first bounded coding workflow are complete. The ESP32
collector now preserves raw NDJSON evidence and writes a separate selectively
retained stream.

The current engineering implementation goal remains persistent multi-rate
telemetry collection. The standalone SolarAssistant collector and its raw
NDJSON evidence have already been manually verified. Existing telemetry plans
document topic-specific observation and retention direction.

## Scope

- Harden only the existing standalone SolarAssistant collector.
- Preserve its existing raw NDJSON evidence filename and record format.
- Select the smallest coherent retained-output step authorized by the existing
  telemetry plans.
- Add focused offline tests requiring no device, credentials, network access,
  or existing evidence files.
- Keep portal, SQLite, and systemd integration deferred.
- Do not modify SolarAssistant device behavior or issue control requests.
- Keep credentials, generated evidence, and secrets out of the repository and
  command output.

## Boundaries

- Keep the work standalone, bounded, and reviewable.
- Preserve existing polling, authentication, timestamp, allowlist, flushing,
  duration, backoff, and clean-interruption behavior unless the bounded task
  explicitly requires and tests a change.
- Do not add portal, SQLite, systemd, or device-control integration.
- Do not expand retention policy beyond existing repository plans.

## Success

One focused SolarAssistant hardening step is implemented and verified offline,
raw evidence remains intact, and no deferred integration boundary is crossed.
