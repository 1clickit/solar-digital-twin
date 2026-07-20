# Next Task

## Objective

Independently review and accept or correct the proposed telemetry observation and provenance contract.

The proposed contract is `docs/TELEMETRY_OBSERVATION_CONTRACT.md`.

## Accepted repository baseline

Repository hardening, runtime installation, metadata verification, and one
finite one-hour passive ESP32 live verification are complete. The actual fixed
endpoint returned HTTP `200`, zero redirects, and `text/event-stream`; 35,968
raw and 33,515 current-retained records passed schema, allowlist, provenance,
UTC chronology, ordering, permission, manifest, and dormant-state validation.
The unit remains static/inactive with no timer or automatic activation.

## Scope

A bounded review should confirm that the contract:

1. accurately reflects current EG4, SolarAssistant, ESP32, Home Assistant,
   portal, and correlation semantics;
2. preserves raw values, native identities, timestamps, source roles, and
   evidence lineage without silent merging or substitution;
3. defines implementable state, timestamp, freshness, normalization,
   derivation, and feedback-loop rules;
4. keeps `solardt` authoritative and Home Assistant complementary; and
5. separates adapter, storage, portal, export, and persistent-runtime work.

## Protected boundary

The proposed contract authorizes no implementation by itself. Review does not authorize
runtime or service action, live contact, capture, evidence reads or changes,
database/schema migration, portal binding, Home Assistant integration,
credential, firmware/ESPHome, network, retention-policy, or persistent ESP32
operation. Those remain separately bounded decisions.

## Success

Independent ChatGPT review and explicit owner acceptance, or a bounded list of
required corrections, is recorded. Acceptance must not silently authorize
implementation.

## Architectural sequence after hardening

After acceptance, separately plan source adapters and select the first bounded
offline implementation slice; production binding remains later. `solardt`
remains the authoritative aggregation and provenance layer;
Home Assistant should eventually receive selected ESP32 forensic-frequency and
related metrics from `solardt` rather than become duplicate direct ingestion
once the exported path passes lineage, freshness, availability, restart, and
interruption validation.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
