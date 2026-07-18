# Next Task

## Objective

Prepare the separately authorized live canary for the implemented
`esp32-conservative-v1` retained writer. Complete the production-plan preflight,
review the exact invocation, monitoring, stop, rollback, and post-capture
verification steps, and obtain the one operational approval before launch.

## Context

The repository implementation now provides independent `esp32-frequency-v1`
and `esp32-conservative-v1` policies, exclusive output creation, explicit
opt-in canary mode, and a separate append-only capture manifest. Synthetic
validation passed. Production behavior remains unchanged, the current policy
remains the default, raw evidence remains authoritative, and no live canary has
run.

## Scope

1. Verify the repository is clean, synchronized, and at the implementation
   checkpoint with focused and full tests passing.
2. Perform the documented pre-canary VM capacity, time, destination, collision,
   monitoring, stop-time, and rollback readiness checks using read-only access.
3. Review one exact 12-hour daytime canary invocation that produces raw,
   current-retained, conservative-retained, and manifest outputs from one SSE
   stream.
4. Obtain Chris's one operational approval before endpoint access or launch.
5. Do not retire `esp32-frequency-v1`, change a service, or activate a new
   production default.

## Runtime boundary

Use strict read-only, bounded offline access. Do not access credentials,
tokens, protected collector or monitor logs, device controls, services, or
unrelated files. Do not restart or modify the SolarAssistant monitor, EG4
workflow, installed ESP32 collector, evidence, database, permissions, or
runtime. Repository source changes remain limited to the implementation scope.

## Following task

After approved canary execution, preserve and hash all outputs and perform the
separate deterministic canary-analysis milestone. Policy retirement remains a
later decision after every production acceptance gate passes.

## Success

The exact canary work unit is reviewable, capacity and collision checks are
complete, monitoring and rollback are ready, and no live endpoint is accessed
until Chris grants the single operational approval.
