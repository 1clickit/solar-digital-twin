# Solar Digital Twin - Project State

Current Milestone:
Device time synchronization and solar equipment inventory

Next Task:
Review and standardize time synchronization across all deployed solar equipment using solardt at 192.168.3.11 as the preferred LAN NTP server.

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
- Tracked shell scripts validated with `bash -n`
- Tracked Python source validated with `python -m compileall`
- EG4 and ESP32 forensic correlation design documented
- Project published to GitHub

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
