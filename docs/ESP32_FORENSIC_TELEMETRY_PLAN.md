# ESP32 Forensic Telemetry Collection Plan

## Status
Reviewed design. Implementation is deferred to a later task.

## Collection Decision
Use the read-only ESPHome HTTP server-sent-event stream at `http://192.168.3.13/events` from `solardt`.

It has been verified over IPv4, exposes the required public entities, requires no ESP32 changes, and avoids adding a native-API client dependency. Console logs are unsuitable for continuous evidence collection.

## Timestamp Semantics
SSE updates do not include a complete event timestamp. Stamp every accepted update on receipt using the synchronized `solardt` clock.

Store ISO 8601 UTC as canonical correlation time and derive `America/Chicago` time for reports. ESP32 log time-of-day text is supporting evidence only.

## Fields
Collect estimated power, active microinverters, curtailment, frequency, L1 current, estimated L1-L2 voltage, total energy, power and frequency ramp rates, largest power drop, event count, current status, forensic event log, and relevant binary event states.

Voltage ramp is not a separate public entity. Calculate it from consecutive voltage updates while preserving voltage deltas embedded in forensic text.

## Smallest Safe Implementation Step
Create a standalone read-only collector that reconnects with bounded backoff, filters approved entity IDs, timestamps each update, and appends raw newline-delimited JSON under ignored `evidence/`.

Do not modify the EG4 collector, SQLite schema, firmware, thresholds, services, or portal. A later step may transform raw updates into aligned one-second rows.
