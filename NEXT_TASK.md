# Next Task

## Objective

Implement and offline-test one synthetic ESP32 generator-frequency root adapter
that preserves every finite reported value, without production binding or
operational integration.

## Accepted baseline

The synthetic SolarAssistant combined-SOC adapter is independently reviewed and
owner-accepted. The accepted next-milestone review selected an ESP32 frequency
slice as the smallest test that the common validator and registry generalize to
a second source. `docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md` records the
forensic reason to retain electrically surprising finite source values.

## Implementation task

Add one I/O-free adapter for caller-supplied synthetic ESP32 SSE-shaped records
from exact entity `sensor-01_gen_frequency`. Generalize the minimal validator
and immutable registry only as required for strict SolarAssistant and ESP32
root profiles. Preserve every finite numeric value without plausibility-range
rejection, clipping, correction, or suppression. Reject malformed, Boolean,
nonnumeric, and non-finite values with bounded payload-free reasons.

## Scope

Use synthetic repository fixtures only. Preserve raw `value` and `state`, exact
native/canonical identity, forensic role, ESPHome/SSE lineage, receipt-only UTC
time, adapter-specified Hz provenance, ingest ordering, immutable input, and
raw/retained copies as one source occurrence. Cover values near 60 Hz,
threshold crossings, multiples of 60 Hz, 5,000 Hz, 30,000 Hz, explicit null,
`unknown`, `unavailable`, missing, malformed, Boolean, and non-finite input.
Preserve all accepted SolarAssistant behavior.

## Protected boundary

This synthetic implementation does not authorize production observation-ID or
record-ID encoding, production binding, schema/storage/migration/backfill,
collector or retention changes, historical or operational evidence access,
runtime/service/timer/deployment action, portal or Home Assistant binding,
credentials, device/firmware/network activity, weather integrations, or
persistent/additional ESP32 collection.

The unresolved HA `source.metric_id` fallback and unscheduled `solardt` reboot/
recovery procedure remain separate deferred tasks.

## Success

The adapter and focused synthetic tests pass the applicable accepted-contract
gates; all existing tests remain compatible; no import-time or adaptation-time
I/O exists; extreme finite readings remain valid source observations; and
production gate 16 remains explicitly Deferred. Recovery is a normal revert of
the bounded repository implementation commit with no operational rollback.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
