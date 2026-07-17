# Next Task

## Objective

Establish matching EG4 evidence availability and prepare a separately bounded
offline EG4/SolarAssistant/ESP32 correlation-analysis plan.

## Context

The ESP32 retention assessment is complete. It found that current behavior
matches the documented policy: frequency is selectively retained at a 0.04 Hz
deadband and 30-second heartbeat, while all non-frequency entities pass through.
No defect or policy change was approved. The full ESP32 window overlaps the
completed SolarAssistant capture and both use compatible `solardt` UTC receipt
timestamps. Matching EG4 evidence has not yet been established.

## Scope

1. Use read-only repository and evidence metadata inspection to establish
   whether matching EG4 evidence covers the ESP32/SolarAssistant overlap.
2. Define exact source files, timestamp semantics, alignment rules, bounded
   event windows, and missing-data treatment before analysis.
3. Preserve source identities and avoid claiming that correlation proves
   causation.
4. Include representative event windows suitable for later replay of the
   conservative ESP32 retention candidate.
5. Do not begin broad correlation, change retention policy, or modify evidence,
   collectors, databases, services, or runtime state.

## Following task

After the plan and evidence availability are reviewed, perform the separately
approved bounded offline correlation. Use its known event windows to validate
whether the conservative ESP32 retention candidate preserves dropout,
recovery, plateau, frequency, binary-event, and availability evidence.

## Monitor boundary

The SolarAssistant monitor remains running and healthy but stale after capture
completion. A read-only inspection inadvertently included its in-memory abort-
control token field in command output; the token was not used, abort was
disabled, and no credential was accessed. Before any future abort-capable
capture, rotating that token requires a separately approved monitor restart.
Do not restart or deploy the monitor during correlation planning.

## Success

Matching EG4 evidence availability and timestamp compatibility are explicit,
the bounded analysis method is reviewable, all evidence remains unchanged, and
no correlation or retention implementation begins without separate approval.
