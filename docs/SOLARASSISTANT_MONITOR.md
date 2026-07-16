# SolarAssistant Live-Capture Monitor

## Purpose and status

The SolarAssistant live-capture monitor is a lightweight temporary LAN
dashboard for observing a controlled evidence capture. It is the separate
standard-library module
`solar_digital_twin.reporting.solarassistant_monitor`; it does not change or
run inside the collector. Repository implementation and offline testing are
complete. The monitor is installed and running as `solardt-sa` in root-owned
detached tmux session `solarassistant-monitor` at
`http://192.168.3.11:8792`; its health endpoint returned `{"status":"ok"}`.

No systemd service is included. Integration into the primary project portal
remains deferred.

The running monitor may continue to display an `Unknown` status badge despite
fresh data. This is not a capture blocker. Commit `a227b68` reproduced the
defect offline: bare JavaScript `status` resolved to the browser-provided
`window.status` value instead of the intended badge element. The correction
explicitly binds that element and uses it for normal rendering and fetch-error
fallback. A regression test explicitly rejects bare `status.textContent`.
Focused monitor tests passed (27), and the full suite passed (87). Backend
status semantics and read-only monitor behavior were unchanged. The commit is
pushed but has not been deployed to the active monitor. Its PID was observed as
92674, but PIDs are transient observations and not stable runtime configuration.

## Data flow and in-memory operation

Raw SolarAssistant NDJSON remains authoritative. The monitor reads the selected
raw file once at startup, builds its state in memory, remembers the byte offset,
and then reads only newly appended complete lines. It never opens evidence for
writing and never truncates, touches, renames, or deletes raw or retained
evidence. A temporarily incomplete final line waits for completion; a malformed
complete line increments the invalid-line count without stopping monitoring.

Without `--raw-file`, the newest `solarassistant_*.ndjson` file that is not a
`_retained.ndjson` file is selected. If none exists, the monitor safely shows
`No capture data yet` and waits. An explicit raw file must be inside the
configured evidence directory and cannot be a retained file.

The monitor keeps these derived values in memory:

- latest record per stable topic identity;
- latest completed polling snapshot;
- raw and retained complete-record counts and raw byte size;
- distinct poll and invalid-line counts;
- first and latest receipt times;
- numeric minimum and maximum per topic;
- reliably observed receipt gaps;
- countdown and freshness state;
- safely identified collector PID and Linux process-start identity.

The retained sibling is used only for an incrementally maintained record count.
It is not a telemetry source. The monitor does not read the SolarAssistant
credential, password file, environment credential, or device API.

## Complete polling snapshots

All records from one collector response share one receipt timestamp. A browser
snapshot is published atomically when a different receipt timestamp begins. If
no next timestamp has arrived, a pending poll is published after 0.75 seconds
without a new record. During startup, the final complete historical timestamp
group is published after the one-time read. An incomplete final NDJSON line is
not part of a snapshot until its newline arrives.

The dashboard can show that a newer poll is still being assembled. It never
mixes a partially received new poll into the completed snapshot on display.

## Dashboard

The responsive page is self-contained and loads no remote scripts, fonts,
tracking, or other internet assets. It shows Combined, Battery 1, and Battery 2
telemetry with prominent SOC, voltage, current, power, state of health, battery
temperature, average/highest/lowest cell voltage, and cell imbalance values.
Capacity, charge capacity, cycles, temperature sensors, and MOS temperature are
also shown. Missing values say `Waiting for data` or `Not reported`; zero is
preserved as a real observation.

Capture details include raw and retained filenames and counts, poll count,
invalid-line count, raw size, capture start, latest poll, expected completion,
freshness, and whether a newer poll is being assembled. The browser requests
sanitized state from `GET /api/status` about every two seconds without reloading
the page. Other explicit endpoints are `GET /`, `GET /report`, `GET /health`,
and `POST /api/abort`; arbitrary file serving is unavailable.

All responses prohibit caching and include a restrictive Content Security
Policy, `nosniff`, and no-referrer policy. Evidence-derived text is escaped
before insertion into generated HTML.

## Countdown and capture status

The first valid receipt timestamp is the capture start. The default planned
duration is 86,400 seconds. The upper-right panel shows elapsed time, remaining
`HH:MM:SS`, expected completion, and progress. Remaining time reaches zero and
stays at zero. If a previously identified collector exits before completion,
the page reports `Capture stopped with HH:MM:SS remaining`.

Status distinguishes Fresh, Stale, Stopping, Stopped, Complete, Running, and
Unknown using receipt age, countdown state, and safe process observation. The
default freshness threshold is 30 seconds.

## Report behavior

The Report button opens an on-demand HTML report made only from current
in-memory state. It does not stop or pause collection and writes no report
file. The report includes generation time, capture status and countdown,
capture start and expected end, evidence filenames and counts, poll and invalid
counts, receipt-time range, current values, numeric ranges, freshness, and
reliably observed receipt gaps. It excludes credentials, environment variables,
authorization data, request headers, and entire NDJSON records.

## Abort safety model

Abort Capture is separate from monitor shutdown. The browser first confirms
that existing evidence is preserved, no data is deleted, and only the current
capture will be stopped. The request is POST-only and requires same-origin
validation plus an unpredictable in-memory token generated at monitor startup.

Abort is enabled only when `/proc` inspection finds exactly one process that:

- has the same UID as the `solardt-sa` monitor;
- has `-m solar_digital_twin.collectors.solarassistant` in its arguments;
- contains the configured evidence directory in its arguments;
- is not the monitor process;
- retains the recorded PID and `/proc/<pid>/stat` process-start time.

Immediately before abort, UID, exact arguments, PID, process-start time, module,
and evidence directory are revalidated. Missing, ambiguous, exited, or changed
processes disable or reject Abort without guessing. A valid request sends
exactly one `SIGTERM`; it never invokes a shell, accepts a browser PID or
command, sends `SIGKILL`, deletes evidence, or waits indefinitely for exit. The
page reports Stopping while the collector performs its clean shutdown.

## LAN-only access and practical limitation

The default bind is `127.0.0.1` on port `8792`. The intended later LAN
invocation explicitly binds `192.168.3.11`, with exact URL:

`http://192.168.3.11:8792`

The monitor must not be exposed through WAN port forwarding. It follows the
approved practical Home Assistant-style trusted-host model and does not add an
enterprise authentication system. Anyone deliberately granted access to this
LAN page can see the displayed battery telemetry. The in-memory token limits
cross-site and accidental abort requests; future OPNsense containment remains
the planned network boundary.

## Active-capture boundary and later workflow

The active collector and monitor must not be stopped, restarted, signaled,
redeployed, or modified without Chris's explicit approval. Safe development may
continue only when it cannot alter the installed collector or retained-output
behavior. The badge issue was reproduced and corrected offline while
preserving read-only monitor operation. That repository work is complete, but
deployment remains prohibited during the active capture and requires explicit
later approval.

After the configured 86,400-second capture should have completed, the next
stage requires separately approved minimal read-only verification that the
collector stopped automatically, evidence remains present, the monitor is
reachable or its resulting state is understood, and no premature termination
is indicated. Results must be reviewed before deployment is authorized. Only
after separate approval may the installed monitor code be updated and only the
monitor restarted, followed by real-browser badge verification while preserving
all captured evidence. Capture completion has not yet been verified.

The committed launcher is `scripts/run_solarassistant_monitor.sh`. Its
non-privileged `--check` validates local inputs without root, `/var/lib`, a
credential, active collector, device contact, or network access. Real use is
foreground-only as `solardt-sa`; it accepts the documented paths, address,
port, duration, and freshness options, rejects credential-like arguments,
prints the browser URL, and does not use `sudo`, install packages, daemonize, or
create a service.

The approved operator action deployed the committed runtime and started the
launcher in detached `tmux` with the LAN bind. In general, stopping that
monitor process, such as with Ctrl+C in its foreground terminal, stops only the
web monitor and leaves the collector running. The dashboard's confirmed Abort
Capture action instead sends one validated `SIGTERM` to the current collector
while leaving the monitor available to show the resulting stopped state.

When already executing as `solardt-sa` inside that later approved runtime
workflow, the intended foreground command is
`/opt/solar-digital-twin/scripts/run_solarassistant_monitor.sh --evidence-dir /var/lib/solar-digital-twin/solarassistant/evidence --bind 192.168.3.11 --port 8792 --capture-duration 86400 --freshness-seconds 30`.
The later operator workflow is responsible for the approved account switch and
detached `tmux` session; the launcher itself performs neither.

Evidence remains authoritative and unchanged in both cases. The credential is
never read by the monitor.
