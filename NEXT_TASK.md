# Next Task

## Objective

Allow active coordinated capture `solar-forensic-20260718T062127Z` to continue
without interference through its planned automatic end at
`2026-07-19T06:21:27.571Z`, then verify completion and restoration, preserve
the evidence unchanged, and prepare the bounded three-source analysis work
unit.

## Context

Chris authorized one common 24-hour interval in place of the earlier 12-hour
ESP32-only canary. `docs/COORDINATED_FORENSIC_CAPTURE.md` defines isolated
native outputs, append-only common provenance, competing-writer handling,
automatic stop/restoration, monitoring, and evidence-preservation boundaries.
The current ESP32 policy remains the production default.

The corrected relaunch passed `startup_verified`. Privileged operator checks
confirm EG4, ESP32, and SolarAssistant are running with growing isolated
outputs and no recent errors. The live processes use implementation commit
`6b734306c6f414c6413f7c6e86e9d443e3fe49e2`; later documentation commits do
not change that live checkpoint. An unprivileged status check can falsely show
the child processes as `not-running` when process inspection is restricted.

## Scope

1. Use only compact, read-only monitoring. Avoid rebooting the VM or changing
   the supervisor, relevant services, timers, collectors, or tmux sessions.
2. Intervene only for documented stop conditions: a source stops, output growth
   stalls or becomes excessive, errors or rapid reconnects persist, timestamps
   become implausible, free space approaches the threshold, or the supervisor
   exits early or reports failure/interruption.
3. Treat nighttime zero AC-couple production, unchanged EG4 bytes between its
   15-minute polls, recovered short reconnects, and cloud-driven production
   variation as expected context rather than automatic stop conditions.
4. After the planned end, verify the transient supervisor and all source
   processes ended, prior services/timers were restored exactly, and the
   append-only manifest has the correct terminal and restoration records.
5. Preserve every evidence file unchanged. Record required sizes, counts,
   timestamps, gaps, parse integrity, and checksums.
6. Prepare a bounded three-source correlation work unit comparing the native
   sources and raw/current/conservative ESP32 context. Do not claim causation
   or retire `esp32-frequency-v1`.

## Runtime boundary

While the capture is active, do not scan evidence, query devices, access
credentials, or alter output, databases, permissions, services, collectors,
monitors, or runtime. The existing SolarAssistant monitor and portal preview
tmux processes are not duplicate collectors and must remain untouched.

## Following task

After evidence analysis, decide whether another capture or a narrowly targeted
measurement is needed. Policy retirement remains a later owner-reviewed
decision after every production acceptance gate passes.

## Success

The capture reaches a verified terminal state, prior units are restored exactly,
immutable source evidence and hashes are preserved, and the next bounded
analysis can proceed with explicit uncertainty.
