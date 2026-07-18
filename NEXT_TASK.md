# Next Task

## Objective

Perform the first read-only `solardt` VM health review and append the measured
result to `docs/operations/VM_HEALTH_LOG.md`. Do not perform remediation.

## Context

The governance correction established a minimum 30-day and event-driven VM
health schedule, but intentionally took no operational measurement. The
procedure, thresholds, required observations, secret-safety boundary, and
entry format are authoritative in `docs/operations/VM_HEALTH_LOG.md`.

## Scope

1. Inspect root filesystem use and free space, inode use, memory, swap, uptime,
   load averages, summarized leading CPU/memory consumers, relevant failed
   systemd units, approved local disk/filesystem warnings, and aggregate
   evidence/database/report/log growth.
2. Assess capacity for the next planned bounded analysis or capture.
3. Compare with an earlier logged entry if one exists; for this first review,
   record that no prior health-log baseline exists.
4. Classify the result as normal, advisory, or action required using the
   documented thresholds and engineering judgment.
5. Append only the concise result. Do not include full process listings, large
   logs, secrets, tokens, credentials, authorization data, or unrelated private
   details.
6. Do not delete, archive, move, resize, restart, rotate, tune, or otherwise
   remediate anything in this work unit.

## Following technical task

Resume the bounded offline comparison of current ESP32 retained evidence and
the conservative retention candidate against validated real three-source event
windows. Do not change evidence or production retention behavior.

## Success

The first dated health entry records measured capacity and performance facts,
classification, and any recommended follow-up without changing runtime state.
Any persistent corrective action is proposed as a separate risk-classified
work unit and receives a `CHANGE_AUDIT.md` entry if performed.
