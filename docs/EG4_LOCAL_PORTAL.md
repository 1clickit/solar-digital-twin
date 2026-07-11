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
- load gauge
- data freshness/latest source time
- latest engineering findings

## Systemd Service

Service source: `systemd/eg4-local-portal.service`

Install and start the service:

`sudo install -m 0644 systemd/eg4-local-portal.service /etc/systemd/system/eg4-local-portal.service`

`sudo systemctl daemon-reload`

`sudo systemctl enable --now eg4-local-portal.service`

Check service status:

`systemctl status eg4-local-portal.service --no-pager`

The service starts automatically at boot and serves the portal on port 8000.

## Automated Refresh Timer

Refresh service: `systemd/eg4-refresh-report.service`

Refresh timer: `systemd/eg4-refresh-report.timer`

The timer runs `./eg4_refresh_report.sh` every 15 minutes and starts five minutes after boot.

The collector reads unattended credentials from:

`/etc/solar-digital-twin/eg4.env`

This protected file is owned by root with mode `0600` and must not be committed.

Install and enable the timer:

`sudo install -m 0644 systemd/eg4-refresh-report.service /etc/systemd/system/eg4-refresh-report.service`

`sudo install -m 0644 systemd/eg4-refresh-report.timer /etc/systemd/system/eg4-refresh-report.timer`

`sudo systemctl daemon-reload`

`sudo systemctl enable --now eg4-refresh-report.timer`

Check the timer:

`systemctl status eg4-refresh-report.timer --no-pager`

## Timezone and Data Freshness

The VM timezone must be `America/Chicago` so the collector requests the correct EG4 calendar day.

EG4 runtime and energy `server_time` values are interpreted as UTC and displayed in Central time.

Day telemetry timestamps are interpreted as Central time.

AC-couple and Load retain valid zero readings. If day telemetry is missing or more than 30 minutes old, those gauges display `n/a` with a stale-data warning instead of presenting an old reading as current.
