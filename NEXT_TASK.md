# Next Task

## Objective

Select and plan the next telemetry-contract milestone after acceptance of the synthetic SolarAssistant combined-SOC adapter, without authorizing production binding or operational integration.

## Accepted baseline

The synthetic offline SolarAssistant combined-SOC adapter is independently
reviewed and owner-accepted. Its minimal root-observation, source-status, and
rejection profiles remain unbound to production IDs, storage, collectors,
runtime, devices, portal, or Home Assistant integration.

## Planning task

Review the already documented deferred telemetry-contract milestones and
recommend one bounded next milestone. Record its rationale, dependencies,
risks, exclusions, acceptance gates, and recovery approach. Resolve only the
planning detail needed to make that milestone separately reviewable and
authorizable.

## Scope

Inspect the accepted contract, adapter plan, current state, and existing
deferred decisions. Compare candidate milestones and select one without
implementing it. Preserve unresolved alternatives and identify prerequisites
that need separate evidence or owner decisions.

## Protected boundary

Milestone selection does not authorize implementation, production binding,
schema or storage work, collector or retention changes, live SolarAssistant or
JK access, evidence or database access, runtime or service action, deployment,
portal binding, Home Assistant work, device or network activity, or persistent
ESP32 operation. Each remains separately reviewed and approved.

The unresolved HA `source.metric_id` fallback and unscheduled `solardt` reboot/
recovery procedure remain separate deferred tasks.

## Success

One bounded next telemetry-contract milestone is recommended with explicit
rationale, dependencies, risks, exclusions, acceptance gates, and recovery.
The result is a plan only and grants no implementation or operational authority.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
