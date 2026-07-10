# EG4 Local Portal

## Purpose

The EG4 local portal is a read-only local dashboard generated from existing report data.

## Generate Fresh Data

Run `./eg4_refresh_report.sh` from the repository root.

This updates:

- EG4 CSV reports
- engineering daily report
- local portal HTML

## Portal Output

Generated file: `reports/eg4_portal.html`

The `reports/` directory is ignored by Git and should not be committed.

## Temporary LAN Web Server

Start the server from the repository root:

`python -m http.server 8000 --directory reports --bind 0.0.0.0`

Open the portal from another LAN device using the VM IPv4 address:

`http://VM_IPV4_ADDRESS:8000/eg4_portal.html`

Use IPv4, not IPv6.

Stop the server with Ctrl+C in the terminal running the server.

## Current Portal Status

The portal MVP passed a LAN browser smoke test.

Current dashboard shows:

- system status
- battery SOC gauge
- AC-couple power gauge
- consumption gauge
- data freshness/latest source time
- latest engineering findings
