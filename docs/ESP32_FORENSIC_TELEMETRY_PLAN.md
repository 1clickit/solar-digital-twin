# ESP32 Forensic Telemetry Collection Plan

## Status
The raw standalone collector was implemented and manually verified on
2026-07-13. The separate retained-output stage is covered by offline tests. A
fixed 12-hour live-verification capture launched successfully on 2026-07-16 as
described below; final retained-output behavior remains pending completion and
evidence-integrity review. The collector is
`src/solar_digital_twin/collectors/esp32_sse.py`.

## Collection Decision
Use the read-only ESPHome HTTP server-sent-event stream at `http://192.168.3.13/events` from `solardt`.

It has been verified over IPv4, exposes the required public entities, requires no ESP32 changes, and avoids adding a native-API client dependency. Console logs are unsuitable for continuous evidence collection.

## Timestamp Semantics
SSE updates do not include a complete event timestamp. Stamp every accepted update on receipt using the synchronized `solardt` clock.

Store ISO 8601 UTC as canonical correlation time and derive `America/Chicago` time for reports. ESP32 log time-of-day text is supporting evidence only.

## Fields
Collect estimated power, active microinverters, curtailment, frequency, L1 current, estimated L1-L2 voltage, total energy, power and frequency ramp rates, largest power drop, event count, current status, forensic event log, and relevant binary event states.

Voltage ramp is not a separate public entity. Calculate it from consecutive voltage updates while preserving voltage deltas embedded in forensic text.

## Raw Evidence and Retained Output
The existing timestamped `esp32_sse_*.ndjson` file is complete raw evidence for every approved SSE update. Collection writes and flushes each raw record before applying retention policy, and selective retention never removes or changes a raw record.

A separate sibling `esp32_sse_*_retained.ndjson` file contains unchanged copies of retained records. All approved non-frequency records pass through. Valid numeric `sensor-01_gen_frequency` observations retain the first value, changes of at least 0.04 Hz from the last retained value, and a 30-second heartbeat measured with monotonic elapsed time. Invalid frequency values remain in raw evidence but do not enter or alter the retained-frequency state.

Raw evidence is primary. If retained output cannot be opened or later fails during retained processing, writing, or flushing, the collector reports the first failure once, disables retained output for that run, and continues raw collection.

## Active Controlled 12-Hour Capture

The fixed capture launched successfully at `2026-07-16 13:05:13
America/Chicago` as unprivileged user `chris` in detached tmux session
`esp32-forensic-12h`. It is configured for 43,200 seconds and should stop
automatically at approximately `2026-07-17 01:05 America/Chicago`, allowing up
to about 30 seconds for a pending network read. PID 107886 was observed at
launch but is transient and not stable runtime configuration.

Active files:

- raw authoritative evidence:
  `/home/chris/solar-digital-twin/evidence/esp32/esp32_sse_20260716_180514Z.ndjson`;
- derived retained output:
  `/home/chris/solar-digital-twin/evidence/esp32/esp32_sse_20260716_180514Z_retained.ndjson`.

Initial health checks found exactly one collector process, current receipt
timestamps, both files growing, no immediate reconnect or error loop, and a
clean repository working tree. During a 10-second interval, raw grew from 498
to 598 lines and retained grew from 470 to 566 lines. This initially high
retained-to-raw ratio is an early observation only, not a final retention
assessment.

Purposes:

- verify the offline-tested retained-output behavior against the live ESP32;
- preserve complete raw ESP32 SSE evidence and the separate retained stream;
- capture high-resolution AC-couple power, active-microinverter count, voltage,
  frequency, ramp-rate, status, and forensic-event observations;
- obtain useful overlap with the active SolarAssistant capture and normal EG4
  collection workflow;
- where timing permits, include daytime solar operation, sunset, production
  shutdown, and evening load or battery transitions; and
- support later timestamp alignment and cross-source forensic analysis.

The capture changes no ESP32 firmware or configuration. It authorizes no change
to the EG4 collector, cadence, portal, SQLite, equipment settings, SolarAssistant
collector, or SolarAssistant retained-output behavior. The existing
SolarAssistant capture must not be stopped, restarted, or altered. Raw evidence
remains authoritative, and retained output is derived.

This first run is evidence collection and live-retention verification, not
final causal analysis. Cloud cover and normal solar variability remain possible
explanations for power changes. Success requires automatic completion plus
intact, reviewable raw and retained evidence with useful timing coverage; it
does not require an AC-couple fault to occur.

Until completion verification, do not stop, restart, signal, attach to,
redeploy, or modify this collector; change collector or retention behavior; or
alter or truncate either active evidence file. Do not modify the active
SolarAssistant collector. EG4 workflows remain unchanged. Ordinary repository
development may continue only when it cannot affect these active processes or
evidence outputs.

After the configured ESP32 and SolarAssistant capture periods should have
completed, separately approved minimal read-only verification will confirm
automatic completion, evidence presence, final metadata and integrity, and
whether either capture appears prematurely terminated. Detailed correlation,
retention tuning, monitor deployment, collector restart, and analysis remain
outside that verification work unit and require a separate reviewed plan.

## Following Post-Capture ESP32 Retention Assessment

Only after completion and evidence integrity are confirmed, a separately
reviewed ESP32 retention assessment must:

1. calculate the full-capture retained-to-raw line ratio;
2. calculate the full-capture retained-to-raw byte ratio;
3. identify which fields, value changes, availability transitions, heartbeats,
   status changes, or forensic events account for the retained volume;
4. determine whether the current retention policy appropriately preserves
   meaningful information or retains unnecessarily high volume;
5. recommend whether retention tuning is justified;
6. remain separate from the initial completion and evidence-integrity
   verification;
7. make no retention-code or policy change until the assessment is reviewed and
   that change is separately approved; and
8. preserve the complete raw stream as authoritative evidence regardless of
   later retention recommendations.

This assessment is analysis, not authorization to change collection or
retention behavior.

## Smallest Safe Implementation Step
The standalone read-only collector reconnects with bounded backoff, filters approved entity IDs, timestamps each update, and appends raw and separately retained newline-delimited JSON under ignored `evidence/`.

Do not modify the EG4 collector, SQLite schema, firmware, thresholds, services, or portal. A later step may transform raw updates into aligned one-second rows.
