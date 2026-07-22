# Solar Collapse Forensic Event Plan

## Status and authority

This document is the authoritative semantic plan for future detection and
analysis of abrupt daytime AC-coupled solar-production collapses. It records an
accepted investigation direction only. It does not implement a detector,
authorize historical or live data access, bind a portal, change collection, or
make a causal, safety, code, or warranty finding.

Existing raw evidence remains authoritative. Source observations, operator
context, hypotheses, analytic results, causal claims, and warranty conclusions
remain separate.

## Primary question

> What changed across every available electrical and environmental source
> immediately before SolarAssistant showed an otherwise illogical collapse of
> established daytime solar production to zero or near zero, and how did the
> system recover afterward?

The investigation is not limited to high-output periods. A stable baseline near
4,000 W, 1,500 W, 700 W, or another meaningful level may qualify when it drops
almost immediately to zero or very near zero. Future detection must distinguish
an abrupt system shutdown from gradual irradiance change, clouds, dawn, sunset,
stale telemetry, and source failure.

## Trigger authority and source boundary

The first detector will use one exact, reviewed SolarAssistant
solar-production metric as the primary collapse and recovery timeline. The
exact native topic is not established by the current battery-only collector or
its allowlist and must be identified and semantically validated from an
approved sanitized fixture or separately authorized source inventory before
implementation. It must not be guessed from a display name.

The trigger must never use or relabel the EG4-reported aggregate AC-use/load
value that may include AC-coupled production. ESP32 and EG4 provide
corroborating, contradictory, and explanatory evidence; their disagreement
does not veto creation of a SolarAssistant-triggered event. Trigger authority
may change only after evidence establishes a more reliable source. Source
identities are never silently merged.

SolarAssistant/JK BMS remains trusted battery SOC authority. EG4 SOC remains a
separately identified comparison estimate. Volcast and weather are context,
not trigger authorities.

## Configurable research defaults

These values initialize research and are not permanent physical limits:

| Parameter | Initial value |
|---|---:|
| Pre-event baseline window | 2 minutes |
| Minimum meaningful SolarAssistant production baseline | approximately 250 W |
| Minimum relative collapse | 90% |
| Near-zero ceiling | approximately 50 W |
| Near-zero qualification | more than 30 continuous seconds |
| Trusted SolarAssistant/JK BMS SOC condition | below 98% |
| Detailed post-collapse window | at least 20 minutes |

A primary complete-collapse candidate requires both a large relative decline
from the preceding baseline and arrival at the absolute near-zero region. A
large percentage decline that remains well above zero is not the primary event
under this specification. Thresholds remain configurable and must later be
tuned with observed data.

The SOC condition is research scope, not permission to merge SOC sources or a
claim that high SOC causes an event. Events excluded by a research filter must
not be destroyed or relabeled as normal in raw evidence.

## Solar-day state and qualification

Actual production behavior is the primary daylight evidence. Official
sunrise/sunset and Volcast support interpretation but do not independently arm
or veto the detector.

1. After meaningful daytime production is established, the detector remains
   armed until sunset.
2. A transition toward zero starts a fresh 30-second qualification timer.
3. Meaningful production returning before qualification completes discards the
   candidate and resets the timer.
4. A single sample or very small rise does not terminate a continuing outage.
   The exact debounce/recovery threshold remains a configurable detector rule.
5. Near-zero persisting beyond 30 seconds creates a qualified collapse whose
   origin `T` is the first sample of the sustained decline, not the later
   qualification time.
6. After an episode closes, the detector remains armed and may identify
   another episode before sunset.
7. Sunset stops qualification of new daytime-collapse candidates, but an
   already active post-collapse observation may continue.
8. Continuous zero output cannot generate repeated collapses at 30-second
   intervals.

Normal nighttime shutdown is not a daytime collapse: meaningful production
must exist immediately beforehand.

## Case and episode hierarchy

The conceptual hierarchy is:

- one solar-day forensic case;
- one or more collapse episodes during the day; and
- one or more collapse attempts or relapses within an episode.

This is semantic organization, not an accepted storage schema.

For each qualified collapse, preserve detailed context from `T - 2 minutes`
through at least `T + 20 minutes`. The interval is intended to observe an
approximate microinverter reconnection delay, initial production, staged group
return, partial or full recovery, repeated synchronization attempts, and
another collapse during recovery.

If meaningful production returns and another qualifying collapse occurs in
the active window, record a distinct relapse with its own timestamp and
pre-collapse condition inside the same episode, and extend the episode end to
20 minutes after that newest collapse. Continuous zero does not extend the
window repeatedly. Lower-detail tracking may continue afterward until eventual
recovery or the observation period ends.

## Recovery observations and descriptive results

Preserve when the data supports them:

- time to first nonzero and meaningful production;
- time to 25%, 50%, 75%, and 90% of the pre-collapse baseline;
- time to stable recovery and the explicit stability rule used;
- recovery step sizes, repeated rises and collapses, and maximum recovery
  within 20 minutes;
- absence of production at 20 minutes and eventual recovery time when later
  observed; and
- source disagreement, missing, stale, unavailable, and insufficient-data
  states.

Possible descriptive labels include `recovered_under_10_minutes`,
`recovered_10_to_20_minutes`, `partial_recovery`,
`repeated_reconnect_attempts`, `not_recovered_at_20_minutes`,
`source_data_insufficient`, and `measurement_source_disagreement`. They are
analytic descriptions, not causal conclusions.

## Cross-source episode context

An event does not require every source to exist or agree. Preserve source
identity, native and canonical metric identity, observation and receipt times,
freshness, availability, unit provenance, lineage, and alignment uncertainty.

### SolarAssistant

- the exact reviewed AC-coupled solar-production trigger metric;
- trusted combined and per-battery SOC, battery voltage/current, and
  charge/discharge direction;
- inverter/source state, availability, freshness, and other relevant complete
  read-only telemetry.

### ESP32/PZEM

- reported frequency and frequency ramp/step behavior;
- voltage, current, estimated AC-coupled power, power ramps, and estimated
  active microinverters;
- availability, status text, forensic events, reconnects or interruptions, and
  extreme finite readings.

The current PZEM arrangement measures one 120 V leg and estimates some
split-phase values by multiplication. It does not directly prove both legs or
true L1-L2 waveform behavior.

### EG4

- AC-coupled production; generator/AC-coupling voltage and frequency; grid and
  EPS values; operating mode and state;
- comparison SOC, availability, freshness, and relevant read-only telemetry.

### Volcast

- expected production with available five-minute, hourly, and daily context;
- issued/generated time only when the source supplies it, retrieval time,
  forecast age/staleness, and actual-versus-forecast deviation;
- explicit unavailable or stale state.

Volcast never vetoes actual established production followed by collapse. A
sudden storm may make a forecast inaccurate. Production Volcast access remains
separately deferred and requires its own authorization.

### KVBT airport observations

For each case and episode, retain when available the latest observation before
and first after the event, observation time and age, ambient temperature, dew
point, relative humidity, wind, pressure, visibility, sky condition, reported
weather, and original METAR or stable source reference.

KVBT is approximately 1,000 metres west of the solar installation. Because of
that close distance, this project treats it as representative local ambient-
weather data while retaining explicit KVBT source identity, observation time,
and provenance. It is not a sensor physically attached to the residence,
inverter, batteries, or microinverters and must not be represented as their
temperature or local equipment measurement. A future shaded on-site sensor may
supplement it.

### National Weather Service alerts

Attach, when later authorized and available, geographically relevant watches,
warnings, advisories, and similar alerts with stable ID, active state, type,
headline, severity, certainty, urgency, effective/onset/expiration/end times,
affected area, and updates or cancellations. Alerts are contextual evidence;
they neither suppress electrical events nor prove causation.

## ESP32 generator-frequency semantics

The planned synthetic root adapter must identify the metric as
ESP32/PZEM-reported generator frequency and preserve every finite numeric value
from approved entity `sensor-01_gen_frequency`. It must not reject, clip,
clamp, correct, or suppress a value solely because it is electrically
surprising.

The prior 6000XP systems reportedly produced slowly updated extreme values,
multiples or harmonics of 60 Hz, readings above 5,000 Hz, and values near
30,000 Hz. The 12000XP has not been tested for this behavior and remains
unqualified. An extreme value is not automatically the actual AC fundamental,
but an estimator artifact may still be useful forensic evidence if it repeats
before or during shutdown.

Structural malformed values, Booleans, nonnumeric strings, and non-finite
numbers reject. Raw `value` and `state` remain lossless. Firmware settings at
59 Hz, 62 Hz, and the configured frequency-step threshold are event-analysis
thresholds, not record-validity limits. Anomaly flags remain separate from
source-record validity.

Future synthetic fixtures cover ordinary values near 60 Hz, threshold
crossings, multiples of 60 Hz, 5,000 Hz, 30,000 Hz, explicit null, `unknown`,
`unavailable`, malformed, Boolean, and non-finite input. Raw and retained
copies represent one physical/source occurrence. Production observation-ID and
record-ID encoding remains deferred.

## Nighttime EG4 characterization

A separate future task must characterize the believed nighttime removal or
power-down of the EG4 240 V AC-coupling signal. Measure last sustained
production, last AC-coupling voltage, voltage disappearance, frequency
disappearance or abnormality, EG4 and SolarAssistant state transitions,
morning restoration, and microinverter reconnection timing. Duration and
sequencing are currently unmeasured. This task remains distinct from daytime
collapse detection and requires separate authorization.

## Working hypothesis and alternatives

Hypothesis only:

> A transient abnormality in voltage, frequency, waveform quality,
> synchronization, or another condition at the EG4 GEN/AC-coupling output may
> simultaneously trigger protection logic in all connected microinverters. The
> EG4 output may normalize quickly, while the microinverters remain offline
> through their reconnection qualification period and later return in stages.

Competing explanations remain intentional EG4 AC-coupling interruption or
control behavior; a voltage interruption too brief for slower telemetry;
frequency or waveform distortion; repeated zero crossings or estimator
behavior; microinverter protection responding to a genuine grid-quality event;
PZEM/ESPHome artifacts; collector/network interruption; reporting loss rather
than physical production loss; weather-related irradiance collapse; and
unknown causes.

## Future Forensics controls

The future portal `Forensics` tab may reanalyze retained historical
observations without changing raw evidence. Planned controls include minimum
near-zero duration, minimum drop percentage or amount, near-zero ceiling,
minimum pre-event production, pre/post windows, and optional recovery/relapse
thresholds. Initial displayed defaults mirror this plan: more than 30 seconds,
2 minutes before, 20 minutes after, approximately 250 W baseline, 90% collapse,
and approximately 50 W near-zero ceiling.

Controls never alter collectors, erase evidence, rewrite history, or imply that
research defaults are proven physical limits.

## Milestone sequence

1. Synthetic ESP32 generator-frequency root adapter preserving all finite
   reported values.
2. Finalize the source-neutral solar-collapse event specification, including
   the exact reviewed SolarAssistant production trigger identity.
3. Offline synthetic multi-source collapse and recovery detector.
4. Historical analysis against separately approved existing captures.
5. Later live event detection.
6. Later Forensics-tab controls.
7. Separate 6000XP and 12000XP nighttime-output and reconnection
   characterization.
8. Later KVBT and National Weather Service production integrations under
   separate approval.

Each milestone requires its own bounded review and authorization. This plan
does not implement or authorize any of them.

## Protected boundary and recovery

No source code, adapter, collector, detector, storage, schema, portal, service,
timer, credential, evidence, database, runtime, device, firmware, network, or
weather integration is authorized here. Persistent ESP32 operation remains
unauthorized. Household-load derivation remains separate.

Recovery from this documentation decision is a normal revert of its future
documentation commit. No operational rollback applies.
