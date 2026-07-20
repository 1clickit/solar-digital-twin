# Next Task

## Objective

Prepare and separately authorize one short, finite, passive live verification
of the installed ESP32 forensic-collector runtime on `solardt`. This task
definition does not authorize device contact or service activation.

## Accepted repository baseline

The repository implementation in
`docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md` is complete and offline-tested.
It includes hardened HTTP/SSE behavior, focused regression tests,
`scripts/install_esp32_runtime.sh`, a fixed-provenance finite launcher, and a
dormant `systemd/esp32-forensic-collector.service` with no timer or activation
target. The current default remains `esp32-frequency-v1`.

The runtime and dormant unit from commit
`7f2274b9011c4bb85f3099eb80c8bb86a21f0e04` are installed and metadata-
verified. `solardt-telemetry`, `/var/lib/solar-digital-twin/esp32`, reporter
read-only access, the exact installed commit/unit, and static/inactive state
passed verification. No credential or evidence file exists, no timer or
automatic activation path exists, and no device was contacted. The actual
ESP32 `Content-Type` and live compatibility remain unknown.

## Scope

A new authorization should define one observed finite invocation and verify:

1. installed commit and dormant pre-run state;
2. fixed-destination connectivity and actual compatible SSE `Content-Type`;
3. credentialless operation, approved allowlist, UTC receipt/provenance fields,
   restrictive output ownership/modes, and raw/current-retained ordering;
4. complete start/terminal manifest state, clean finite stop, payload-free
   diagnostics, and preserved partial evidence on failure; and
5. post-run inactive/static state with no timer or persistent operation.

The resulting finite evidence must be inventoried and preserved even if live
compatibility fails. Permanent HTTP/content-policy rejection must not be
retried or worked around by weakening validation or changing the device.

## Protected boundary

This document does not authorize root commands, user/group or permission
changes, installation, daemon reload, unit changes, service start/enablement,
live ESP32 contact, HTTP/SSE requests, capture, evidence creation, firmware,
network, credential, Home Assistant, database, portal, or retention-policy
changes. A new bounded owner authorization must explicitly cover the finite
passive run and its evidence handling. Persistent or long-duration operation
remains a later decision.

## Success

One finite credentialless run confirms actual compatible SSE response behavior,
approved records/provenance, restrictive outputs, clean manifest closure, and
safe stopping without device/configuration change. The unit returns inactive,
no persistent activation is created, and all verification evidence is preserved.

## Architectural sequence after hardening

After installation and a separately authorized passive verification, define a
common telemetry observation, provenance, source-lineage, timestamp, freshness,
availability, and normalization contract before production multi-source portal
binding or reciprocal Home Assistant integration. `solardt` remains the
authoritative aggregation and provenance layer.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
