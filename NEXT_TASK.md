# Next Task

## Objective

Prepare the smallest safe production-retention implementation plan for the
accepted conservative ESP32 candidate. Do not deploy or change collector
behavior in the planning work unit.

## Context

The deterministic replay in `docs/ESP32_RETENTION_REPLAY.md` preserved all
three validated classifications, the stable control, every full-capture
binary/text transition, frequency ranges and ordering, UTC chronology, and
provenance. It reduced current retained volume by 84.35% by records and 75.82%
by bytes. Production behavior remains unchanged and raw evidence remains
authoritative.

## Scope

1. Map the accepted entity deadbands and 60-second heartbeat into an explicit,
   reviewable ESP32 retention-policy design.
2. Preserve first records, availability transitions, exact text/binary changes,
   UTC timestamps, provenance, and complete raw evidence.
3. Define focused synthetic tests for availability transitions, boundary
   seeding, event ordering, and rollback to the current policy.
4. Define a bounded post-implementation capture verification and decision gate.
5. Do not deploy, alter runtime, or start a capture during the planning work.

## Runtime boundary

Use strict read-only, bounded offline access. Do not access credentials,
tokens, protected collector or monitor logs, device controls, services, or
unrelated files. Do not restart or modify the SolarAssistant monitor, EG4
workflow, ESP32 collector, evidence, database, permissions, or runtime.

## Following task

After the plan is reviewed, implement the candidate in a bounded repository
work unit without deployment. A later separately approved capture should verify
real availability handling and operational size reduction.

## Success

The plan is explicit, testable, reversible, evidence-preserving, and separates
repository implementation from later deployment and capture verification.
