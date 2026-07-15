# ESP32 Forensic Telemetry Collection Plan

## Status
The raw standalone collector was implemented and manually verified on 2026-07-13. The separate retained-output stage is covered by offline tests but has not yet been verified against the live ESP32. The collector is `src/solar_digital_twin/collectors/esp32_sse.py`.

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

## Smallest Safe Implementation Step
The standalone read-only collector reconnects with bounded backoff, filters approved entity IDs, timestamps each update, and appends raw and separately retained newline-delimited JSON under ignored `evidence/`.

Do not modify the EG4 collector, SQLite schema, firmware, thresholds, services, or portal. A later step may transform raw updates into aligned one-second rows.
