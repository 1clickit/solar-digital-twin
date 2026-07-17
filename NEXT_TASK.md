# Next Task

## Objective

Perform the separately reviewed, offline ESP32 full-capture retention
assessment defined in `docs/ESP32_FORENSIC_TELEMETRY_PLAN.md`.

## Context

The fixed 12-hour ESP32 capture completed successfully with 43,199.774 seconds
of coverage, 431,513 raw records, and 394,327 retained records. Integrity review
found no malformed or truncated records, backward timestamps, unapproved entity
IDs, unavailable records, or reconnect/error loop. The retained/raw ratios were
approximately 91.38% by line count and 95.77% by bytes; those high ratios are
observations, not conclusions about retention policy.

The overlapping SolarAssistant 24-hour capture also completed normally and
passed with documented permissions-related qualifications. Both sources use
compatible `solardt` UTC receipt timestamps.

## Scope

1. Independently confirm the full-capture retained-to-raw line and byte ratios.
2. Attribute retained volume to fields, value changes, availability
   transitions, heartbeats, status changes, and forensic events.
3. Determine whether the current policy preserves meaningful information or
   retains unnecessary volume.
4. Produce a recommendation on whether retention tuning is justified.
5. Preserve raw evidence as authoritative and leave both evidence files
   unchanged.
6. Do not change collector code, retention policy, thresholds, firmware,
   runtime state, services, EG4 workflows, or SolarAssistant behavior.
7. Require separate review and explicit approval before any retention-code or
   policy change.

## Following task

After the retention assessment is reviewed, prepare a separately bounded
offline EG4/SolarAssistant/ESP32 correlation-analysis plan. The complete ESP32
window overlaps SolarAssistant and their UTC receipt timestamps are compatible,
but matching EG4 evidence availability must be established before three-source
correlation begins.

## Monitor boundary

The SolarAssistant monitor remains running and healthy but stale after capture
completion. A read-only inspection inadvertently included its in-memory abort-
control token field in command output; the token was not used, abort was
disabled, and no credential was accessed. Before any future abort-capable
capture, rotating that token requires a separately approved monitor restart.
Do not restart or deploy the monitor during the retention assessment.

## Success

The high retained volume is explained quantitatively, the policy receives an
evidence-based keep-or-tune recommendation, authoritative raw evidence remains
unchanged, and any implementation remains separately approved.
