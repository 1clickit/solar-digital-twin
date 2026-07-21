# Next Task

## Objective

Independently review and accept or correct the synthetic SolarAssistant combined-SOC adapter implementation without authorizing production binding.

## Review baseline

The owner-accepted first slice is implemented in
`src/solar_digital_twin/telemetry/` with a committed synthetic fixture and
focused tests. It provides only the minimal root-observation,
source-status, and rejection profiles needed for SolarAssistant combined SOC.

Review should verify:

1. the registry contains exactly the accepted combined-SOC metric;
2. SolarAssistant REST is the sole represented interface and no direct-JK
   source, transport, protocol, address, credential, or connection exists;
3. observation and record IDs use separate required injected providers with no
   production encoding;
4. one valid numeric input emits exactly one root source-value observation and
   no normalized observation;
5. raw and retained records share semantic observation identity but have
   distinct record and copy provenance;
6. missing, null, unknown, unavailable, malformed, out-of-range, unit, time,
   registry, provenance, and ID failures remain distinct and payload-free;
7. one transport outage creates one source-scoped status; and
8. implementation and tests perform no operational I/O.

## Scope

Review the implementation, synthetic fixture, focused tests, contract
conformance, validation results, and exact repository scope. Return bounded
corrections or accept the implementation as an offline source-adapter slice.

The review does not decide production ID encoding, storage representation,
historical adaptation, runtime integration, or the Deferred production-binding
gates.

## Protected boundary

Review does not authorize production binding, schema/storage work, collector or
retention changes, live SolarAssistant or JK access, evidence/database access,
runtime/service action, deployment, portal binding, Home Assistant work, or
persistent ESP32 operation.

The unresolved HA `source.metric_id` fallback and unscheduled `solardt` reboot/
recovery procedure remain separate deferred tasks.

## Success

Independent review either accepts the synthetic-only implementation or returns
specific bounded corrections. Acceptance of the offline implementation does
not authorize production binding or operational integration automatically.

## After acceptance

Select and plan the next contract milestone separately. Production storage and
binding require their own evidence, review, and authorization.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
