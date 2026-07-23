# Next Task

## Objective

Independently review the implemented synthetic ESP32 generator-frequency root
adapter and decide whether it is owner-accepted or requires one bounded
correction.

## Accepted baseline

The synthetic SolarAssistant combined-SOC adapter is independently reviewed and
owner-accepted. The accepted next-milestone review selected an ESP32 frequency
slice as the smallest test that the common validator and registry generalize to
a second source. `docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md` records the
forensic reason to retain electrically surprising finite source values.

## Review task

Review the exact source, registry, validator, synthetic fixture, and focused
tests. Confirm lossless raw `value`/`state` preservation, exact ESP32 identity,
adapter-specified Hz mapping, unrestricted finite numeric values, semantic
occurrence/copy identity, bounded rejection behavior, strict cross-profile
validation, and unchanged SolarAssistant behavior. Confirm specifically that
stream-local ingest order is absent from observation identity and that the
adapter-specified Hz root uses `normalized_source_value` plus normalized
quality.

## Scope

Review is repository-only and read-only unless a separate bounded correction is
authorized. The two review findings concerning copy identity and normalized Hz
semantics were corrected, and the implementation passed 33 focused telemetry
tests and all 251 offline repository tests. It is pending review and is not
owner-accepted.

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

The review either records explicit acceptance or identifies the smallest exact
correction. Production gate 16 remains explicitly Deferred. Recovery is a
normal revert of the one bounded implementation commit with no operational
rollback.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
