# ESP32 Forensic Telemetry Collection Plan

## Status
The raw standalone collector was implemented and manually verified on
2026-07-13. The separate retained-output stage is covered by offline tests. The
fixed 12-hour live-verification capture completed successfully on 2026-07-17
and passed evidence-integrity review as described below. The subsequent
full-capture assessment and real-window replay found no implementation defect
and adopted the conservative candidate for a separately reviewed rollout. The
production policy remains unchanged; the implementation and canary design are
in `docs/ESP32_RETENTION_PRODUCTION_PLAN.md`. The collector is
`src/solar_digital_twin/collectors/esp32_sse.py`. Static runtime/security review
and the separately gated hardening phases are defined in
`docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md`. Repository hardening is
implemented and offline-tested; no installation, runtime action, or live
compatibility verification has occurred.

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

## Completed Controlled 12-Hour Capture

The fixed capture launched at `2026-07-16 13:05:13 America/Chicago` as
unprivileged user `chris` in detached tmux session `esp32-forensic-12h`, ran for
its requested 43,200 seconds, and stopped automatically. PID 107886 was a
transient launch observation, not stable runtime configuration.

Evidence files:

- raw authoritative evidence:
  `/home/chris/solar-digital-twin/evidence/esp32/esp32_sse_20260716_180514Z.ndjson`;
- derived retained output:
  `/home/chris/solar-digital-twin/evidence/esp32/esp32_sse_20260716_180514Z_retained.ndjson`.

The reviewed window was `2026-07-16T18:05:14.599Z` through
`2026-07-17T06:05:14.373Z`, or 43,199.774 seconds. Raw evidence contains
431,513 records and 156,174,965 bytes; retained output contains 394,327 records
and 149,568,755 bytes, for 305,743,720 combined bytes. Both files end with a
newline. All records parsed, timestamps never moved backward, the largest raw
gap was 1.102 seconds, and primary telemetry median cadence was approximately
1.001 seconds.

All 17 approved public entity IDs appeared and no unapproved ID appeared.
Every timestamp used canonical UTC; no unavailable record or reconnect/error
loop was found. Every retained record matched an unchanged raw record in the
same order. Repeated millisecond receipt timestamps represented distinct
events received within the same millisecond, not duplicate records. The result
is **Passed**.

The retained/raw ratios are approximately 91.38% by line count and 95.77% by
bytes. These are inputs to the following assessment, not evidence that the
policy should already change.

Purposes:

- verify the offline-tested retained-output behavior against the live ESP32;
- preserve complete raw ESP32 SSE evidence and the separate retained stream;
- capture high-resolution AC-couple power, active-microinverter count, voltage,
  frequency, ramp-rate, status, and forensic-event observations;
- obtain useful overlap with the concurrent SolarAssistant capture and normal EG4
  collection workflow;
- where timing permits, include daytime solar operation, sunset, production
  shutdown, and evening load or battery transitions; and
- support later timestamp alignment and cross-source forensic analysis.

The capture changed no ESP32 firmware or configuration. It authorizes no change
to the EG4 collector, cadence, portal, SQLite, equipment settings, SolarAssistant
collector, or SolarAssistant retained-output behavior. Raw evidence remains
authoritative, and retained output is derived.

This first run is evidence collection and live-retention verification, not
final causal analysis. Cloud cover and normal solar variability remain possible
explanations for power changes. Success required automatic completion plus
intact, reviewable raw and retained evidence with useful timing coverage; it
did not require an AC-couple fault. That success criterion was met. Preserve
both files unchanged. Collector or retention changes remain separately
reviewed and approved.

## Completed Post-Capture ESP32 Retention Assessment

Completion and evidence integrity are confirmed. The completed assessment:

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

The measured ratios were 91.382% by record and 95.770% by byte. Current behavior
matches the documented frequency-only selective policy; all non-frequency
entities pass through. The replay is complete and supports an Adopt decision,
but no production retention change has occurred. Implementation, canary
activation, canary analysis, and retirement remain separate milestones.

## Smallest Safe Implementation Step
The standalone read-only collector reconnects with bounded backoff, filters
approved entity IDs, timestamps each update, and writes raw and separately
retained newline-delimited JSON under ignored `evidence/`.

The collector also accepts an explicit `--output-dir` for isolated coordinated
captures. Omitting it preserves the historical `evidence/esp32` default and
normal `esp32-frequency-v1` behavior. The coordinated 24-hour runbook is
`docs/COORDINATED_FORENSIC_CAPTURE.md`; it uses explicit canary mode without
retiring the current policy.

The versioned conservative writer and opt-in canary mode defined in
`docs/ESP32_RETENTION_PRODUCTION_PLAN.md` are implemented and synthetically
validated. The historical `esp32-frequency-v1` output remains the default;
`esp32-conservative-v1` is dormant unless explicitly selected. No live canary,
deployment, or production-default change occurred. The next step is a
separately authorized administrator installation and metadata-only verification
under `docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md`. It does not promote a
retention policy or authorize service activation, device contact, capture,
firmware, network, database, or portal changes.
