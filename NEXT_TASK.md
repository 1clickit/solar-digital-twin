# Next Task

## Objective

Prepare and separately authorize one administrator-operated installation and
metadata-only verification of the published ESP32 forensic-collector runtime
on `solardt`. This task definition does not authorize installation.

## Accepted repository baseline

The repository implementation in
`docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md` is complete and offline-tested.
It includes hardened HTTP/SSE behavior, focused regression tests,
`scripts/install_esp32_runtime.sh`, a fixed-provenance finite launcher, and a
dormant `systemd/esp32-forensic-collector.service` with no timer or activation
target. The current default remains `esp32-frequency-v1`.

No runtime, identity, path, permission, unit, or device compatibility has been
installed or verified. The actual ESP32 `Content-Type` remains unknown until a
later passive-verification phase.

## Scope

A new authorization should require Chris-operated commands on exact host
`solardt` and should proceed in observed stages:

1. review the published implementation and run the nonprivileged installer
   `--check`;
2. inspect the existing `/opt/solar-digital-twin` type, ownership, installation
   marker, tracked-runtime contents, and SolarAssistant/shared-runtime impact
   without modifying it;
3. inspect whether `solardt-telemetry` or conflicting identity/group state
   already exists;
4. select any trusted reporting account explicitly and verify that the proposed
   group model grants evidence read/traverse but not write access;
5. only after the preflight matches the documented design, run the
   administrator installation using the reviewed legacy-runtime decision when
   applicable;
6. run metadata-only `--verify` for identity, path, ownership, mode, installed
   commit, code non-writability, evidence access, unit installation, and
   rollback/archive state; and
7. prove the unit is disabled/static and inactive, no timer exists, and no
   automatic contact path was created.

The installer must preserve the complete prior shared runtime through its
timestamped archive model and stop on unknown or incompatible state. A failure
must leave the unit inactive, preserve prior runtime and evidence, and report
the exact partial state before recovery.

## Protected boundary

This document does not authorize installation, root commands, user/group or
permission changes, `/opt`, `/var/lib`, `/etc`, or `/usr` writes, daemon reload,
unit copying, service start/enable/disable/stop, live ESP32 or solar-device
contact, HTTP/SSE requests, capture, evidence changes, firmware, network,
credential, Home Assistant, database, portal, or retention-policy changes.

The later installation work unit must authorize only identity, paths, installed
tracked code, dormant unit installation, daemon reload needed to register that
unit, and metadata verification. It must still prohibit service start,
enablement, device contact, capture, firmware/network/credential/evidence
changes, and persistent operation.

Passive live verification requires another owner authorization after the
installation result is reviewed. Persistent or long-duration operation remains
a fourth, later decision.

## Success

The approved repository commit is installed without damaging the existing
shared runtime; the credentialless identity and paths match the reviewed model;
trusted reporting access is read-only; the installed commit is verifiable; the
unit is present but disabled/static and inactive; no timer exists; prior
runtime and evidence are preserved; and no device was contacted.

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
