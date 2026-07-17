# EG4 and ESP32 AC-Couple Forensic Correlation

## Status

This document records the approved bounded investigation, implemented
synthetic analyzer, and reporting plan. Real-evidence input resolution and
analysis remain separately approved.

The proposed work must remain:

- read-only
- non-mutating toward EG4 equipment
- conservative toward EG4 portal endpoints
- evidence-based
- explicit about uncertainty
- separate from normal portal and collector behavior until tested

## July 16-17 EG4 Evidence Availability

Read-only inventory confirms **Complete** EG4 coverage for the full ESP32
window, with cadence and provenance qualifications. The normalized SQLite
database `eg4_digital_twin.sqlite` is the practical deduplicated query source;
the authoritative cloud-response JSON remains under `evidence/<run_id>/` and
is linked through `sync_runs` and `evidence_files`.

The overlap is `2026-07-16T18:05:14.599Z` through
`2026-07-17T06:05:14.373Z`, or `2026-07-16 13:05:14.599` through
`2026-07-17 01:05:14.373` in `America/Chicago` (CDT).

| EG4 source | Overlap records | First | Last | Cadence and gaps |
|---|---:|---|---|---|
| `day_multiline_samples` | 177 | `2026-07-16 13:08:14` | `2026-07-17 01:04:08` | 241 s median; 724 s largest gap; no gap over 20 min |
| `runtime_snapshots` | 47 | server `2026-07-16T18:14:15Z` | server `2026-07-17T05:56:05Z` | 903 s median capture cadence; 960 s largest gap |
| `energy_snapshots` | 47 | server `2026-07-16T18:14:15Z` | server `2026-07-17T05:56:05Z` | same scheduled runs as runtime |
| `set_records` | 0 | none | none | configuration audit records, not an alarm stream |

The 47 collection runs span `evidence/20260716_131601/` through
`evidence/20260717_005713/`. Each run has runtime, energy, day-multiline,
month-column, and set-record JSON: 235 files total, all present and parseable.
The 47 day files contain 3,554 overlap entries including repeated cloud
snapshots; SQLite deduplicates them into 177 unique source-time samples.
Generated CSV files in `reports/` are derived exports, not source evidence.
The corresponding local collector capture range is `2026-07-16T13:16:01`
through `2026-07-17T00:57:13`, consistent with the nominal 15-minute timer.

Day-multiline rows provide AC-couple, consumption, grid, battery-discharge,
solar-PV power, and EG4-estimated SOC. Runtime JSON provides aggregate
AC-couple and load context, EG4 SOC, battery and grid/EPS electrical values,
status, warning/fault codes, and grid/EPS frequency. All 177 day rows and all 47
runtime rows have the relevant normalized fields and valid stored raw JSON.
There is no separate matching alarm/event stream; warning and fault fields are
point-in-time runtime context.

### Timestamp semantics and qualifications

- Day `sample_time` is a cloud-returned, naive Central source timestamp. Convert
  it from `America/Chicago` to UTC; it is not collector receipt time.
- Runtime `server_time` is a cloud/server UTC source timestamp. `device_time`
  is corresponding device-local Central time. `captured_at` is a naive Central
  collector-run timestamp and is provenance, not measurement time.
- Runtime `captured_at` followed `server_time` by 2-119 seconds (72-second
  median), demonstrating variable portal/collection latency.
- Day records are about four minutes apart but include one 724-second gap from
  `2026-07-16 23:51:47` to `2026-07-17 00:03:51` Central.
- EG4 is much coarser than one-second ESP32 and approximately 10.5-second
  SolarAssistant data. It cannot establish the exact second of a step or
  exclude a brief disturbance between samples.

A bounded compatibility check used the first, middle, and last ESP32 receipt
records. After UTC-to-Central conversion, nearest EG4 day samples were 62, 36,
and 66 seconds away. Nearest runtime `server_time` values were 302, 85, and 414
seconds away. This confirms timezone alignment and expected cadence, not system
behavior.

## Investigation Background

A review of EG4 AC-couple data from July 11, 2026 showed that the original simple dropout concept was too narrow.

The original concept looked for total AC-couple output falling near zero. That can detect a complete loss of AC-coupled production, but it does not describe the field behavior observed at the CP-100.

The observed behavior was:

- one or more microinverters appeared to drop completely offline
- other microinverters continued producing
- aggregate AC-couple power therefore remained above zero
- the offline production later returned
- returning production sometimes ramped upward over several samples

EG4 provides aggregate AC-couple power and cannot directly identify which individual microinverter may have stopped producing.

## Important Finding

The July 11, 2026 EG4 data showed repeated partial AC-couple collapse and recovery signatures rather than complete AC-couple dropouts.

Common sequence:

1. High aggregate AC-couple output
2. Sharp partial reduction
3. Continued non-zero AC-couple production
4. Recovery during following samples
5. In some cases, a gradual ramp toward the earlier output level

Example aggregate changes:

| Before | After | Character |
| ---: | ---: | --- |
| 4138 W | 523 W | Sharp partial collapse |
| 4126 W | 724 W | Sharp partial collapse |
| 3449 W | 496 W | Sharp partial collapse |
| 3069 W | 526 W | Sharp partial collapse |

During the detected examples, `grid_power_w` remained at 0 W.

These observations are signatures requiring investigation. They are not proof that a particular microinverter failed or disconnected.

## Planned Feature: AC-Couple Microinverter Dropout Signature Review

### Purpose

Detect likely partial microinverter dropout behavior from aggregate EG4 data while clearly acknowledging that EG4 cannot identify individual microinverters.

### Event Classes

#### Full Dropout

Total AC-couple power falls to or near zero.

#### Partial Collapse

AC-couple power falls sharply but remains meaningfully above zero because some AC-coupled production continues.

#### Rebound or Recovery

AC-couple power rises substantially after a full dropout or partial collapse.

#### Slow Ramp Recovery

Power returns over multiple samples rather than immediately returning to its earlier level.

#### Volatility

Repeated large upward and downward movements occur within a short time window.

#### Repeated Drop-Size Buckets

Similar absolute or percentage reductions recur.

Repeated drop sizes may suggest one or more repeatable production units cycling, but aggregate data alone cannot establish that conclusion.

### Candidate Measurements

A future detector may calculate:

- power before the event
- lowest power during the event
- absolute drop in watts
- percentage drop
- duration of the lower-output plateau
- time to initial rebound
- time to approximate recovery
- recovery slope or ramp rate
- number of large movements within a rolling window
- recurring absolute and percentage drop-size groups
- grid power, load, SOC, and available runtime measurements around the event

Thresholds must be configurable and tested against recorded evidence rather than treated as universal constants.

## Cloud-Cover Limitation

Partly cloudy conditions can resemble partial microinverter dropout behavior because EG4 sees only aggregate AC-couple power.

Both cloud cover and individual microinverter dropout may appear as reductions in total AC-couple output.

Every report must state this limitation clearly.

### Clues More Consistent With Cloud or Solar Variability

Possible clues include:

- smoother or broader reductions
- gradual changes across several samples
- no lower-output step or plateau
- no repeated similar-sized reductions
- no corresponding voltage or frequency disturbance

### Clues More Consistent With Microinverter Dropout and Rejoin

Possible clues include:

- sharp step-like reduction
- a lower-output plateau while other production remains active
- slow ramp back toward prior output
- recurring similar-sized reductions
- repeated cycling during otherwise strong solar conditions
- possible timing relationship with voltage or frequency events

These clues should affect confidence or interpretation. They must not be presented as definitive identification.

## EG4 Frequency Review

Nearby EG4 runtime snapshots were reviewed around large aggregate AC-couple events.

Available readings were generally close to 60 Hz:

- grid frequency approximately 59.93 to 60.12 Hz
- EPS frequency approximately 59.94 to 60.11 Hz

The available EG4 readings did not show an obvious frequency cause.

However, EG4 runtime snapshots may be several minutes away from the actual collapse event and may miss short voltage or frequency disturbances.

The absence of an EG4-recorded disturbance must not be interpreted as proof that no brief disturbance occurred.

## ESP32 Frequency Retention Status

Implemented and covered by offline collector-level tests:

- approved ESP32 SSE observations remain preserved in the existing raw NDJSON
- a separate retained NDJSON stream exists
- approved non-frequency records pass through unchanged
- valid generator-frequency values retain changes of at least 0.04 Hz from the last retained value
- a 30-second heartbeat uses monotonic elapsed time to retain stable frequency periodically
- invalid frequency values remain raw-only and do not alter retention state

The retained stage was verified by the completed 12-hour ESP32 capture. The raw
and retained files parsed without malformed or truncated records, used
canonical UTC receipt timestamps, contained all 17 approved public entity IDs
and no unapproved IDs, and preserved every retained record unchanged and in raw
order. The high retained/raw ratios (approximately 91.38% by line and 95.77% by
byte) were explained by the completed assessment in
`docs/ESP32_RETENTION_ASSESSMENT.md`: only frequency is selectively retained,
while every non-frequency entity intentionally passes through. No policy change
is approved pending event-window validation.

Still planned:

- normalized database retention
- last-observed tracking for suppressed samples in normalized history
- rolling raw buffers
- automatic pre-event, event, and post-event preservation
- event-triggered suppression overrides for threshold crossings, availability transitions, and forensic events
- the remainder of the multi-topic retention schedule

The 0.04 Hz deadband is an initial configurable value. Review actual evidence and widen or narrow it only after measuring normal frequency variation.

Field observation indicates that the EG4 inverter appears to switch AC-coupled microinverters on and off when operating conditions are met rather than continuously ramping their output. Event detection should therefore treat abrupt power steps, lower-output plateaus, and later step recovery as primary signatures. Ramp-rate measurements remain useful supporting evidence but should not be required for event detection.

## Mixed-Status Telemetry Observation and Retention Schedule

The following is an initial configurable design. Only the ESP32 retained-file
frequency deadband and heartbeat subset described above is implemented; the
normal database retention schedule and other topic policies remain planned.

| Source and telemetry | Observation cadence | Normal database retention | Status |
|---|---:|---|---|
| ESP32 AC-couple power | Continuous, aligned to one-second samples | On change, plus 30-second heartbeat while producing | Planned |
| ESP32 active-microinverter count | Continuous | Immediately on every change | Planned |
| ESP32 status, curtailment, and binary events | Continuous | Immediately on every transition | Planned |
| ESP32 frequency | Every second while solar is active | Change of at least 0.04 Hz, plus 30-second heartbeat | Retained file offline-tested; database planned |
| ESP32 voltage, current, and ramp rates | Every second while active | On meaningful change, plus 30-second heartbeat | Planned |
| SolarAssistant load power | Every 10 seconds | On change, plus 60-second heartbeat | Planned |
| Battery voltage, current, and power | Every 10 seconds | On change, plus 60-second heartbeat | Planned |
| Battery 1, Battery 2, and combined SOC | Every 60 seconds | On SOC change, plus 5-minute heartbeat | Planned |
| Cell voltage and imbalance | Every 60 seconds | On meaningful change, plus 5-minute heartbeat | Planned |
| Battery temperatures | Every 60 seconds | On meaningful change, plus 5-minute heartbeat | Planned |
| Health, capacity, and cycle count | Every 15 minutes | On change, plus daily heartbeat | Planned |
| EG4 telemetry | Existing established cadence | Preserve as a separate inverter and aggregate source | Existing EG4 workflow |

SolarAssistant returns the complete metrics response on each authenticated request and topics are filtered locally. Different database retention intervals therefore reduce evidence and database volume, but do not reduce SolarAssistant API traffic unless the overall polling interval is changed.

Planned normalized history must update a last-observed timestamp for suppressed
duplicates so unchanged current values cannot be mistaken for stale data.
Planned significant-event handling may override normal suppression and preserve
complete one-second pre-event, event, and post-event evidence.

## Evidence Roles

The complete ESP32 capture window overlaps the SolarAssistant capture. Both
sources use `solardt` UTC receipt timestamps, and the completion review found no
clock reversal or timezone conflict. SolarAssistant samples average about 10.5
seconds apart while the ESP32 primary cadence is about one second. The evidence
is suitable for a later bounded offline correlation analysis. The ESP32
retention assessment is complete, and matching EG4 evidence availability is
classified Complete with the cadence and provenance qualifications above.

### EG4 Data

EG4 data is useful for detecting aggregate symptoms and operating context:

- aggregate AC-couple collapse and recovery
- load
- grid power
- battery SOC
- runtime frequency snapshots
- event timing at the EG4 sampling resolution

### ESP32 Forensic Logger Data

The ESP32 forensic logger may provide higher-resolution evidence about possible causes:

- 1-second GEN voltage
- 1-second GEN frequency
- 1-second estimated AC-coupled power
- power ramp rate
- voltage ramp rate
- frequency ramp rate
- timestamped forensic event entries

Discussed ESP32 event names include:

- `POWER_DROP`
- `POWER_RISE`
- `FREQ_DROP`
- `FREQ_RISE`
- `VOLT_DROP`
- `VOLT_RISE`

The deployed ESPHome configuration must be reviewed before future correlation code depends on these sensors or event names.

## Timestamp synchronization basis

`solardt` and the ESP32 already use the verified LAN NTP arrangement documented
in `PROJECT_STATE.md`. SolarAssistant and ESP32 preserve canonical `solardt` UTC
receipt timestamps. EG4 requires the explicit conversions above. Correlation
must use UTC internally and may render Central time only for operator reports.

## Bounded Offline Correlation-Analysis Plan

### Implemented synthetic analyzer

`src/solar_digital_twin/analysis/forensic_correlation.py` is a pure, offline
component that accepts already parsed, source-labeled record streams. It does
not open files, databases, protected paths, credentials, or network resources.
Callers must provide each original timestamp, its source-specific timestamp
kind, and an explicit timezone for naive source times. The analyzer preserves
the original timestamp and provenance while normalizing its internal timeline
and report timestamps to UTC.

The first conservative detector uses configurable minimum baseline, absolute
and percentage drop, plateau-sample, recovery, zero-output, search-window, gap,
alignment, and frequency-support thresholds. It requires an abrupt EG4 drop,
at least two reduced-output plateau samples, and a later recovery. It reports
non-zero partial collapse separately from zero output, supports multiple events,
and orders unsorted parsed input deterministically without changing it.

SolarAssistant and ESP32 nearest-record matches use conservative default
tolerances of 15 and 2 seconds. Exact, nearest, missing, and out-of-tolerance
results remain distinct; the analyzer does not interpolate or invent evidence.
It attaches an ESP32 native-sample window for frequency, event, and availability
context. EG4 SOC remains labeled as a comparison estimate, while
SolarAssistant/JK BMS remains the trusted battery source.

Confidence is intentionally explainable (`low`, `moderate`, or `high`). Output
lists the factors that raise or lower confidence, always retains cloud cover or
normal solar variability as an alternative explanation, and never claims
causation. Seventeen focused synthetic tests cover partial and zero-output
events, recovery shapes, cloud-like and no-event controls, missing and
out-of-tolerance context, timezone normalization, cadence gaps, availability
and frequency context, distinct SOC roles, multiple events, deterministic
ordering, input immutability, and reduced ESP32 context equivalence.

This validation does not authorize execution against EG4 SQLite, actual JSON
or NDJSON evidence, generated operational reports, or the protected
SolarAssistant directory. Explicit input adapters and any real-data report run
belong to a later separately approved work unit.

### Implemented synthetic input adapters

`src/solar_digital_twin/analysis/correlation_adapters.py` provides explicit,
offline iterators for bounded EG4 day and runtime SQLite rows, grouped raw
SolarAssistant polls, and raw or retained ESP32 NDJSON observations. Every
interface requires a caller-supplied input path and aware UTC start/end bounds.
There are no inferred operational paths, network calls, credential handling,
output files, or import-time actions.

SQLite uses URI `mode=ro`, `PRAGMA query_only`, fixed table/column selections,
parameterized time bounds, schema checks, and batched `fetchmany` iteration.
EG4 day source times are explicitly interpreted as `America/Chicago`; runtime
`server_time` is canonical UTC. Only selected warning, fault, and operating-mode
keys are extracted from runtime JSON, never the complete payload.

NDJSON inputs are read one line at a time. SolarAssistant records from one poll
are grouped only until the receipt timestamp changes, preserving metric names,
units, combined/Battery 1/Battery 2 identity, and trusted combined SOC. ESP32
records preserve entity identity, value, unit, availability, stream kind, and
approved provenance. Malformed input raises a line-numbered diagnostic without
including raw payload text. Canonical receipt timestamps must use UTC `Z`.

Day records feed event detection directly. Runtime records use the analyzer's
separate EG4 context input and its conservative ten-minute nearest-record
tolerance. SolarAssistant and ESP32 continue to use 15-second and 2-second
tolerances. Provenance survives into aligned report records, while missing and
out-of-tolerance observations remain explicit.

The adapters themselves are iterative and do not cache complete inputs. The
analyzer sorts the records supplied for a run, so a future real workflow must
first detect candidate EG4 windows and then supply only explicitly bounded
SolarAssistant and ESP32 windows. It must not pass an entire high-rate capture
to the analyzer and call that bounded-memory operation.

Synthetic temporary SQLite and NDJSON tests validate read-only enforcement,
schema failures, bounded queries, source scopes, canonical time handling,
malformed input, availability, lazy iteration, input immutability, provenance,
and end-to-end partial-collapse detection. No real evidence or operational
database has been used. Real execution remains separately approved.

### Future protected SolarAssistant access procedure

The installed evidence directory intentionally prevents `chris` from listing
or reading collector output. Elevated administrator assistance is therefore
required, but only after Chris approves the exact metadata or copy action.

Before a real run, obtain only the raw filename, retained filename if relevant,
ownership, permissions, size, modification time, capture window, and completion
confirmation. Prefer a narrowly scoped administrator-run metadata inventory.
If analysis access is later approved, use a controlled read-only copy of only
the named evidence file into a dedicated temporary analysis directory owned by
the intended unprivileged analyst and protected from other users.

The approved procedure must:

1. identify exact source and destination files in advance, without recursive
   listing, permission changes, or access to neighboring files;
2. avoid the credential directory, monitor process state, environment, command
   output containing tokens, and all unrelated runtime files;
3. keep secrets out of arguments, output, shell history, reports, and Git;
4. record source size and modification time, plus a source hash calculated by
   the administrator without printing evidence content;
5. calculate the copy hash as the unprivileged analyst and require matching
   size and hash before analysis;
6. keep the protected source immutable and open any approved analysis copy
   read-only;
7. place derived reports only in the separately approved temporary or ignored
   destination; and
8. after review and separate approval, remove temporary copies without touching
   the protected source, then confirm the source metadata still matches.

Separate approval is required for metadata inspection, source hashing, copy
creation, reading the copy, running the real analyzer, producing a derived
report, and deleting the temporary copy. No runnable elevated command is
approved or recorded here. Restarting the monitor merely to rotate the unused
abort token is unrelated to adapter validation, would alter runtime state, and
remains a separate future approval before another abort-capable capture.

### Selected sources

- EG4: query `day_multiline_samples` and `runtime_snapshots` read-only from
  `eg4_digital_twin.sqlite`, with reported rows traceable to stored `raw_json`
  and the 47 immutable JSON evidence runs. Use day samples for aggregate
  AC-couple, grid, load, and EG4 SOC; use runtime for status, warning/fault,
  voltage, and grid/EPS-frequency context.
- SolarAssistant: use the authoritative non-retained raw NDJSON in
  `/var/lib/solar-digital-twin/solarassistant/evidence` whose verified receipt
  window is `2026-07-16T07:00:43.194Z` through
  `2026-07-17T07:00:41.713Z`. Its exact protected filename must be resolved by
  a separately approved metadata-only preflight before analysis; do not guess
  it or weaken directory permissions. Raw is required because several battery
  families are intentionally absent from retained output.
- ESP32: use authoritative raw
  `evidence/esp32/esp32_sse_20260716_180514Z.ndjson`. Raw retains complete
  one-second frequency and all approved events; retained output is used only
  for the later policy-replay comparison.

EG4 is aggregate inverter/context evidence. SolarAssistant/JK BMS is trusted
battery SOC and battery telemetry. ESP32 is high-resolution frequency, state,
estimated power, active-microinverter, ramp-rate, and forensic-event evidence.
EG4 SOC remains a separately labeled estimate and must not replace, correct, or
be merged with trusted JK SOC.

### Common timeline and alignment

1. Normalize every selected timestamp to aware UTC while preserving original
   text, source, timestamp kind, and conversion rule.
2. Use EG4 day `sample_time`, runtime `server_time`, SolarAssistant
   `received_at_utc`, and ESP32 `received_at_utc`. Retain EG4 `captured_at` as
   provenance and latency context only.
3. Detect candidate event windows from consecutive EG4 day samples. Do not
   interpolate a step between them or invent samples.
4. Within each bounded window, retain native samples and use nearest-neighbor
   lookup only for tabular context: normally plus or minus 7 minutes for EG4
   day, 10 minutes for runtime, 15 seconds for SolarAssistant, and 2 seconds for
   ESP32. A miss remains explicitly missing.
5. Show source latency and cadence separately. Do not treat receipt timestamps
   as device timestamps or infer sub-cadence precision.

### Candidate event logic

Keep thresholds configurable and evidence-reviewed. A candidate begins with a
large absolute or percentage decrease in EG4 AC-couple power. Classify its
shape using the non-zero post-drop level, consecutive lower-output samples,
later rebound, time toward the prior level, and any gradual recovery ramp.
Attach, without merging, nearby ESP32 active-microinverter, estimated-power,
frequency/voltage/ramp, binary-state, and forensic-log observations plus
SolarAssistant battery SOC, voltage, current, and power context.

Cloud cover and ordinary solar variability remain competing explanations.
Step-like reduction, a sustained non-zero plateau, repeatable drop size,
active-microinverter transition, or supporting electrical event may raise
confidence; smooth broad change or missing high-resolution evidence lowers it.
Correlation never proves causation or identifies an individual microinverter.

### Reproducible output and validation

Produce one concise offline report with source file/database identities,
analysis parameters, candidate windows, aligned native-sample timeline,
before/during/after values, step magnitude and percentage, plateau duration,
recovery timing/ramp, frequency and battery context, gaps, provenance,
confidence, and alternative explanations. Generated output belongs in an
ignored report or `/tmp`, not Git.

Implement focused tests before real analysis for synthetic aligned sources,
missing-source windows, deliberate timestamp offsets, abrupt steps, gradual
cloud-like ramps, non-zero plateaus, simultaneous availability transitions,
and no-event controls. Then use identified real event windows to replay current
raw ESP32 evidence through the conservative candidate from
`docs/ESP32_RETENTION_ASSESSMENT.md`; compare event/window preservation without
changing evidence or production retention.

## Planned Report: AC-Couple Event Correlation Report

### Report Purpose

Use EG4 data to detect aggregate AC-couple collapse and recovery events, then inspect ESP32 1-second voltage, frequency, power, ramp-rate, and forensic-log evidence around the same timestamp.

### Example Event Section

    Event: Possible microinverter dropout
    EG4 event time: 2026-07-11 13:38:08
    EG4 AC-couple: 4126 W -> 724 W
    EG4 grid power: 0 W
    EG4 load: 1732 W

    Nearest ESP32 evidence:
    - voltage, frequency, and power before, during, and after the event
    - matching power, voltage, or frequency forensic events
    - measurement gaps or timestamp uncertainty

### Interpretation Categories

#### Likely Microinverter Dropout

- EG4 AC-couple output drops sharply
- ESP32 estimated power also drops
- voltage and frequency remain mostly normal
- a step, plateau, rebound, or slow-ramp pattern is present

#### Possible Grid or Electrical Disturbance

- EG4 AC-couple output drops sharply
- ESP32 records a voltage or frequency disturbance near the event
- matching forensic event entries are present

This indicates correlation, not proven causation.

#### Likely Cloud or Solar Variability

- output changes gradually or broadly
- no voltage or frequency disturbance is recorded
- no repeatable step-like signature is present

#### Uncertain

Use this category when data is missing, timestamps are misaligned, sample gaps are too large, or more than one explanation remains plausible.

## Possible Later Synchronized Strong-Sun Diagnostic Window

A later, separately approved synchronized diagnostic window may reduce
cloud-cover uncertainty only if the initial 12-hour ESP32 capture and existing
evidence justify it. Do not schedule or launch this window now.

Suggested design:

- run for approximately six hours during strong-sun conditions;
- collect ESP32 SSE at its existing approximately one-second cadence;
- use SolarAssistant at its established 10-second polling target;
- begin temporary EG4 diagnostic collection at a five-minute cadence;
- remain read-only and non-mutating
- leave EG4 settings unchanged
- label diagnostic runs clearly
- keep evidence distinct where practical; and
- preserve normal EG4 collection and reporting behavior outside the window.

A one-minute EG4 interval is not authorized. It may be considered only after
five-minute testing is reviewed and separately explicitly approved. Any timing
relationship is correlation evidence and must not be claimed to prove
causation.

EG4 cloud and portal endpoints must not be hammered.

## CP-100 Local Data Access Research

Direct CP-100 data may expose individual microinverter behavior that aggregate EG4 measurements cannot identify.

Research possibilities include:

- local web interface
- documented or discoverable local API
- local network service
- data export capability
- supported integration interface
- RS485 only if evidence shows it is practical

CP-100 integration remains a research and backlog item until its local interfaces, permissions, protocol, and data fields are confirmed.

## Future Implementation Boundaries

Before implementing this design:

1. Preserve existing EG4 collector and portal behavior.
2. Define event thresholds from recorded evidence.
3. Confirm timestamp semantics for every source.
4. Confirm ESP32 measurement and log formats.
5. Establish and test time synchronization.
6. Keep raw evidence available for review.
7. Separate observations from interpretations.
8. Include confidence and uncertainty in reports.
9. Do not identify individual microinverters without supporting data.
10. Promote the work through `NEXT_TASK.md` before implementation.

## Documentation Follow-Up

This design note is indexed. Immediate work is governed by `NEXT_TASK.md`; the
possible synchronized diagnostic window remains deferred until evidence and
separate approval justify promotion.
