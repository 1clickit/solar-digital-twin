# Next Task

## Objective

Independently review and accept or correct the proposed telemetry source-adapter plan and selected first offline implementation slice.

## Review baseline

`docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md` is a proposed authoritative
implementation plan governed by the owner-accepted
`solar-digital-twin.telemetry-observation.v1` contract. It maps EG4 cloud
runtime, energy, and day-series data; SolarAssistant/JK BMS; ESP32 SSE; future
allowlisted Home Assistant imports; and normalized and derived producers into
the canonical contract.

The plan selects one later bounded slice: a minimal shared envelope
model/validator plus a SolarAssistant combined-SOC adapter using synthetic poll
fixtures. Production record and observation IDs remain injectable and
unselected. The selection does not authorize implementation automatically.

## Scope

Review should confirm that:

1. the shared adapter boundary is small, deterministic, and storage-neutral;
2. metric and unit registries preserve source identity, authority, and unit
   provenance;
3. every source mapping preserves native timestamp, state, lineage, evidence,
   and retention semantics;
4. all sixteen contract acceptance gates have concrete planning coverage;
5. existing collectors, evidence, SQLite, reports, portal behavior,
   `TimedRecord`, and correlation analysis remain compatible;
6. the selected synthetic-only slice is appropriately bounded and useful; and
7. implementation, production binding, and operational decisions remain
   separately gated.

The unresolved Home Assistant fallback for `source.metric_id` when only an HA
entity ID is known remains a later owner-reviewed adapter decision. The
unscheduled `solardt` reboot/recovery procedure also remains a separate future
task.

## Protected boundary

Review does not authorize adapter or collector code, schemas or migrations,
storage or database access, evidence access or changes, runtime/service action,
live device or Home Assistant contact, portal binding, HA export, retention
changes, or persistent ESP32 operation.

## Success

Independent review either accepts the proposed plan and selected slice or
returns bounded corrections. Acceptance confirms planning authority only; it
does not authorize implementation or publication by itself.

## After acceptance

Separately authorize the selected synthetic-fixture implementation slice.
Storage/schema planning, production normalized storage, portal binding, Home
Assistant export, duplicate-ingestion retirement, and persistent ESP32
operation remain later independent milestones.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
