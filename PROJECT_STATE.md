# Solar Digital Twin - Project State

Current Milestone:
Safe Codex CLI preparation

Next Task:
Prepare the repository and solardt VM for safe OpenAI Codex CLI use before resuming collector implementation.

## Repository
https://github.com/1clickit/solar-digital-twin

## VM
solardt

## Working Directory
/home/chris/solar-digital-twin

## Current Branch
main

## Current Status
- Repository health check script operational
- status.sh runs repository health check script at startup
- AI engineering framework MVP boundary design documented
- EG4 collector operational
- SQLite database operational
- Evidence capture operational
- CSV report generation operational
- EG4 collector/report MVP complete
- EG4 local portal generator operational
- Browser smoke test passed on LAN
- EG4 local portal systemd service enabled and verified with HTTP 200
- Automated EG4 refresh timer enabled on a 15-minute schedule
- Unattended EG4 refresh verified successfully through systemd
- VM timezone set to America/Chicago for correct EG4 calendar-day collection
- solardt Chrony service synchronized to upstream NTP sources
- solardt LAN NTP server bound to 192.168.3.11:123
- NTP access restricted to the 192.168.3.0/24 LAN
- External NTP response verified successfully from WS01
- Portal browser freshness verified: no-cache headers and 60-second URL-busting reload are present
- Portal timestamps normalized to Central time
- AC-couple and Load gauges reject day telemetry older than 30 minutes
- Portal Load gauge uses day_multiline_samples.csv consumption_w
- status.sh repository health checks operational
- Required-file, duplicate-heading, and documentation-drift checks tested
- Persistent SolarAssistant collection selected with a 10-second base polling interval
- Topic-specific change retention and heartbeat policy documented
- ESP32 frequency observed at one-second cadence with an initial 0.04 Hz storage deadband
- Complete one-second evidence retained around significant forensic events
- EG4 AC-couple step transitions treated as primary evidence; ramp rate is supporting evidence
- Tracked shell scripts validated with `bash -n`
- Tracked Python source validated with `python -m compileall`
- EG4 and ESP32 forensic correlation design documented
- ESPHome forensic logger config saved at `firmware/esphome/eg4_forensic_probe_v3.yaml`
- ESPHome Wi-Fi secrets protected with `firmware/esphome/secrets.yaml` ignored by Git
- ESP32 forensic logger configured and OTA-updated for static IPv4 `192.168.3.13`
- ESP32 forensic logger configured to prefer LAN NTP server `192.168.3.11`
- ESP32 NTP requests to `solardt` verified with `chronyc clients`; forensic log uses the same Central-time basis
- ESP32 forensic logger reachability verified from desktop and solardt
- ESP32 read-only SSE telemetry verified from solardt at one-second cadence
- ESP32 telemetry receipt timestamps verified in America/Chicago
- ESP32 forensic telemetry collection plan documented
- Standalone read-only ESP32 SSE collector implemented and manually verified
- UTC-stamped ignored NDJSON evidence and clean interruption verified
- SolarAssistant static IPv4 `192.168.3.12` and REST API verified
- SolarAssistant software updated to version `2026-07-02`
- Live combined and per-JK-BMS battery telemetry verified
- SolarAssistant/JK BMS established as trusted battery source
- Telemetry source roles and SolarAssistant collection plan documented
- Standalone read-only SolarAssistant REST collector implemented
- Explicit battery-topic allowlist manually verified
- UTC-stamped ignored NDJSON evidence manually verified
- Combined, Battery 1, and Battery 2 telemetry verified
- Clean interruption verified during password prompt and active collection
- Project published to GitHub

- Repomix evaluation stopped as an active task; Repomix remains only an optional future architecture-audit tool.
- Preparing repository rules for safe Codex CLI use on solardt before installation or evaluation.

## Current Reporting Implementation
src/solar_digital_twin/reporting/eg4_daily_report.py
src/solar_digital_twin/reporting/eg4_portal.py

Primary output:
reports/engineering_daily_report.md
reports/eg4_portal.html

Refresh command:
./eg4_refresh_report.sh

## Do Not Change Yet
- EG4 collector behavior
- SQLite schema
- Home Assistant integration
- Additional collectors

## Startup Command
cd /home/chris/solar-digital-twin
source .venv/bin/activate
./status.sh

## Workflow
- One tested step at a time.
- Test before every commit.
- Commit every completed milestone.
- Keep main clean.
- Push to GitHub at session end.
- Engineering Bible is the design authority.
