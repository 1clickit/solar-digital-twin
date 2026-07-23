# Next Task

## Objective

Finalize the source-neutral solar-collapse event specification and resolve the
prerequisite for identifying the exact SolarAssistant solar-production trigger
metric, without implementing detection or authorizing operational access.

## Accepted baseline

The corrected synthetic ESP32 generator-frequency adapter and the existing
SolarAssistant combined-SOC adapter are independently reviewed and
owner-accepted. SolarAssistant is the intended initial collapse-trigger
authority; ESP32 and EG4 remain corroborating or contradictory evidence.

The tracked battery-only SolarAssistant collector does not establish the exact
native solar-production metric. The ambiguous aggregate AC-use/load field must
not be substituted, and metric identity must not be invented or inferred.

## Planning and specification task

First inspect whether an existing approved synthetic or sanitized repository
fixture establishes the exact SolarAssistant solar-production native metric
and its semantics. If it does not, specify the smallest separately
authorizable inventory or sanitized-fixture work required to identify and
semantically validate that metric.

Keep the source-neutral event specification usable while the trigger metric is
unresolved. Preserve:

- meaningful established production followed by an abrupt relative decline to
  zero or near zero;
- qualification for more than 30 seconds, with the detector armed through
  sunset;
- a two-minute pre-event and twenty-minute post-collapse window;
- relapse resetting the twenty-minute observation period, while continuous
  zero does not repeatedly create new collapses;
- trusted SolarAssistant/JK BMS SOC below 98% as the research condition;
- ESP32 and EG4 as corroborating or contradictory evidence;
- Volcast, KVBT, sunrise/sunset, and NWS alerts as context only; and
- no causal conclusion.

## Acceptance gates

- The exact trigger metric is either established from already approved
  repository material or remains explicitly unresolved.
- Any needed follow-up inventory or sanitized fixture is narrowly specified,
  separately authorizable, read-only, and provenance-preserving.
- Trigger authority, event state transitions, qualification, relapse, window,
  source-disagreement, missing-data, and contextual-source rules are exact and
  source-neutral.
- Risks of metric ambiguity, stale or missing telemetry, gradual irradiance
  change, sunset, source outage, copied evidence, and false causal inference
  remain explicit.
- Independent review confirms no operational access or detector implementation
  was silently authorized.

## Scope

This is planning/specification only. Do not contact live SolarAssistant or any
device, inspect operational evidence, implement the detector, select production
IDs, define storage schema, perform historical analysis, change collectors or
retention, bind runtime/portal/Home Assistant, add weather integrations, or
create live controls. Production gate 16, the HA native-ID fallback, and the
`solardt` reboot/recovery procedure remain Deferred.

## Success

Success is an independently reviewable source-neutral specification plus an
honest resolution path for the trigger-metric prerequisite. Recovery is a
normal revert of the documentation commit; no operational rollback applies.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
