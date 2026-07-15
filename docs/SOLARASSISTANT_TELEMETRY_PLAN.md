# SolarAssistant Read-Only Telemetry Plan

## Status

Implemented and manually verified on 2026-07-14. Collector: `src/solar_digital_twin/collectors/solarassistant.py`.

## Purpose

Define the smallest safe standalone collector for trusted JK BMS telemetry
from SolarAssistant.

## Source

- host: `192.168.3.12`
- endpoint: `GET /api/v1/metrics`
- authentication username: `admin`
- software version verified: `2026-07-02`
- interface is read-only for this task

## Credential Handling

The collector will read `SOLARASSISTANT_PASSWORD` from the environment.

For an interactive manual run, it may fall back to a private `getpass` prompt.

The password must never be printed, written to evidence, committed, or included
in command output.

## Timestamp and Evidence Policy

The REST response does not contain source timestamps.

Each successful poll will receive one canonical UTC timestamp from the
synchronized `solardt` clock. Every approved metric from that response will
carry the same poll receipt timestamp.

Raw evidence will be newline-delimited JSON under:

`evidence/solarassistant/`

Each record will preserve:

- `received_at_utc`
- source URL
- topic
- device
- device number when present
- group
- metric name
- numeric value
- unit

Generated evidence remains ignored by Git.

Raw evidence files are authoritative source material and must be preserved.

## Cadence Definitions and Status

- **API polling interval:** how often the collector requests the complete REST response.
- **Raw evidence cadence:** every approved metric from every successful poll is written and flushed to raw NDJSON.
- **Retained-history cadence:** how often a topic is eligible for a future retained-output record.
- **Heartbeat cadence:** the maximum planned interval between retained records when an observed value remains stable.

The current collector defaults to one-second polling. That remains available for
manual or diagnostic use, but the approved intended normal persistent polling
interval is 10 seconds. The existing raw collector and its one-second default
were manually verified.

Topic-specific retained-history and heartbeat schedules are documented in
`docs/EG4_FORENSIC_CORRELATION.md`; they remain planned and are not implemented
for SolarAssistant. Changing retention does not change API traffic or raw
evidence cadence. No persistent SolarAssistant systemd service exists yet.

## Approved Topic Scope

The first collector will use an explicit allowlist.

Combined battery topics:

- `total/battery_state_of_charge`
- `total/battery_voltage`
- `total/battery_current`
- `total/battery_power`
- `total/battery_temperature`
- `total/battery_state_of_health`
- `total/battery_cell_voltage_-_average`
- `total/battery_cell_voltage_-_highest`
- `total/battery_cell_voltage_-_lowest`
- `total/battery_cell_imbalance_-_average`

Battery 1 and Battery 2 will preserve the equivalent individual measurements
under `battery_1/*` and `battery_2/*`.

Approved suffixes for both `battery_1/` and `battery_2/`:

- `state_of_charge`
- `voltage`
- `current`
- `power`
- `state_of_health`
- `capacity`
- `charge_capacity`
- `cycles`
- `cell_voltage_-_average`
- `cell_voltage_-_highest`
- `cell_voltage_-_lowest`
- `cell_voltage_-_imbalance`
- `temperature`
- `temperature_1`
- `temperature_2`
- `temperature_mos`

No topic outside these explicit combined and individual lists will be written
by the first collector.

## Polling and Failure Handling

The current collector will:

- poll once per second by default
- use a finite HTTP request timeout
- timestamp only successful responses
- skip malformed or missing metrics without inventing values
- retry connection failures using bounded backoff
- stop cleanly on Ctrl+C
- flush each NDJSON record promptly

The polling interval is configurable. One second is the current default and
manual diagnostic capability; 10 seconds is the intended normal persistent
configuration.

## Exclusions

- no SolarAssistant control or configuration requests
- no portal changes
- no SQLite schema changes
- no systemd service
- no committed evidence or credentials
- no SOC alert threshold
- no automatic substitution for missing values

## Manual Verification

A short run must demonstrate:

- successful authenticated read-only polling
- only approved topics written
- canonical UTC receipt timestamps
- combined and both individual batteries represented
- valid newline-delimited JSON
- evidence ignored by Git
- clean interruption without evidence corruption
