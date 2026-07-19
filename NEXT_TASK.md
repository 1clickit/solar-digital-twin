# Next Task

## Objective

Verify the immutable evidence from intentionally interrupted coordinated
capture `solar-forensic-20260718T062127Z`, then perform the bounded three-source
offline analysis. Keep the prepared EG4 local-dongle path subordinate to this
evidence milestone.

## Context

The capture used implementation commit
`6b734306c6f414c6413f7c6e86e9d443e3fe49e2` and was intentionally stopped
through its transient coordinated service after approximately 21 hours 15
minutes. It had covered nighttime battery discharge, sunrise, the complete
daytime production and charging cycle, sunset, and return to nighttime.

The final manifest reported `capture_terminal`, state `interruption`, reason
`signal`, and `restoration_success: true`. All three children received normal
SIGTERM shutdowns. `eg4-refresh-report.timer` was restored; the coordinated
unit is inactive, the refresh timer and local portal are active/enabled, and the
static refresh service is normally inactive between timer runs. This controlled
interruption is not a capture failure.

The isolated evidence remains at
`/var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z`.
Observed compact totals were approximately 7.06 MB EG4, 605 MB ESP32, and 72.5
MB SolarAssistant, with approximately 64.8 GB free. Those operational
observations are not substitutes for the pending immutable inventory.

## Scope

1. Preserve every evidence file unchanged. Record paths, sizes, counts,
   timestamps, gaps, parse/newline integrity, and SHA-256 identities.
2. Reconcile manifest chronology, terminal/source states, artifact inventory,
   reconnects, coverage, and stable pre/post hashes using bounded read-only
   methods.
3. Perform reproducible three-source correlation using native EG4,
   SolarAssistant, and ESP32 evidence plus raw/current/conservative ESP32
   context.
4. Prioritize the largest production collapses and keep cloud cover, load,
   battery constraints, aggregation, source gaps, and electrical/control
   behavior as explicit alternatives. Do not claim unsupported causation.
5. Keep `esp32-frequency-v1` as production and
   `esp32-conservative-v1` as canary-only.
6. After analysis, obtain owner review before deciding whether a targeted
   follow-up capture or the prepared local-dongle measurement is justified.

## Runtime boundary

Use only approved read-only evidence and strict read-only database paths. Do
not query devices, access credentials, or alter evidence, databases,
permissions, services, collectors, monitors, or runtime. The existing
SolarAssistant monitor and portal preview remain outside this task.

## Following task

After evidence analysis, decide whether another capture or a narrowly targeted
measurement is needed. `docs/EG4_LOCAL_DONGLE_INVESTIGATION.md` prepares one
possible read-only path but authorizes no connection. Home Assistant export,
MQTT migration, irradiance measurement, and retention-policy retirement remain
separately reviewed later work.

## Success

Immutable source identities and hashes are preserved, integrity and coverage
are documented, the first bounded analysis is reproducible, and any follow-up
measurement is chosen with explicit uncertainty and owner review.
