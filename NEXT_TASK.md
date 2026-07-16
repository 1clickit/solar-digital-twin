# Next Task

## Objective

Implement a separate retained-output stage for SolarAssistant telemetry using
the approved topic-specific retention and heartbeat policies while preserving
the complete raw NDJSON evidence stream unchanged.

## Context

Commit `c7370ca` completed authentication-failure and response-lifecycle
hardening with focused offline tests. The standalone collector and complete raw
NDJSON evidence remain intact. SolarAssistant credential authority remains
unknown, no credential is installed, and live authenticated work remains
deferred; those facts do not block offline retained-output work.

## Scope

- Keep raw SolarAssistant NDJSON authoritative, complete, and unchanged.
- Write retained records to a separate derived NDJSON stream.
- Continue polling the complete metrics response at the configured interval; retention changes storage cadence, not API traffic.
- Preserve topic allowlists, receipt timestamps, source fields, raw write ordering, and flushing.
- Use the shared retention library where appropriate while keeping SolarAssistant topic policy separate from reusable mechanics.
- Implement the approved 60-second, 5-minute, and daily heartbeats and change policies documented in `docs/SOLARASSISTANT_TELEMETRY_PLAN.md`.
- Do not invent numeric deadbands for families whose meaningful-change threshold remains undefined; keep those thresholds explicit implementation questions.
- Add focused tests requiring no device, credential, network, or existing evidence.
- Design clean reusable components for later sensors without speculative device abstractions.

## Boundaries

- Keep the work bounded, standalone, and reviewable.
- Do not implement credential storage, install credentials, enter passwords,
  contact SolarAssistant, or perform authenticated collector work.
- Preserve authentication handling, polling, backoff, duration, response
  closure, and interruption behavior.
- Keep SQLite, portal, systemd, persistent service installation, and live
  retained-stream verification deferred.
- Do not alter device configuration, existing evidence, or the approved security model.

## Success

Raw output remains byte-for-byte compatible in structure and complete in
coverage; a separate retained stream follows approved topic and heartbeat
policy; polling traffic is unchanged; deterministic offline tests pass; and no
undefined deadband or deferred integration boundary is crossed.
