# EG4 Local Portal

## Purpose

The dedicated local portal is the intended primary engineering interface. Its
current implementation is a read-only EG4-only dashboard generated from
existing report data.

Home Assistant may later provide complementary convenience, status, and alerts.
It is not an authoritative data store and does not replace raw evidence, SQLite
history, reports, or the engineering portal.

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

- EG4 system status and detail
- EG4-estimated battery SOC gauge
- AC-couple power gauge
- load gauge
- independent Runtime, Energy, and Day Telemetry source health
- Today Usage
- latest engineering findings

Current inputs are the EG4 `runtime_snapshots.csv`, `energy_snapshots.csv`, and
`day_multiline_samples.csv` outputs plus `engineering_daily_report.md`.
SolarAssistant/JK BMS, ESP32, and SQLite history are not yet portal inputs.

## Browser Freshness

The generated portal HTML uses cache-discouraging metadata.

An open portal tab reloads the HTML every 60 seconds using a cache-busting `_refresh` query parameter.

This browser reload:

- requests only the existing generated HTML
- does not run the EG4 collector
- does not regenerate the portal
- remains separate from the 15-minute systemd collection timer

A direct HTTP reload test confirmed that the modification time of `reports/eg4_portal.html` does not change when the browser requests the page.

A LAN browser test confirmed that an open portal tab displayed newly generated HTML after the scheduled refresh without triggering additional EG4 collection.

## Systemd Service

Service source: `systemd/eg4-local-portal.service`

Install and start the service:

`sudo install -m 0644 systemd/eg4-local-portal.service /etc/systemd/system/eg4-local-portal.service`

`sudo systemctl daemon-reload`

`sudo systemctl enable --now eg4-local-portal.service`

Check service status:

`systemctl status eg4-local-portal.service --no-pager`

The service is documented as operational, starts automatically at boot, and
serves the portal on port 8000. This documentation update does not revalidate
the live service.

## Automated Refresh Timer

Refresh service: `systemd/eg4-refresh-report.service`

Refresh timer: `systemd/eg4-refresh-report.timer`

The timer is documented as operational, runs `./eg4_refresh_report.sh` every 15
minutes, and starts five minutes after boot. This documentation update does not
revalidate the live timer or refresh service.

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

Runtime, Energy, and Day Telemetry are evaluated independently. Each source is
shown as Fresh, Stale, Missing, Invalid timestamp, or Future-dated with its own
Central timestamp and approximate age. The initial stale threshold is 30
minutes for each source, representing two expected 15-minute refresh intervals.
The three thresholds are separate constants in the portal generator so they can
be adjusted independently later.

System Status and EG4 Estimated SOC display as unavailable unless Runtime is
fresh. Today Usage displays as unavailable unless Energy is fresh. AC-couple
and Load display as unavailable unless Day Telemetry is fresh. Valid zero
readings remain valid. Normal, warning, or alert styling is applied to inverter
status only when Runtime is fresh; unavailable or unknown status is not shown
as healthy.

The portal-generation timestamp is labeled separately from source-observation
timestamps. Trusted Battery SOC (JK BMS via SolarAssistant) is already collected
by the project but is not yet integrated into this portal. The EG4 SOC card is
explicitly labeled as an inverter estimate. The two values must remain separate;
do not merge, correct, substitute, average, or apply a fixed offset between them.

## Planned Primary-Interface Capabilities

- trusted JK BMS measurements collected through SolarAssistant
- clearly labeled comparison of Trusted Battery SOC (JK BMS via SolarAssistant) and EG4 Estimated SOC
- ESP32 electrical and forensic telemetry
- per-source and per-card freshness
- collector-health and missing-data status
- SQLite-backed source-labeled history and historical trends
- evidence traceability
- evidence-based forensic event correlation with uncertainty

Reports and the portal remain derived consumers of authoritative raw evidence
and normalized SQLite history.

## Planned Refresh and Development Workflows

### Fresh-Data Browser Refresh

A normal static HTML reload does not collect data. A future F5 workflow or
`Refresh data now` control may request one bounded EG4 collection, report, and
portal-generation cycle, then display the newly generated data.

Implementation requires a secured local backend or controlled service
interface. It must prevent overlapping refresh jobs, rapid repeated requests,
uncontrolled command execution, and credential exposure. The portal must show
refresh-in-progress, success, failure, and last-completed time clearly.

### Portal-Development Live Reload

An optional local development mode may automatically reload the browser when
portal code or generated HTML changes so Chris can watch visible progress while
Codex works. Development live reload must remain separate from the normal
production portal and must not trigger telemetry collection.

Neither workflow is implemented.
