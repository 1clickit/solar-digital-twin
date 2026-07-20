# Next Task

## Objective

Define a common telemetry observation, provenance, source-lineage, timestamp,
freshness, availability, and normalization contract before production multi-
source portal binding or reciprocal Home Assistant integration.

## Accepted repository baseline

Repository hardening, runtime installation, metadata verification, and one
finite one-hour passive ESP32 live verification are complete. The actual fixed
endpoint returned HTTP `200`, zero redirects, and `text/event-stream`; 35,968
raw and 33,515 current-retained records passed schema, allowlist, provenance,
UTC chronology, ordering, permission, manifest, and dormant-state validation.
The unit remains static/inactive with no timer or automatic activation.

## Scope

A bounded repository design work unit should:

1. inventory existing EG4, SolarAssistant, ESP32, and relevant Home Assistant
   observation and timestamp semantics from authoritative documentation;
2. define canonical measurement identity, source, source lineage, transport,
   receipt time, source time, units, availability, freshness, quality, and
   normalization fields without silently merging incompatible sources;
3. define how copied or exported values retain origin and avoid circular or
   double-counted evidence;
4. define source-specific adapters and acceptance gates before SQLite, portal,
   or Home Assistant production binding; and
5. keep `solardt` authoritative for aggregation and provenance while planning
   selected read-only exports to Home Assistant.

## Protected boundary

This document authorizes no implementation by itself. It does not authorize
runtime or service action, live contact, capture, evidence reads or changes,
database/schema migration, portal binding, Home Assistant integration,
credential, firmware/ESPHome, network, retention-policy, or persistent ESP32
operation. Those remain separately bounded decisions.

## Success

A reviewed contract defines explicit source and lineage semantics, compatible
timestamp/freshness/availability rules, normalization boundaries, adapter
responsibilities, and acceptance gates without changing production systems or
weakening raw-evidence authority.

## Architectural sequence after hardening

After the contract is accepted, separately plan source adapters and production
binding. `solardt` remains the authoritative aggregation and provenance layer;
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
