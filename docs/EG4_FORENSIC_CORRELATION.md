# EG4 and ESP32 AC-Couple Forensic Correlation

## Status

This document records planned investigation and reporting features.

These features are not the current implementation task. They must not replace the active task in `NEXT_TASK.md` until deliberately promoted through the normal project workflow.

The proposed work must remain:

- read-only
- non-mutating toward EG4 equipment
- conservative toward EG4 portal endpoints
- evidence-based
- explicit about uncertainty
- separate from normal portal and collector behavior until tested

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
retention assessment is complete. Matching EG4 evidence availability must still
be established before a three-source correlation is authorized.

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

## Planned Time Synchronization

Accurate event correlation requires the solardt VM and ESP32 logger to use closely aligned timestamps.

Target concept:

- configure solardt as a LAN NTP server
- point the ESP32 SNTP client to solardt as its preferred server
- retain public NTP servers as fallbacks
- use `America/Chicago` consistently
- verify actual clock alignment before relying on correlation results

The VM address has previously been observed as `192.168.3.11`, but it must be confirmed before being placed into deployed configuration.

Possible ESPHome configuration, for design reference only:

    time:
      - platform: sntp
        id: esptime
        timezone: America/Chicago
        servers:
          - 192.168.3.11
          - 0.pool.ntp.org
          - 1.pool.ntp.org

Do not apply this configuration until solardt is confirmed to be serving NTP and the VM address is confirmed.

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
