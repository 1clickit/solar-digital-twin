# Next Task

## Objective

Implement the versioned `esp32-conservative-v1` retained writer and opt-in
dual-output canary mode with synthetic tests only. Do not deploy, run a live
capture, or change the current default policy.

## Context

`docs/ESP32_RETENTION_PRODUCTION_PLAN.md` defines the accepted policy exactly,
chooses one collector process with independent current/candidate writers,
specifies versioned filenames and an append-only manifest, and separates
repository implementation, live canary, analysis, and policy retirement.
Production behavior remains unchanged and raw evidence remains authoritative.

## Scope

1. Add the pure `esp32-conservative-v1` per-entity policy using the adopted
   deadbands and 60-second heartbeat.
2. Preserve the current policy as the default and add explicit opt-in canary
   mode with independent retained state and failure isolation.
3. Add exclusive output creation, versioned candidate naming, and append-only
   capture-manifest identity without changing raw record shape.
4. Import the canonical policy into offline replay rather than duplicating it.
5. Add the focused synthetic tests enumerated in the production plan.
6. Do not access a device, deploy, alter runtime, or start a capture.

## Runtime boundary

Use strict read-only, bounded offline access. Do not access credentials,
tokens, protected collector or monitor logs, device controls, services, or
unrelated files. Do not restart or modify the SolarAssistant monitor, EG4
workflow, installed ESP32 collector, evidence, database, permissions, or
runtime. Repository source changes remain limited to the implementation scope.

## Following task

After repository implementation is reviewed and pushed, request one approval
for the preflight and approximately 12-hour three-output daytime canary. Canary
analysis and retirement remain later milestones.

## Success

The implementation is offline-tested, current behavior remains the default,
raw semantics are unchanged, each retained failure is isolated, and the code is
ready for a separately approved canary without activating it.
