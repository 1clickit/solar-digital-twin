# Next Task

## Objective

Prepare, preflight, and—only after explicit approval—launch the fixed 12-hour
ESP32 forensic capture without altering the active SolarAssistant or EG4
workflows.

## Context

The standalone ESP32 SSE collector preserves complete raw evidence and writes a
separate retained stream. Its retained-output behavior passed offline tests but
has not yet been verified against the live ESP32. A controlled 12-hour run is
intended to provide that live verification and collect high-resolution evidence
with useful overlap across the active SolarAssistant capture and normal EG4
workflow. Raw evidence remains authoritative; retained output is derived.

The SolarAssistant badge correction in pushed commit `a227b68` remains
undeployed. The configured SolarAssistant capture has not yet been verified
complete and must not be stopped, restarted, or altered by this work.

## Scope

1. Review current documentation and repository state without accessing live
   evidence or changing any runtime.
2. Under separately reviewed authorization, perform a non-invasive preflight of
   the existing ESP32 collector, intended output paths, available storage, time
   synchronization, and fixed-duration automatic-stop behavior.
3. Prepare and review the exact proposed launch method and command. Do not
   launch during command review.
4. Obtain separate explicit approval before launching the fixed 12-hour run.
5. After launch, perform only minimal approved health confirmation without
   attaching invasively or disturbing the ESP32 or SolarAssistant collectors.
6. Allow automatic completion, then separately review evidence metadata,
   integrity, raw/retained presence, coverage, and retained-output behavior.

## Capture boundaries

- Fixed duration: 12 hours; the run must stop automatically.
- Preserve complete raw ESP32 SSE evidence and the separate retained stream.
- Capture AC-couple power, active-microinverter count, voltage, frequency,
  ramp-rate, status, and forensic-event observations.
- No ESP32 firmware or configuration change is planned.
- Do not change EG4 collection, cadence, portal, SQLite, or equipment settings.
- Do not change the SolarAssistant collector or retained-output behavior, and
  do not stop, restart, or alter its existing capture.
- This is evidence collection and live-retention verification, not final causal
  analysis. Cloud cover and normal solar variability remain possible causes of
  power changes, and success does not require an AC-couple fault.

## Following task

After the configured SolarAssistant capture should have completed, perform the
separately approved minimal read-only completion verification documented in
`docs/SOLARASSISTANT_MONITOR.md`. Review those results before separately
authorizing any installed-monitor update. Only then may the installed monitor
be updated, only the monitor restarted, and the corrected badge verified in a
real browser while preserving all evidence. Do not assume capture completion.

## Success

The exact 12-hour launch is reviewed and explicitly approved, the collector
starts without altering SolarAssistant or EG4 workflows, minimal health is
confirmed non-invasively, the run stops automatically, and later metadata and
integrity review can assess raw and retained evidence. No fault occurrence is
required.
