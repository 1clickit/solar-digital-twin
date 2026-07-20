# Next Task

## Objective

Implement the reviewed ESP32 forensic-collector runtime and security hardening
plan in one separately authorized repository-only work unit. The plan is
`docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md`; this task definition does not
itself begin implementation.

## Accepted baseline

The coordinated evidence is sufficient to establish repeated real aggregate
AC-couple production collapse and recovery for the project's initial
diagnostic baseline. No additional causal measurement is selected now.
Irradiance, local-dongle, sub-second disturbance, per-microinverter, and fan
investigations remain later decision-driven possibilities.

## Scope

The future authorization should cover only the exact repository files and
acceptance gates in sections 5–9 and 11–12 of the hardening plan. Expected work
is:

1. locally reverify current collector and focused-test behavior before editing;
2. implement only the confirmed HTTP/SSE gaps: redirect rejection,
   environment-proxy bypass, compatible content-type validation, a justified
   line/event bound, permanent/transient failure classification, reliable
   response closure, and payload-free diagnostics;
3. preserve the existing URL, allowlist, record/timestamp schema, exclusive
   creation, raw-first ordering, retained-writer isolation, manifests,
   reconnect policy state, and default `esp32-frequency-v1` behavior;
4. add focused collector regression tests;
5. add a reviewed credentialless runtime installer with nonprivileged check,
   install, and metadata-only verify designs, plus focused tests;
6. add a dormant disabled/inactive systemd unit with no timer, no automatic
   contact, restrictive identity/filesystem settings, and semantic tests; and
7. update only directly related documentation, project state, index, and the
   append-only audit.

The implementation must not adopt an unsupported static observation. Identity
installation state and actual device `Content-Type` remain runtime-phase facts.

## Protected boundary

This task definition requires a new bounded authorization before repository
implementation begins. Even then, it must not authorize installation,
deployment, package installation on the host, user/group creation, ACL or
permission change, daemon reload, service start/enable, runtime action, live
ESP32 contact, device query, firmware change, capture, credential access,
network change, database migration, evidence change, portal work, or retention-
policy promotion.

Installation and short passive live verification require separate later
authorizations after repository implementation is committed and reviewed.

## Architectural sequence after hardening

After validated ESP32 repository and runtime phases, define a common telemetry
observation, provenance, source-lineage, timestamp, freshness, availability,
and normalization contract before production multi-source portal binding or
reciprocal Home Assistant integration. `solardt` remains authoritative for
aggregation and provenance; HA, direct EG4, EG4 cloud, SolarAssistant, and
ESP32 measurements must remain separately identifiable.

HA-derived EG4 provenance remains
`Home Assistant → EG4 Web Monitor hybrid mode`; per-entity local-dongle versus
cloud lineage remains unproven. Home Assistant's direct ESPHome path must not be
removed until a selected `solardt` export is implemented and validated.

## Success

The repository contains tested collector safeguards, a reviewed installer and
dormant unit, updated documentation and recovery, and proof that current
evidence/retention semantics remain unchanged—without any installation,
runtime action, or device contact.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
