# Next Task

## Objective

Prepare the bounded repository-only implementation request for the accepted synthetic SolarAssistant combined-SOC slice.

## Accepted baseline

`docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md` is the owner-accepted authoritative
implementation plan under `solar-digital-twin.telemetry-observation.v1`.
Independent review passed and Chris accepted both the plan and its selected
first slice. Acceptance establishes planning authority only and does not
authorize implementation automatically.

The selected slice is a minimal shared canonical envelope model/validator plus
a SolarAssistant combined-SOC adapter driven exclusively by synthetic poll
fixtures. It preserves the exact SolarAssistant source mapping, separate
observation and record identities, one normal root SOC observation, and
Deferred production-binding status.

## Scope

Prepare a complete bounded request that defines:

1. exact repository checkpoint and publication mode;
2. the files, minimal standard-library-first interfaces, and synthetic fixtures
   authorized for the slice;
3. separate injected observation-ID and record-ID methods without selecting a
   production encoding;
4. the exact combined-SOC registry mapping, root-record fields, status and
   rejection cases, and raw/retained-copy identity behavior;
5. focused and full offline validation;
6. exact staging, publication, recovery, and completion-report safeguards; and
7. explicit exclusions for every later adapter, storage, production, portal,
   Home Assistant, retention, runtime, evidence, device, and network action.

The request must preserve that `jk_bms` is a canonical telemetry namespace for
JK BMS data reported by SolarAssistant. Solar Digital Twin never contacts a JK
BMS directly; the exclusive source transport is `solarassistant_rest_v1`.

## Protected boundary

This task prepares the implementation request only. It does not itself
authorize code, tests, fixtures, schema or storage changes; evidence or database
access; collector, runtime, service, or device action; live SolarAssistant or
Home Assistant contact; portal/HA binding; retention changes; or persistent
ESP32 operation.

The unresolved HA `source.metric_id` fallback and unscheduled `solardt` reboot/
recovery procedure remain separate deferred tasks.

## Success

A complete, copyable, independently reviewable bounded work request precisely
authorizes the accepted synthetic-only slice without expanding into production
binding or operational work. Implement nothing while preparing that request.

## Architectural sequence

After the bounded request is reviewed and authorized, implement and offline-test
only the selected slice. Storage/schema planning, production binding, other
source adapters, portal binding, Home Assistant export, duplicate-ingestion
retirement, and persistent ESP32 operation remain later independent milestones.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
