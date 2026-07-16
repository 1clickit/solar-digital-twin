# Next Task

## Objective

After the configured ESP32 and SolarAssistant capture periods should have
completed, perform separately approved minimal read-only completion and
evidence-integrity verification.

## Context

The fixed ESP32 capture launched at `2026-07-16 13:05:13 America/Chicago` as
unprivileged user `chris` in detached tmux session `esp32-forensic-12h`. It is
configured for 43,200 seconds and should stop automatically at approximately
`2026-07-17 01:05 America/Chicago`, allowing up to about 30 seconds for a
pending network read. PID 107886 was a transient historical observation only.

Its active raw file is
`/home/chris/solar-digital-twin/evidence/esp32/esp32_sse_20260716_180514Z.ndjson`.
Its separate derived retained file is
`/home/chris/solar-digital-twin/evidence/esp32/esp32_sse_20260716_180514Z_retained.ndjson`.
Initial health confirmed one collector, current timestamps, both files growing,
no immediate reconnect or error loop, and a clean repository tree. During 10
seconds, raw grew from 498 to 598 lines and retained from 470 to 566 lines. The
early high retained-to-raw ratio is not a final retention assessment.

The configured SolarAssistant capture period should also be allowed to finish
without interference. Completion of either capture has not yet been verified.

## Scope

1. With separate explicit approval and without signaling either collector,
   confirm each expected automatic completion state.
2. Confirm the ESP32 raw and retained files remain present and nonempty.
3. Record final file sizes, line counts, first and last receipt timestamps, and
   a compact reconnect/error summary without printing full evidence records.
4. Confirm SolarAssistant evidence remains present and its collector completion
   state is understood.
5. Determine whether either capture appears to have terminated prematurely.
6. Preserve all evidence unchanged.
7. Do not begin detailed correlation, retention tuning, monitor deployment, or
   collector restart during this verification work unit.
8. Require a separate reviewed analysis plan after evidence integrity is
   confirmed.

## Following analysis task

After completion and evidence integrity are confirmed, perform the separately
reviewed ESP32 retention assessment defined in
`docs/ESP32_FORENSIC_TELEMETRY_PLAN.md`. That later analysis will calculate
full-capture line and byte retention ratios, explain retained volume, and
recommend whether tuning is justified. Do not begin that assessment, detailed
correlation, or retention tuning during completion verification. Any retention
code or policy change requires still-later separate approval.

## Active-capture boundaries

- Until completion verification, do not stop, restart, signal, attach to,
  redeploy, or modify the ESP32 collector.
- Do not modify ESP32 collector or retention behavior, or alter or truncate
  either active ESP32 evidence file.
- Do not modify the active SolarAssistant collector or its retained-output
  behavior. EG4 workflows remain unchanged.
- Ordinary repository development may continue only when it cannot affect
  these active processes or evidence outputs.
- Repository, commit, or push authorization does not authorize runtime or
  evidence access; completion verification requires separate explicit approval.

## Success

Both collectors' completion states are understood without signaling them,
evidence presence and integrity metadata are recorded without exposing full
records, premature termination is assessed, and all evidence remains unchanged.
Any detailed analysis or runtime change remains separately reviewed and
approved.
