# Solar Digital Twin - Project State

Current Milestone:
Clean read-only local EG4 web portal MVP

Next Task:
Add EG4 local portal systemd service

## Repository
https://github.com/1clickit/solar-digital-twin

## VM
solardt

## Working Directory
/home/chris/solar-digital-twin

## Current Branch
main

## Current Status
- EG4 collector operational
- SQLite database operational
- Evidence capture operational
- CSV report generation operational
- EG4 collector/report MVP complete
- EG4 local portal generator operational
- Browser smoke test passed on LAN
- Portal Load gauge uses day_multiline_samples.csv consumption_w
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
