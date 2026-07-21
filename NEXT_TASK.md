# Next Task

## Objective

Plan source-specific adapters and select the first bounded offline implementation slice.

The planning is governed by the owner-accepted
`docs/TELEMETRY_OBSERVATION_CONTRACT.md`.

## Accepted repository baseline

`solar-digital-twin.telemetry-observation.v1` passed final independent ChatGPT
review and was explicitly accepted by Chris as the authoritative observation
and provenance contract. Its six earlier internal review findings are resolved.
Acceptance establishes design authority but does not authorize implementation.

## Scope

A bounded repository-only planning work unit should:

1. define source-adapter plans for EG4 cloud runtime, energy, and day series;
2. define adapter plans for SolarAssistant/JK BMS, ESP32 SSE, and future
   allowlisted Home Assistant imports;
3. define normalized and derived producer responsibilities;
4. plan the adapter registry and stable metric-ID mappings;
5. map source-specific timestamps, state, unit, lineage, and evidence fields;
6. assess compatibility with existing SQLite, NDJSON, reports, portal behavior,
   and `TimedRecord`;
7. identify contract acceptance gates for each source before production
   binding; and
8. select and justify one small offline-fixture implementation slice for a
   later separately authorized work unit.

The planning must preserve the unresolved HA-import fallback meaning of
`source.metric_id` when only the HA entity ID is known as an explicit deferred
adapter decision; milestone selection must not silently decide it.

## Protected boundary

This task is planning-only. It does not authorize adapter or collector code,
schemas or migrations, database reads/writes, evidence reads or changes,
runtime/service action, live device or Home Assistant contact, portal binding,
HA export, retention changes, or persistent ESP32 operation. The separately
deferred `solardt` VM reboot/recovery procedure is not part of this milestone.

## Success

A reviewed source-adapter plan maps each source honestly to the accepted
contract, documents compatibility and acceptance gates, and selects one small
offline-fixture implementation slice without performing implementation or
crossing an operational boundary.

## Architectural sequence

After adapter planning is accepted, separately authorize the selected offline
fixture slice. Storage/schema planning, production normalized storage, portal
binding, Home Assistant export, duplicate-ingestion retirement, and persistent
ESP32 operation remain later independent milestones.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
