# SolarAssistant Read-Only Telemetry Plan

## Status

The raw collector was manually verified on 2026-07-14. The first separate
retained-output slice was implemented in commit `4e069bb`, verified offline,
and subsequently exercised by the completed 24-hour capture. Commit `dc1adc9` completed the first
offline raw-evidence deadband assessment, but the evidence was insufficient for
numeric thresholds. Collector:
`src/solar_digital_twin/collectors/solarassistant.py`.

Commit `39548b1` completed the repository-side dedicated runtime support. The
runtime and credential were subsequently installed under the approved practical
Home Assistant-style trusted-host model, runtime metadata and access boundaries
passed committed verification, and one authenticated manual run succeeded as
`solardt-sa`. No persistent service was created. The controlled 24-hour capture
subsequently completed normally and passed evidence-quality review with the
permissions-related qualifications below.

## Completed 24-hour capture

The capture ran from `2026-07-16T07:00:43.194Z` through
`2026-07-17T07:00:41.713Z`, covering 86,398.519 of the requested 86,400
seconds. The monitor reported `stopped_early: false`, 8,219 completed polls,
42 records per poll, 345,198 raw records, 2,705 retained records, 80,199,183
raw bytes, and zero invalid complete records. Average observed poll cadence was
approximately 10.513 seconds, or 95.13% of an exact ten-second poll schedule.
No monitor-observed receipt gap exceeded 30 seconds.

Combined and per-battery SOC, voltage, current, power, cell-voltage, health,
and temperature families were present. Full-duration coverage showed no
evidence of premature HTTP `401` or `403` termination or a major outage. The
result is **Passed with qualifications**.

The protected runtime permissions correctly prevented unprivileged direct
inspection of collector evidence and logs. Exact retained byte size, exact
largest sub-30-second gap, trailing-line condition, and transient collector-log
errors therefore were not independently confirmed. This is a permissions
boundary, not a capture failure.

## Purpose

Define the smallest safe standalone collector for trusted JK BMS telemetry
from SolarAssistant.

The accepted future solar-collapse investigation direction is
`docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md`. Its first detector will use an
exact reviewed SolarAssistant solar-production metric as trigger authority, but
that metric is not part of this battery-only collector or its current allowlist.
Identifying it requires a separate sanitized fixture or authorized source
inventory. Do not substitute the qualified EG4 aggregate AC-use/load display
field described below.

Tracked approved material does not currently establish that trigger binding.
The event plan therefore uses `solar_production_trigger_metric` and specifies
the smallest later proposal: one separately authorized read-only
`GET /api/v1/metrics` inventory, a narrowly sanitized candidate fixture, and
independent semantic/owner review. A single response is sufficient only if it
unambiguously establishes topic, scope, unit, sign, instantaneous AC-coupled
production meaning, exclusions, state/time behavior, and provenance; otherwise
any short known-state comparison requires separate authorization and must stop
if ambiguity remains.

The next owner-authorized implementation milestone may use standing
authenticated read-only authority for that inventory through the approved
runtime identity. It must minimize requests and response volume, stop after
limited authentication failures, avoid controls/writes, keep the full
authenticated response outside Git, and create only the narrowly sanitized
candidate fixture needed for review. Exact trigger acceptance remains a
milestone gate; unresolved semantics may remain deferred without substituting
another field.

Once resolved, the trigger adapter must feed the reusable collection/analysis
architecture in `docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md`. Pilot collection
uses canonical observations and durable five-minute run checkpoints; interval
analysis remains rerunnable for one through 30 days without recollection.

## Source

- host: `192.168.3.12`
- endpoint: `GET /api/v1/metrics`
- authentication username: `admin`
- software version verified: `2026-07-02`
- interface is read-only for this task

## Qualified EG4 aggregate AC-use interpretation

Chris reports that, in this EG4 AC-coupled installation, SolarAssistant
displays the aggregate AC-use value supplied through EG4 telemetry. He also
reports that a SolarAssistant developer explained that EG4 calculates and
reports total AC use without separating the included AC-coupled solar
contribution from actual household AC loads. This is operator/developer-
reported source-semantic information, not independently proven protocol
documentation.

The native reported value must remain unchanged, source-labeled, and
provenance-preserving. It must not automatically be labeled or interpreted as
actual household load. During beta portal testing, label it as an
**EG4-reported aggregate AC-use** metric, or use an equally explicit
source-semantic label, rather than simply **Home Load**.

A candidate estimate is:

    estimated household load =
      EG4-reported aggregate AC use - included AC-coupled solar contribution

This subtraction is not an approved universal canonical transformation. Do not
apply it automatically to historical data, canonical records, storage,
reports, or portal values. Existing and future synchronized logs must first be
reviewed across grid import or bypass, off-grid operation, battery charging and
discharging, solar curtailment or collapse, inverter operating-mode
transitions, and telemetry timing differences. The project may find the
subtraction unnecessary or applicable only in specific modes.

This known display/source-semantic issue is not warranty evidence and must
remain separate from causal claims about inverter behavior.

## Credential Handling

The existing collector can read `SOLARASSISTANT_PASSWORD` from the environment.

For an interactive manual run, it may fall back to a private `getpass` prompt.

The password must never be printed, written to evidence, committed, or included
in command output.

The SolarAssistant-specific custom credential-bootstrap direction was reviewed
and superseded before installation. The committed credential installer was
later run manually, with private entry through the controlling terminal and
approved installed metadata.

Credential handling follows the approved Home Assistant-style model in
`docs/SECURITY_MODEL.md` and the repository-side runtime design in
`docs/SOLARASSISTANT_RUNTIME.md`. SolarAssistant uses the dedicated
`solardt-sa` identity until the `admin` credential's effective authority is
confirmed. The protected password path is
`/etc/solar-digital-twin/solarassistant/password`; the collector can read but
cannot modify it. The password and any derivative remain outside Git,
documentation, chat, command arguments, and shell history.

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

Development continues to default to `evidence/solarassistant`. The installed
dedicated runtime explicitly selects
`/var/lib/solar-digital-twin/solarassistant/evidence` without changing raw or
retained filenames, records, cadence, or policy.

## Cadence Definitions and Status

- **API polling interval:** how often the collector requests the complete REST response.
- **Raw evidence cadence:** every approved metric from every successful poll is written and flushed to raw NDJSON.
- **Retained-history cadence:** when an implemented topic policy writes to the separate derived retained stream.
- **Heartbeat cadence:** the maximum planned interval between retained records when an observed value remains stable.

The current collector defaults to one-second polling. That remains available for
manual or diagnostic use, but the approved intended normal persistent polling
interval is 10 seconds. The existing raw collector and its one-second default
were manually verified. The dedicated runtime was additionally verified at the
normal 10-second interval during a bounded 25-second authenticated run.

Topic-specific retained-history and heartbeat schedules are documented in
`docs/EG4_FORENSIC_CORRELATION.md`. The exact-change subset below is implemented;
meaningful-change families remain planned. Changing retention does not change
API traffic or raw evidence cadence. No persistent SolarAssistant systemd
service exists yet.

The separate repository-side live-capture monitor documented in
`docs/SOLARASSISTANT_MONITOR.md` reads authoritative raw evidence without making
device requests or changing collector behavior. It maintains derived display
state in memory, may count the retained sibling, and never reads the credential
or writes evidence. It is installed and active as `solardt-sa` in root-owned
detached tmux session `solarassistant-monitor`; its fresh-data `Unknown` badge
is a minor deferred, non-blocking correction.

## Retained-Output Status

The collector writes a separate derived sibling NDJSON output while preserving
every approved observation in the existing raw NDJSON. Raw records are written
and flushed before retained processing. The collector continues to
poll and locally filter the complete response at its configured interval.
Retention changes only storage cadence and never reduces API traffic.

Use the shared source-independent retention library where its change and
monotonic-heartbeat mechanics fit. Keep SolarAssistant topic-family policy
separate so later collectors can reuse mechanics without inheriting battery-
specific rules.

Implemented and offline-tested in commit `4e069bb`:

- Battery 1, Battery 2, and combined SOC: exact change plus 300-second heartbeat
- approved health, capacity, charge-capacity, and cycle topics: exact change plus 86,400-second heartbeat
- independent state per stable metric identity using monotonic heartbeat time
- retained records preserve raw fields and add `retention_reason`

The retained-output tests passed (9), existing SolarAssistant tests passed (6),
shared retention tests passed (14), and the full suite passed (52). Repository
diff and health checks passed. The retained file was created successfully during
the bounded authenticated runtime verification described below.

Still raw-only pending numeric deadband approval:

- battery voltage, current, and power: meaningful change plus 60-second heartbeat
- cell voltage and imbalance: meaningful change plus 5-minute heartbeat
- battery temperatures: meaningful change plus 5-minute heartbeat

No numeric deadband is approved yet for a family described as retaining on
meaningful change. These observations remain complete in raw evidence and are
intentionally excluded from retained output; this is an incomplete source-
specific policy, not a collector defect. Offline evidence characterization must
distinguish resolution from meaningful variation and leave candidate values
pending project-owner approval.

The assessment used two raw files containing 294 valid records and no invalid
records. It covered about 3 minutes 47 seconds by receipt time but only about
7.4 seconds of active capture, with seven observations per stable metric
identity. Raw and retained files were distinguished, only raw evidence was used,
and matching before-and-after metadata manifests confirmed that no evidence was
modified, created, renamed, or deleted. The full 52-test suite, diff check, and
repository health check passed.

No numeric deadband was proposed, approved, implemented, or activated. The
evidence did not adequately cover sustained charging, broad discharging, idle
or near-zero current and power, sign or load transitions, several hours of
temperature evolution, wider voltage movement, or cell behavior near full
charge. Combined and individual batteries may require different thresholds.

The dedicated runtime, protected credential delivery, metadata verification,
and one controlled manual authenticated verification are complete. That run
used the protected password file and dedicated runtime and evidence paths at a
10-second interval for 25 seconds. It stopped cleanly, wrote 126 approved raw
records, and created a separate retained NDJSON file. Raw receipt times spanned
`2026-07-16T05:41:34.125Z` through `2026-07-16T05:41:55.129Z`, representing
approximately three successful responses without authentication rejection.

The run confirmed the approved combined, Battery 1, and Battery 2 telemetry,
including SOC, state of health, voltage, current, power, capacity, charge
capacity, cycles, cell voltage and imbalance, battery temperatures, temperature
sensors, and MOS temperature. Representative values were 78%, 79%, and 77% SOC
and 53.3 V, 53.4 V, and 53.2 V for combined, Battery 1, and Battery 2. Combined
current and power were zero. These are short point-in-time observations, not a
long-term operating characterization.

The controlled 24-hour capture and completion review are complete. The
collector is no longer running. Numeric deadbands, SQLite, portal integration,
systemd, persistent service operation, and any future capture remain separately
reviewed and approved.

The collector supports `--password-file` and `--output-dir` for that runtime.
Password-file loading precedes the existing environment and interactive prompt
sources. Missing, unreadable, empty, or whitespace-only files stop locally
without a request and produce only a credential-free error. Runtime preparation
and credential installation scripts have safe non-privileged checks; their real
installation modes have now been used under the approved manual workflow.

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
- stop immediately without retry or backoff on HTTP `401` or `403`
- close every received HTTP response on success and failure paths
- stop cleanly on Ctrl+C
- flush each NDJSON record promptly

Authentication rejection produces a fixed credential-free operator message and
process exit status 1. This behavior and response closure were completed in
commit `c7370ca` and covered by six focused offline tests; the full 43-test suite
and repository health check passed. Raw evidence behavior was unchanged.

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

The completed short run demonstrated:

- successful authenticated read-only polling
- only approved topics written
- canonical UTC receipt timestamps
- combined and both individual batteries represented
- valid newline-delimited JSON
- evidence ignored by Git
- clean termination without evidence corruption

It also confirmed creation of both raw and separate retained NDJSON files. The
later separately authorized 24-hour capture and its completion review are
documented above.
