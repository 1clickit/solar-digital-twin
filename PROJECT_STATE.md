# Solar Digital Twin - Project State

Current Milestone:
Owner review of coordinated-capture findings and follow-up measurement decision

Next Task:
Review the seven correlated production-collapse candidates and decide whether one targeted follow-up measurement is justified.

## Repository
https://github.com/1clickit/solar-digital-twin

## VM
solardt

## Working Directory
/home/chris/solar-digital-twin

## Current Branch
main

## Current Status
- Coordinated capture `solar-forensic-20260718T062127Z` was intentionally
  stopped through transient supervisor
  `solar-coordinated-solar-forensic-20260718T062127Z.service` after
  approximately 21 hours 15 minutes, after observing nighttime discharge,
  sunrise, the complete daytime production/charging cycle, sunset, and return
  to nighttime
- The capture used implementation commit
  `6b734306c6f414c6413f7c6e86e9d443e3fe49e2`; later repository-only
  documentation commits did not change the code revision used by its processes
- Startup was verified at approximately `2026-07-18T06:21:27Z`
  (`2026-07-18 01:21:27 CDT`), and automatic completion had been planned for
  `2026-07-19T06:21:27.571Z` (`2026-07-19 01:21:27 CDT`)
- Final compact observation reported `capture_terminal`, no recent error,
  approximately 7.06 MB EG4, 605 MB ESP32, and 72.5 MB SolarAssistant evidence,
  with approximately 64.8 GB free
- Final manifest observations record normal SIGTERM shutdown for all three
  children, terminal state `interruption`, reason `signal`, and
  `restoration_success: true`. This intentional controlled stop is not a
  capture failure
- Post-closure unit verification found the coordinated transient unit inactive,
  `eg4-refresh-report.timer` active/enabled,
  `eg4-refresh-report.service` inactive/static as normal between timer runs,
  and `eg4-local-portal.service` active/enabled
- Raw evidence is immutable. The exact 444-file inventory, stable pre/post
  hashes, native parse/newline checks, record counts, timestamp coverage,
  cadence/gaps, reconnect review, and SQLite/artifact integrity verification
  passed. The ESP32-specific manifest lacks a terminal record, but the common
  manifest records its controlled SIGTERM and every ESP32 stream ends cleanly;
  this is a documented provenance qualification, not evidence invalidation.
- The first reproducible three-source analysis is complete. The primary
  detector found seven candidates: five zero-output events and two partial
  collapses. All seven classifications and three deterministic controls were
  preserved by raw, current-retained, and conservative-canary ESP32 streams
- The five zero-output events remain under the fixed strict sensitivity set;
  both partial events are threshold-sensitive, and the loose set adds one
  candidate not promoted into the primary result
- ESP32 power corroborates real aggregate loss/rejoin, but frequency behavior
  is non-discriminating because the same excursions and rolling forensic text
  appear in controls. No ESP32 availability transition occurred. Events 01 and
  03 have larger near-anchor voltage excursions than controls
- Trusted JK BMS context shows four zero-output events at 99% combined SOC and
  several charging-to-discharging reversals, but another zero-output event at
  88% SOC weakens a simple full-battery-only explanation. Battery reversal may
  also be a consequence of lost solar production
- A detailed read-only Battery 1/Battery 2 review found event-anchor cell
  spreads of 2–10/1–8 mV, capture maxima of 24/19 mV, and highest reported
  cells of 3.501/3.494 V. No positive JK cell-overvoltage signature was found.
  Missing MOS, balancing, protection/alarm, individual-cell, and charge-limit
  topics prevent absolute exclusion of an unobserved transient, but existing
  telemetry poorly supports JK protection for any event and does not support it
  as a common explanation for all seven
- Aggregate evidence cannot distinguish cloud/irradiance variation, inverter
  AC-couple control behavior, microinverter response, irradiance variation, or
  a sub-second AC disturbance, nor can it identify an individual microinverter.
  Owner review must decide whether a targeted measurement adds enough
  independent evidence to justify its cost and risk
- `esp32-frequency-v1` remains the current policy. The separate
  `esp32-conservative-v1` output is an explicit canary evaluation only
- Home Assistant is a separate VM on the Proxmox host at static
  `192.168.3.15/24`; gateway/DNS are `192.168.3.1`, IPv6 is disabled, and its
  malformed prior static profile was repaired through temporary DHCP before
  assigning `.15`. Reverify versions before compatibility-sensitive work
- SolarAssistant remains at `192.168.3.12`, connects directly to both JK BMS
  units over RS-485, is not connected to the EG4 inverter, and remains the
  trusted battery source
- Home Assistant MQTT was corrected from stale broker `192.168.3.231` to the
  SolarAssistant broker `192.168.3.12:1883`; MQTT remains 3.1.1 because that
  broker did not support the requested MQTT 5 migration. HA's Mosquitto add-on
  was installed but port 1883 on `.15` was closed and it was not the active LAN
  broker at discovery. No broker migration is selected
- HA EG4 Web Monitor was functioning with approximately 3 devices/115 entities
  through the EG4 cloud account; `Manage Local Devices` showed none. It is a
  second presentation of the same upstream cloud source as the solardt EG4
  collector, not independent evidence, and its writable controls remain
  unauthorized
- A bounded two-hour Home Assistant REST capture completed normally with 7,200
  successful one-second `GET /api/states` snapshots and zero errors. Local
  allowlist filtering was proven, but polling cadence differed sharply from
  source cadence: Radiator 1/2 had only 52/32 distinct `source_last_updated`
  timestamps. Reusable method and safety boundaries are recorded in
  `docs/EG4_HOME_ASSISTANT_TELEMETRY.md`
- The cooling-control analysis found eight Radiator 1 temperature-cycle
  episodes under both 5- and 10-minute grouping rules. Radiator 1/2 ranges were
  59–72/47–51 °C; each high episode's next source update was below 68 °C
  about 121 seconds later. Coarse endpoint rates of approximately −4.0 to
  −6.0 °C/min are source-resolution-limited. No fan telemetry was available,
  and no fan operation or causation was inferred. Further fan instrumentation
  is deferred until after primary milestones
- Provenance for the capture remains `Home Assistant → EG4 Web Monitor hybrid
  mode`; local-dongle versus cloud lineage is unproven per entity. Home
  Assistant, SolarAssistant, and direct-EG4 values must remain separately
  identified, with `solardt` as the authoritative aggregation/provenance layer
- HA directly integrates `EG4 Forensic Probe v3` at `192.168.3.13`, with
  approximately 21 entities; an old frequency dashboard has stale/missing
  references. Do not remove it until reboot behavior and the preferred
  `ESP32 -> solardt -> selected read-only HA exports` path are proven
- The existing EG4 Wi-Fi dongle was observed at `192.168.3.20:8000`, MAC
  `d8:3b:da:21:92:c8`. Public-source research is documented in
  `docs/EG4_LOCAL_DONGLE_INVESTIGATION.md`; no LAN request was sent. The
  prepared `dongle -> solardt -> HA` path remains separately gated after
  capture analysis because the protocol is control-capable and single-client
  coexistence is unresolved
- Repository health check script operational
- status.sh runs repository health check script at startup
- AI engineering framework MVP boundary design documented
- EG4 collector operational
- Raw evidence files are authoritative source material; reports and interfaces are derived consumers
- SQLite normalized history and query layer operational for EG4
- SolarAssistant and ESP32 remain standalone NDJSON collectors and are not yet normalized into SQLite
- Evidence capture operational
- CSV report generation operational
- EG4 collector/report MVP complete
- EG4 local portal generator operational
- Dedicated local portal selected as the primary engineering interface
- Browser smoke test passed on LAN
- EG4 local portal systemd service enabled and verified with HTTP 200
- Automated EG4 refresh timer enabled on a 15-minute schedule
- Unattended EG4 refresh verified successfully through systemd
- VM timezone set to America/Chicago for correct EG4 calendar-day collection
- solardt Chrony service synchronized to upstream NTP sources
- solardt LAN NTP server bound to 192.168.3.11:123
- NTP access restricted to the 192.168.3.0/24 LAN
- External NTP response verified successfully from WS01
- Portal browser freshness verified: cache-discouraging HTML metadata and a 60-second cache-busting reload are present
- Portal timestamps normalized to Central time
- Portal independently classifies Runtime, Energy, and Day Telemetry freshness with adjustable 30-minute thresholds
- Portal suppresses stale, missing, invalid-timestamp, and future-dated source values instead of displaying them as current
- System Status and EG4 Estimated SOC depend on fresh Runtime; Today Usage depends on fresh Energy; AC-couple and Load depend on fresh Day Telemetry
- Portal source-health and card-protection behavior covered by focused offline tests; not live-browser reverified in this work unit
- Portal Load gauge uses day_multiline_samples.csv consumption_w
- Current local portal is EG4-only; trusted JK BMS and ESP32 values are not yet portal inputs
- status.sh repository health checks operational
- Required-file, duplicate-heading, and documentation-drift checks tested
- SolarAssistant normal persistent polling target is 10 seconds; the current 1-second default remains available for manual diagnostics
- Topic-specific change retention and heartbeat policy documented
- ESP32 frequency observed at one-second cadence with an initial 0.04 Hz storage deadband
- Approved ESP32 observations are preserved continuously in raw NDJSON; rolling buffers and automatic pre-event, event, and post-event preservation remain planned
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
- The custom SolarAssistant root-bootstrap experiment was reviewed and
  superseded before installation; its complete uncommitted state is preserved
  outside the repository at
  `/home/chris/solar-digital-twin-backups/20260715-212729-superseded-solarassistant-credential-bootstrap`
- Project security direction now follows a practical Home Assistant-style
  trusted-host model, with future OPNsense VLANs and firewall rules planned as
  the primary network-containment boundary
- The SolarAssistant credential is installed at the protected approved path;
  its value and derivatives remain outside Git, documentation, chat, command
  arguments, and shell history under the practical Home Assistant-style trusted-host model
- Project-wide runtime identity, credential isolation, unknown-authority,
  authentication-failure, network-containment, and recovery decisions are approved
- ESP32 SSE may use a shared telemetry identity; SolarAssistant and EG4 remain
  separately isolated until their credentials are proven technically read-only
- HTTP `401` or `403` stops automated authentication attempts; operator
  correction and one manual verification are required before automation resumes
- SolarAssistant runtime paths and metadata are installed and verified;
  device-specific recovery details remain pending
- Practical offline SolarAssistant collector hardening may resume without
  implementing credentials or performing authenticated live work
- Commit `c7370ca` completed SolarAssistant authentication hardening: HTTP
  `401`/`403` stop without retry or backoff, use a fixed credential-free message
  and exit status 1, and temporary failures retain bounded exponential backoff
- Every received SolarAssistant HTTP response now closes on success and failure
  paths; raw NDJSON behavior remains unchanged
- SolarAssistant focused offline tests passed (6), the full suite passed (43),
  and the repository health check passed for commit `c7370ca`
- The first separate SolarAssistant retained-output implementation is complete;
  SQLite, portal, and systemd integration remain deferred
- Commit `4e069bb` implemented a separate derived SolarAssistant retained NDJSON
  stream while preserving complete raw evidence and unchanged polling traffic
- Raw records are written and flushed before retained processing; retained
  records preserve observation fields and add `retention_reason`
- Combined, Battery 1, and Battery 2 SOC retain exact changes plus a 300-second
  monotonic heartbeat
- Approved state-of-health, capacity, charge-capacity, and cycle topics retain
  exact changes plus an 86,400-second monotonic heartbeat
- Retention state is independent per stable metric identity; authentication,
  backoff, duration, response closure, interruption, filtering, and credential safety remain unchanged
- Retained-output tests passed (9), existing SolarAssistant tests passed (6),
  shared retention tests passed (14), the full suite passed (52), and repository checks passed
- Voltage, current, power, cell voltage, cell imbalance, and temperature remain
  complete in raw evidence but intentionally absent from retained output pending approved deadbands
- Commit `dc1adc9` completed an offline, raw-only SolarAssistant deadband
  assessment using two files, 294 valid records, and seven observations per
  stable metric identity; no invalid records were found
- Receipt-time coverage was about 3 minutes 47 seconds, but active capture was
  only about 7.4 seconds across two short runs; it did not adequately represent
  broad charging, discharging, idle, transition, thermal, voltage, or near-full
  cell behavior
- Before-and-after evidence metadata manifests matched exactly; no evidence was
  modified, created, renamed, or deleted
- The assessment full suite passed (52), `git diff --check` passed, and the
  repository health check passed
- No numeric deadband was proposed, approved, implemented, or activated;
  combined, Battery 1, and Battery 2 may ultimately require different thresholds
- The dedicated SolarAssistant runtime, credential, and manual authenticated
  verification are complete under the approved separate-identity and
  credential-isolation model
- The controlled 24-hour raw and retained capture completed normally;
  persistent service operation remains a separate later stage
- Commit `39548b1` completed the repository-side dedicated SolarAssistant
  runtime preparation using the fixed `solardt-sa:solardt-sa` non-login system
  identity, administrator-owned `/opt/solar-digital-twin` runtime, protected
  `/etc/solar-digital-twin/solarassistant/password`, and writable
  `/var/lib/solar-digital-twin/solarassistant/evidence` design
- The collector now supports `--password-file` before the existing environment
  and private prompt sources, plus `--output-dir`; invalid local credential
  files and output-directory preparation fail before device polling
- The committed runtime installer provides non-privileged `--check`, later
  privileged installation, and metadata-only `--verify`; the separate
  credential installer provides hidden confirmed entry and atomic replacement
- Focused collector and retention tests passed (37), the full suite passed (60),
  both scripts passed `bash -n` and non-privileged checks, password-like
  arguments were rejected, and repository checks passed
- The committed runtime installer was run manually from the normal `solardt`
  terminal with private `sudo` authentication. It installed the non-login
  `solardt-sa:solardt-sa` identity, administrator-owned
  `/opt/solar-digital-twin` runtime, protected credential boundary, and writable
  `/var/lib/solar-digital-twin/solarassistant/evidence` boundary
- Runtime verification completed with: `VERIFY: SolarAssistant runtime metadata
  and access boundaries passed`
- The committed credential installer was run manually with private controlling-
  terminal entry and installed the password with approved metadata. No password
  or derivative was placed in Git, documentation, chat, command arguments, or
  shell history
- A one-time authenticated collector verification ran as `solardt-sa` through
  the dedicated runtime using the protected password file and dedicated
  `/var/lib` evidence output at a 10-second interval for 25 seconds. It stopped
  cleanly without authentication rejection
- The run wrote 126 approved raw records and created a separate retained NDJSON
  file. Raw receipt times covered `2026-07-16T05:41:34.125Z` through
  `2026-07-16T05:41:55.129Z`, representing approximately three successful polls
- The short point-in-time verification confirmed expected combined, Battery 1,
  and Battery 2 telemetry: SOC, state of health, voltage, current, power,
  capacity, charge capacity, cycles, cell voltages and imbalance, battery and
  sensor temperatures, and MOS temperature
- Representative point-in-time values were 78% combined SOC, 79% Battery 1
  SOC, 77% Battery 2 SOC, and 53.3/53.4/53.2 V combined/Battery 1/Battery 2;
  combined current and power were zero during this short window. These values
  are not a long-term operating characterization
- No systemd service was created or enabled during the short verification
- Verified current state on 2026-07-16: the dedicated runtime is installed
  under `/opt/solar-digital-twin`, and the administrator-controlled credential
  remains protected outside Git
- The 24-hour SolarAssistant capture covered `2026-07-16T07:00:43.194Z`
  through `2026-07-17T07:00:41.713Z` (86,398.519 seconds of the requested
  86,400), completed 8,219 polls and 345,198 raw records, and stopped normally
  with `stopped_early: false`. It passed with the permissions qualifications
  recorded in `docs/SOLARASSISTANT_TELEMETRY_PLAN.md`
- The read-only monitor remains running as `solardt-sa` in the
  root-owned detached tmux session `solarassistant-monitor` at
  `http://192.168.3.11:8792`; its health endpoint returned `{"status":"ok"}`.
  It reports capture state `Complete` and expected post-capture freshness
  `Stale`; the collector is no longer running
- Collector PID 92638 and monitor PID 92674 were historical observations only;
  PIDs are transient and are not stable runtime configuration
- The installed monitor badge correction remains committed and pushed but not
  deployed. Any monitor update or restart requires separate explicit approval
- During read-only completion inspection, an in-memory abort-control token field
  was inadvertently included in command output. It was not used, the completed
  capture had Abort disabled, and no credential was accessed. Before a future
  abort-capable capture, a separately approved monitor restart must rotate it;
  the token value and sensitive output are not repository material
- Commit `a227b68` reproduced the badge defect offline: bare JavaScript
  `status` resolved to the browser-provided `window.status` value instead of
  the intended badge element
- The correction explicitly binds the intended status element and uses it for
  normal rendering and fetch-error fallback. Its regression test prevents
  reintroduction of bare `status.textContent`
- Focused monitor tests passed (27), and the full suite passed (87). Backend
  status semantics and read-only monitor behavior were unchanged
- Explicit battery-topic allowlist manually verified
- UTC-stamped ignored NDJSON evidence manually verified
- Combined, Battery 1, and Battery 2 telemetry verified
- Clean interruption verified during password prompt and active collection
- Project published to GitHub

- The standalone Solar Digital Twin portal prototype remains synthetic-only,
  offline, and separate from the operational EG4 portal and all collectors
- The accepted Overview order is Solar vs house load, Volcast forecast, System
  health, and Current AC source; the Battery bank row is Battery SOC, Battery
  voltage, Battery current, and Battery cell voltage
- Functional synthetic source-data tabs now cover EG4, SolarAssistant, ESP32,
  and Volcast while documenting that production `Show all` views must preserve
  every parsed, non-secret, read-only parameter
- The current Battery cell voltage prototype uses two enlarged open-arc dials,
  red endpoint stops, yellow caution ends, a dominant green normal region,
  Avg/Max/Min and differential values, and four independent normal/alarm state
  structures
- The visually ambiguous moving inner green cell-voltage indicator has been
  replaced in the synthetic prototype with short white Avg, red Max, and blue
  Min scale markers plus an authoritative dynamic digital readout
- `docs/PORTAL_UI_DESIGN.md` is the authoritative portal design record;
  `docs/chat_ideas/README.md` is a non-authoritative holding area for deferred,
  open, and superseded design ideas
- The temporary synthetic preview is expected to remain available at
  `http://192.168.3.11:8793/solar_portal_mockup.html` for browser review; this
  repository checkpoint does not authorize or modify that server
- The validated portal prototype, focused tests, and design documentation were
  committed and pushed as commit `acfbaf5`

- Repomix evaluation stopped as an active task; Repomix remains only an optional future architecture-audit tool.
- Codex CLI installation and ChatGPT authentication successfully validated on `solardt`.
- Native Bubblewrap/AppArmor sandboxing, workspace-write mode, and explicit approval boundaries successfully validated.
- First bounded Codex coding workflow completed successfully.
- Existing ESP32 raw NDJSON filename and record stream remain intact as complete approved raw evidence.
- Separate selectively retained ESP32 NDJSON output implemented with the documented 0.04 Hz frequency deadband and 30-second heartbeat.
- ESP32 collector-level offline tests and repository health checks passed; the retained stream was subsequently verified by the completed 12-hour capture.
- The fixed 12-hour ESP32 forensic capture launched successfully at
  `2026-07-16 13:05:13 America/Chicago` as unprivileged user `chris` in detached
  tmux session `esp32-forensic-12h`
- It was configured for 43,200 seconds and stopped automatically after
  43,199.774 seconds of receipt-time coverage
- Collector PID 107886 was a transient historical observation, not stable
  runtime configuration
- The capture's raw evidence path is
  `/home/chris/solar-digital-twin/evidence/esp32/esp32_sse_20260716_180514Z.ndjson`;
  its derived retained sibling is
  `/home/chris/solar-digital-twin/evidence/esp32/esp32_sse_20260716_180514Z_retained.ndjson`
- The completed ESP32 window was `2026-07-16T18:05:14.599Z` through
  `2026-07-17T06:05:14.373Z`: 431,513 raw records and 394,327 retained records,
  zero malformed or truncated records, no backward timestamps, a 1.102-second
  largest raw gap, and approximately 1.001-second median primary cadence. All
  17 approved public entity IDs and no unapproved IDs were present
- The ESP32 capture passed. Its retained/raw ratios were approximately 91.38%
  by line and 95.77% by byte; interpretation and any tuning recommendation are
  now recorded in `docs/ESP32_RETENTION_ASSESSMENT.md`, with raw evidence authoritative
- The streaming assessment reproduced 394,327 retained records and 149,568,755
  bytes exactly. Frequency retained 13.81%; every non-frequency entity retained
  100% by documented pass-through design. No implementation defect was found
- A conservative offline candidate estimated 61,724 records and 36,174,692
  bytes. Deterministic replay confirmed those exact totals and accepted the
  candidate for a separate implementation plan; current production behavior
  remains unchanged
- Raw, current-retained, and conservative-candidate streams preserved the same
  partial-collapse and two zero-output classifications, high confidence, and
  stable no-event control. All 17,687 full-capture binary/text transitions were
  identical; UTC chronology, entity identity, and provenance were preserved
- The candidate retained 14.304% of raw records and 23.163% of raw bytes,
  reducing the current retained stream by 84.35% by records and 75.82% by
  bytes. `docs/ESP32_RETENTION_REPLAY.md` records the evidence, limitations,
  acceptance criteria, and Adopt decision
- `docs/ESP32_RETENTION_PRODUCTION_PLAN.md` defines `esp32-conservative-v1`,
  one-process independent current/candidate writers, versioned output and
  manifest provenance, a 12-hour daytime canary, non-destructive rollback,
  post-capture verification, and 14 production acceptance gates
- The rollout is explicitly phased: repository implementation without live
  activation, separately approved three-output canary, offline canary analysis,
  and only then an owner-reviewed future policy transition. Current production
  retention and raw evidence behavior remain unchanged
- The complete ESP32 window overlaps SolarAssistant, both use compatible
  `solardt` UTC receipt timestamps, and no clock reversal or timezone conflict
  was found. Later offline correlation is supportable, but matching EG4 evidence
  availability has now been established as Complete
- EG4 overlap contains 177 unique day-series samples from `2026-07-16 13:08:14`
  through `2026-07-17 01:04:08` Central and 47 runtime snapshots. Median
  cadences are 241 and 903 seconds; the largest gaps are 724 and 960 seconds,
  with no gap over 20 minutes and no malformed overlap JSON
- EG4 day times are cloud-returned Central source timestamps; runtime
  `server_time` is UTC, `device_time` is Central, and `captured_at` is Central
  collector provenance. A three-point check aligned ESP32 UTC receipts to
  nearest EG4 day samples within 36-66 seconds
- The bounded correlation plan is authoritative in
  `docs/EG4_FORENSIC_CORRELATION.md`. The completed SolarAssistant raw and
  retained filenames were verified through a least-privilege read-only access
  model; credentials, tokens, protected logs, and unrelated runtime files
  remain restricted
- The pure offline three-source analyzer is implemented at
  `src/solar_digital_twin/analysis/forensic_correlation.py`. It normalizes
  explicit source timestamp semantics to UTC, preserves provenance, aligns
  nearest source context without interpolation, detects configurable partial
  collapse and zero-output candidates, and reports explainable confidence
  factors without claiming causation
- Seventeen focused synthetic analyzer tests cover abrupt and gradual shapes,
  missing and out-of-tolerance sources, timezone offsets, EG4 cadence gaps,
  availability and frequency context, multiple events, separate trusted and
  estimated SOC roles, input immutability, and reduced ESP32 context. No real
  evidence, operational database, or protected path was used
- Pure read-only adapters now stream explicitly bounded EG4 day/runtime SQLite,
  grouped SolarAssistant raw NDJSON polls, and ESP32 raw/retained NDJSON into
  source-labeled correlation records. SQLite is opened with URI read-only mode
  and query-only enforcement; malformed NDJSON diagnostics omit payload text
- Synthetic end-to-end validation preserves trusted SolarAssistant SOC versus
  estimated EG4 SOC, explicit timestamp semantics, availability, provenance,
  missing context, and input immutability. No operational input was opened
- The analyzer materializes its supplied records for deterministic ordering.
  A real bounded-memory workflow must therefore detect candidate EG4 windows
  first and supply only bounded high-rate source windows
- The real-data dry run used bounded read-only windows and verified source
  hashes before and after analysis. It validated real EG4 naive-UTC runtime
  timestamps, SolarAssistant grouped polls, ESP32 raw/retained context,
  independent availability transitions, actual alarm/event descriptions, and
  correct partial-collapse versus zero-output classification. No source was
  modified and cloud cover remains an alternative explanation
- Trusted read-only SolarAssistant telemetry analysis may use the established
  least-privilege reader path without repeated administrator intervention.
  Credentials, authorization data, tokens, protected logs, unrelated runtime
  files, and write access remain restricted
- Governance now defines Chris as project owner and system operator, ChatGPT as
  proactive project lead and technical engineering partner, and Codex as the
  bounded local implementation agent. `CONTRIBUTING.md` contains the coherent
  risk, approval, archive-first, audit, commit, and milestone-push policy
- `docs/operations/VM_HEALTH_LOG.md` now defines the read-only 30-day and
  event-driven VM health schedule, capacity thresholds, append-only health
  entries, and prohibition on automatic remediation or evidence deletion
- The initial read-only `solardt` VM health baseline was measured at
  `2026-07-18T03:52:24Z` and classified **Normal**: root filesystem use 17%,
  inode use 4%, 2.2 GiB memory available, negligible two-CPU load, systemd
  running with no failed units, and no observed filesystem/I/O/out-of-space
  warning. No remediation was performed; repeat within 30 days and at the
  documented event-driven checkpoints
- The ESP32 collector now identifies the existing default retained policy as
  `esp32-frequency-v1` and implements the adopted `esp32-conservative-v1`
  policy with exact documented deadbands, a 60-second heartbeat, and independent
  per-entity availability state
- Explicit opt-in canary mode uses one SSE stream to write authoritative raw,
  current retained, and versioned conservative retained outputs. The current
  policy and historical retained filename remain the default; conservative
  output is not created without explicit selection
- New capture outputs use exclusive creation, and a separate append-only
  manifest records capture, collector-version, mode, policy, output, and final
  completion/interruption/failure provenance without changing telemetry records
- Retained writers have independent policy and failure state. Raw write and
  flush remain first and authoritative; one retained failure does not disable
  raw or the other retained writer
- Synthetic coverage verifies unavailable entry and restoration, including a
  restoration equal to the last pre-unavailable numeric value. No real
  availability transition has yet been observed, and no deployment or live
  canary was performed
- Coordinated capture orchestration now isolates ESP32, EG4, and SolarAssistant
  evidence beneath one capture ID, records append-only common provenance,
  enforces approximately 24 hours, and restores only previously active
  competing EG4 units. It preserves native source formats and production data
- ESP32 now accepts an explicit output directory without changing its default
  path or policy. The coordinated run uses explicit canary mode; normal
  `esp32-frequency-v1` behavior remains the production default
- The coordinated milestone supersedes the earlier 12-hour ESP32-only canary
  with an authorized 24-hour common interval covering nighttime, sunrise,
  daytime, sunset, and post-sunset context. Controlled closure and restoration
  are verified; immutable inventory and analysis remain the next work unit,
  and cloud cover remains an alternative explanation
- The first coordinated startup (`solar-forensic-20260718T055952Z`) failed
  safely because its SolarAssistant child was forced to primary group `chris`
  and therefore could not read the protected `root:solardt-sa` credential.
  Automatic cleanup stopped all three children, preserved the failed run and
  append-only manifest, and restored `eg4-refresh-report.timer` to its prior
  active state. The coordinator now launches SolarAssistant with the normal
  `solardt-sa` identity; the next launch must use a new capture identifier
- Commit `b88941d` is pushed to `origin/main`; `main` was clean and synchronized
  before the governance reset

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
- Push clean milestone commits under project-lead direction and verify sync.
- Engineering Bible is the design authority.
