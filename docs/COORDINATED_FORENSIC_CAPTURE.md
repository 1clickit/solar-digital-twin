# Coordinated Three-Source Forensic Capture

## Status and purpose

Capture `solar-forensic-20260718T062127Z` is closed. It was intentionally
stopped through its coordinated transient service after approximately 21 hours
15 minutes, after covering nighttime battery discharge, sunrise, the complete
daytime production/charging cycle, sunset, and return to nighttime. The final
manifest reported `capture_terminal`, state `interruption`, reason `signal`,
normal SIGTERM shutdown of all three children, and
`restoration_success: true`. This controlled interruption is not a failure.

Post-closure verification found the coordinated transient unit inactive,
`eg4-refresh-report.timer` active/enabled,
`eg4-refresh-report.service` inactive/static as normal between timer runs, and
`eg4-local-portal.service` active/enabled. Compact observations reported no
recent error, approximately 7.06 MB EG4, 605 MB ESP32, and 72.5 MB
SolarAssistant evidence, with approximately 64.8 GB free. Exact inventory,
hashes, parse/newline integrity, counts, cadence/gaps, reconnects, and analysis
remain outstanding. All evidence is immutable.

The operational milestone was one isolated approximately 24-hour maximum
read-only capture spanning ESP32, EG4, and SolarAssistant. It was designed to
cover nighttime baseline, sunrise, daytime production, sunset, and post-sunset
battery/load behavior on one UTC timeline. Correlation can strengthen or
weaken hypotheses, but cloud cover, load changes, battery constraints,
communications gaps, and telemetry timing remain alternative explanations; the
capture alone does not establish equipment causation.

The repository coordinator is `scripts/coordinated_capture.py`. It keeps native
source evidence separate under one capture directory and binds lifecycle and
provenance with an append-only top-level manifest. It never combines telemetry
records into one monolithic format.

## Isolated outputs

The live root is `/var/lib/solar-digital-twin/coordinated`. Each run uses the
exclusive identifier and directory:

`solar-forensic_<UTC start>` is not used. The canonical form is
`solar-forensic-YYYYMMDDTHHMMSSZ`.

Each run contains:

- `coordinated_manifest.ndjson`: append-only common lifecycle and provenance;
- `esp32/`: full raw, `_retained.ndjson` (`esp32-frequency-v1`),
  `_retained_esp32-conservative-v1.ndjson`, the ESP32 append-only manifest, and
  a bounded collector log;
- `eg4/`: isolated `eg4_capture.sqlite`, immutable per-poll JSON evidence,
  isolated reports, capture config, and collector log; and
- `solarassistant/`: authoritative raw and existing retained NDJSON plus a
  bounded collector log.

All capture outputs are new. Existing evidence and the production EG4 database
are never appended to, copied, migrated, normalized, renamed, or rewritten.
The ESP32 outputs use exclusive creation. The common run directory and manifest
also use exclusive creation.

## Source behavior

- **ESP32:** one read-only SSE connection, explicit `canary` mode, raw write
  first, current and conservative retained writers with independent state, and
  the committed collector version in source provenance. The normal default
  remains `esp32-frequency-v1` and is not retired.
- **EG4:** one isolated read-only sync approximately every 15 minutes using a
  generated capture config, dedicated database/evidence/reports, and
  `--skip-set-records`. No remote-setting method is called.
- **SolarAssistant:** the installed approved collector runs as `solardt-sa`,
  reads the existing protected password file without exposing it, uses the
  normal 10-second interval, and writes to its isolated source directory.

The SolarAssistant child must use the normal `solardt-sa` user and group
identity. Do not force group `chris`: doing so removes the service identity's
group access to its protected credential. The preserved first startup attempt,
`solar-forensic-20260718T055952Z`, demonstrated this failure mode and then
cleanly stopped all children and restored the prior EG4 timer. Relaunch only
with a new capture identifier after the corrected identity path validates.

The coordinator reads the existing EG4 environment file only in the privileged
live process and passes its two required values through a child environment,
never through arguments, logs, manifests, reports, or Git. No credential is
modified.

## Competing writers and restoration

Before launch, inventory and record the loaded, active, and enabled state of:

- `eg4-refresh-report.timer`;
- `eg4-refresh-report.service`; and
- `eg4-local-portal.service`.

The refresh timer/service are competing EG4 writers and are stopped gracefully
when active. Their enabled state is not changed. The static EG4 portal may
remain running because it serves generated HTML and does not collect or modify
telemetry. The SolarAssistant monitor may remain running because it reads the
completed older capture and makes no device request or evidence write. No
active SolarAssistant or ESP32 collector may coexist with this run.

In a `finally` path, the coordinator stops only its three process groups,
closes/preserves their outputs, appends terminal records, and restarts only
units recorded active before capture. It never enables a unit or starts a unit
that was previously inactive. Partial startup evidence is preserved. A source
startup failure aborts all-source startup and restores prior units. After
startup, a source process exit, free space below 5 GiB, signal, or other
integrity failure produces a controlled stop and restoration.

## Preflight and capacity gates

Immediately before launch verify:

- repository clean, synchronized, and at the reviewed implementation commit;
- no coordinated-capture lock or duplicate collector;
- systemd healthy for relevant units and exact prior states recorded;
- UTC synchronization healthy and operator timezone `America/Chicago`;
- root storage and inodes healthy, at least 10 GiB free, and at least ten times
  projected total capture size free;
- memory, CPU, and load have practical headroom;
- capture root writable by the privileged supervisor and target run absent;
- EG4 environment file and SolarAssistant password file readable by their
  approved live paths without displaying contents;
- exactly one known launch/stop path per source; and
- focused/full tests, repository checks, and shortened synthetic rehearsal
  passed.

The prior 12-hour evidence rates project well below 1 GiB for this run; use the
measured preflight value rather than that estimate as the controlling gate.
Five GiB free is the controlled-stop threshold. Storage pressure never
authorizes evidence deletion.

## Launch contract

Generate `CAPTURE_ID=solar-forensic-$(date -u +%Y%m%dT%H%M%SZ)` after the
implementation commit is pushed. Launch one transient root service named
`solar-coordinated-${CAPTURE_ID}.service`, with `Type=simple`, a 120-second stop
timeout, the repository as working directory, and this command:

`/home/chris/solar-digital-twin/.venv/bin/python /home/chris/solar-digital-twin/scripts/coordinated_capture.py live --capture-id ${CAPTURE_ID} --capture-root /var/lib/solar-digital-twin/coordinated --repo /home/chris/solar-digital-twin --commit $(git rev-parse HEAD) --duration 86400 --eg4-interval 900 --startup-timeout 300 --minimum-free-bytes 5368709120 --eg4-environment-file /etc/solar-digital-twin/eg4.env --solarassistant-password-file /etc/solar-digital-twin/solarassistant/password`

The complete supervisor launch is `sudo systemd-run
--unit="solar-coordinated-${CAPTURE_ID}" --property=Type=simple
--property=WorkingDirectory=/home/chris/solar-digital-twin
--property=TimeoutStopSec=120 --collect` followed by the command above. Keep the
capture identifier in the unit name; do not reuse an earlier identifier.

The transient unit must survive SSH disconnection. It automatically enforces
duration, signal propagation, evidence closure, append-only terminal provenance,
and exact prior-unit restoration. The unit name, capture ID, actual start/end,
source PIDs, paths, policy IDs, prior units, warnings, terminal state, and
restoration results are recorded in the common manifest.

## Initial verification and monitoring

Allow up to five minutes for all sources to prove startup. The coordinator
requires a live child for each source and these artifacts:

- four ESP32 NDJSON artifacts;
- SolarAssistant raw and retained NDJSON; and
- EG4 isolated SQLite plus JSON evidence.

Failure triggers preserved partial evidence and automatic restoration. After
startup, use the compact read-only status interface; it reports capture ID,
elapsed/remaining time, planned end, source process state, source byte totals,
free space, manifest state, and only a bounded recent error summary. It never
prints telemetry or credentials.

The manual rescue action is to stop the one transient coordinated-capture unit.
Systemd sends `SIGTERM`; the coordinator's cleanup path stops its child process
groups, appends terminal state, and restores only prior active units. Do not
kill children individually unless a later recovery work unit proves the
supervisor is unavailable. Do not delete partial evidence.

The compact status invocation is `.venv/bin/python
scripts/coordinated_capture.py status --run-dir
/var/lib/solar-digital-twin/coordinated/${CAPTURE_ID}`. The manual rescue
invocation is `sudo systemctl stop solar-coordinated-${CAPTURE_ID}.service`.

Contact ChatGPT before intervening if a source is not running, output growth
stops or becomes excessive, rapid reconnects persist, the manifest reports an
error, free space approaches the 5 GiB threshold, timestamps become implausible,
restoration occurs before the planned end, or device operation appears affected.

## Completion and analysis

After automatic or controlled completion, verify terminal/restoration manifest records, prior
unit states, filenames, times, sizes, hashes, newline/parse integrity,
timestamps, cadence, gaps, approved entities, and source errors. Preserve all
outputs. Then perform bounded offline three-source correlation and raw/current/
conservative ESP32 comparison. Do not retire `esp32-frequency-v1` based only on
capture completion; production acceptance gates and an owner-reviewed later
transition remain required.

This runbook authorizes no device control, firmware/configuration change,
database migration, evidence deletion, credential change, production-default
change, or unsafe event induction.
