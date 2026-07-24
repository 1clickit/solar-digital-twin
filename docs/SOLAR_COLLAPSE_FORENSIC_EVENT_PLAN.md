# Solar Collapse Forensic Event Plan

## Status and authority

This document is the single authoritative semantic plan for future detection
and analysis of abrupt daytime AC-coupled solar-production collapses and its
reusable calibration architecture. This revision is a finalized planning
checkpoint pending independent ChatGPT and owner review. It does not implement
a detector, bind a source metric, authorize historical or live access, select
storage, bind a portal, or make a causal, electrical, safety, code, warranty,
or component-failure finding.

Raw evidence remains authoritative. Source observations, copied views,
operator context, analytic descriptions, hypotheses, and conclusions remain
distinct and provenance-preserving.

## Trigger authority and unresolved binding

SolarAssistant is the intended initial trigger authority. Until separately
reviewed evidence proves the native identity, this plan uses the logical
placeholder:

`solar_production_trigger_metric`

The binding is **unresolved**. Tracked repository inspection found only the
battery-topic SolarAssistant collector and allowlist, its battery-oriented
tests, and the synthetic combined-SOC fixture. Those artifacts establish the
`GET /api/v1/metrics` response family and row fields (`topic`, `device`,
`number`, `group`, `name`, `value`, and `unit`), but no approved artifact
establishes an AC-coupled solar-production topic's exact identity, scope, unit,
sign convention, quantity type, exclusions, state behavior, or semantic
provenance. Home Assistant `pv_total_power` and EG4 fields are different source
paths and cannot establish the SolarAssistant binding.

The EG4-reported aggregate AC-use/load field may include AC-coupled production.
It must not be relabeled or substituted as trigger production or household
load. Friendly display words such as solar, PV, output, load, AC, grid, or
power are not semantic proof.

### Smallest later trigger-metric inventory

A separately authorized milestone should make one read-only
SolarAssistant `GET /api/v1/metrics` response inventory through the already
approved endpoint family and installed runtime identity:

1. use no control or write operation, service installation, persistent
   collector, or credential disclosure;
2. keep credentials out of arguments, logs, Git, documentation, chat, shell
   history, and ordinary backups;
3. do not commit the raw full response;
4. create a narrowly sanitized fixture containing only candidate rows and the
   exact topic, device, number, group, name, unit, value/state type structure,
   receipt semantics, and necessary non-secret provenance;
5. replace or redact sensitive identifiers without changing semantic fields;
6. protect temporary unsanitized material and dispose of it only under the
   existing runtime-security and preservation policy; and
7. stop for independent review before registry or trigger binding.

One instantaneous response is sufficient only if the response semantics and
operating context unambiguously identify AC-coupled instantaneous production
and exclude load, grid flow, inverter consumption, battery power, energy, and
ambiguous aggregates. This is unlikely to be guaranteed from a single display
name. If ambiguity remains, the smallest additional proposal is a short,
separately authorized read-only comparison of the same candidate fields across
known production and non-production operating states. That comparison is not
authorized here. The later task must stop unresolved if semantics remain
ambiguous.

Metric acceptance requires all of: exact native topic; transport/endpoint
family; device/group/number scope; source-supplied or otherwise qualified unit;
sign convention; instantaneous-power quantity; specific AC-coupled production
meaning; exclusion of household load, grid flow, inverter consumption, battery
power, energy, and ambiguous aggregates; combined/device behavior; null,
unknown, unavailable, and missing behavior; receipt/source time semantics; and
reviewable provenance.

## Source roles

- SolarAssistant is intended trigger authority.
- SolarAssistant/JK BMS is trusted battery and SOC authority.
- ESP32 is forensic evidence.
- EG4 is corroborating, contradictory, and comparison evidence; EG4 SOC is not
  trusted battery SOC.
- Volcast, KVBT, sunrise/sunset, and National Weather Service alerts are
  contextual evidence only.
- Context never vetoes an event established by valid actual production.
- A copied view of one upstream source is not independent corroboration.
- Source identity is never merged or silently substituted.

## Definitions

- **Solar day:** one local-day case whose actual production behavior, supported
  but not replaced by sunrise/sunset context, can arm daytime evaluation.
- **Meaningful production:** valid trigger production contributing to a usable
  two-minute baseline. A new primary episode additionally requires a median of
  at least 1,500 W.
- **Valid production sample:** numeric, valid, available, sufficiently fresh,
  correctly sourced trigger power with usable time and unit semantics.
- **Near-zero production:** valid trigger power at or below approximately 50 W.
- **Collapse candidate:** a qualifying-baseline transition satisfying the
  relative-decline and near-zero entry rules but not yet the duration rule.
- **Subthreshold collapse observation:** an otherwise valid abrupt near-zero
  decline whose immediate two-minute baseline median is below 1,500 W.
- **Qualified collapse:** a candidate from a baseline of at least 1,500 W whose
  near-zero condition persists for more than 30 continuous seconds.
- **Event origin (`T`):** first valid near-zero sample in the sustained decline.
- **Qualification time (`qualified_at`):** later time when duration exceeds 30
  continuous seconds; distinct from `T`.
- **Collapse attempt:** the initial qualified collapse or a later qualified
  relapse inside one episode.
- **Relapse:** a new collapse after meaningful recovery inside an already
  qualified active episode.
- **Meaningful recovery:** production above 20% of the original baseline,
  sustained for 30 seconds.
- **Stable recovery:** production at or above 75% of the original baseline,
  sustained for two minutes.
- **Collapse episode:** initial qualified attempt plus its recoveries and
  relapses.
- **Solar-day forensic case:** all qualified episodes, subthreshold
  observations, context, and availability for one solar day.
- **Active observation window:** high-detail interval from `T - 2 minutes`
  through initially `T + 20 minutes`, extended by qualified relapse.
- **Source outage:** trigger transport/source cannot supply observations.
- **Missing data:** an expected sample or field is absent; not numeric zero.
- **Stale data:** otherwise valid data older than its named freshness policy.
- **Unavailable state:** source explicitly cannot currently provide the
  supported metric.
- **Contextual evidence:** environmental/calendar information that informs but
  cannot establish, suppress, or prove cause.
- **Corroborating evidence:** separately sourced evidence consistent with the
  trigger event.
- **Contradictory evidence:** separately sourced evidence inconsistent with the
  trigger event; preserved without silently vetoing it.
- **Unresolved trigger binding:** logical trigger role exists but no native
  SolarAssistant topic has passed the acceptance requirements above.

Numeric zero is distinct from null, missing, stale, `unknown`, `unavailable`,
outage, and malformed data. Reporting loss must not masquerade as physical
collapse. Event labels are descriptive and non-causal.

## Versioned initial research defaults

These adjustable values are not electrical, safety, equipment, manufacturer,
regulatory, or proven physical limits:

| Parameter | Initial value |
|---|---:|
| Baseline window | 2 minutes |
| Minimum baseline median for a new primary episode | 1,500 W |
| Minimum relative decline | 90% |
| Near-zero ceiling | approximately 50 W |
| Near-zero qualification | more than 30 continuous seconds |
| Trusted SolarAssistant/JK BMS SOC research condition | below 98% |
| Detailed post-collapse window | 20 minutes |
| Meaningful recovery | 20% of original baseline for 30 seconds |
| Stable recovery | 75% of original baseline for 2 minutes |

A primary candidate requires both at least a 90% decline from the immediate
baseline and arrival at absolute zero or near zero. A large relative decline
remaining materially above zero is not the complete-collapse event under
study.

Examples: approximately 4,000 W, 2,000 W, or exactly 1,500 W to near zero may
qualify. A baseline median of 1,499 W or less cannot create a new primary
episode and is retained as subthreshold when otherwise valid. Once an episode
qualifies from at least 1,500 W, all lower-output reconnect attempts, partial
recoveries, staged returns, and relapses remain relevant inside that episode.

## Baseline and coverage

The baseline is the median of valid production samples in the two minutes
immediately preceding `T`. Exclude missing, null, `unknown`, `unavailable`,
invalid, nonnumeric, stale-beyond-policy, malformed, future-invalid, and
source-outage samples.

Preserve sample count, expected sample count, time coverage, minimum, maximum,
median, excluded counts/reasons, first/last sample time, and cadence/gaps. Do
not substitute the last sample when the baseline is inadequate or combine
unrelated operating states.

The repository does not already define minimum coverage. Proposed research
default, requiring owner acceptance:

- usable elapsed coverage must span at least 90 seconds of the 120-second
  window; and
- valid samples must represent at least 75% of the samples expected from the
  observed/configured trigger cadence, with no excluded trigger gap longer
  than the proposed candidate-gap limit below.

The immediate baseline median—not an earlier daily maximum—controls new-episode
qualification. A day may exceed 1,500 W and remain armed through sunset, but a
later collapse whose immediate baseline is below 1,500 W is subthreshold.

## Solar-day arming

1. `disarmed` becomes `armed` after valid production establishes a usable
   baseline at or above 1,500 W.
2. Once substantial production has armed the day, arming remains through
   sunset despite later lower production.
3. A new candidate may begin only while armed.
4. Its immediate two-minute baseline must still be at least 1,500 W to become a
   primary candidate; otherwise it is subthreshold.
5. Sunset prevents new daytime-collapse qualification, but an already
   qualified episode/window may continue.
6. Nighttime zero is not a collapse. Normal evening shutdown remains a
   separate characterization.
7. Sunrise/sunset are contextual boundaries, not replacements for production
   evidence.

## State machine

Logical states are `disarmed`, `armed`, `candidate`,
`subthreshold_observation`, `qualified`, `recovering`, `recovered`,
`observation_active`, `insufficient_data`, and `closed`.
`observation_active` is an orthogonal window status: it begins at
qualification and remains true while the episode's recovery substate is
`qualified`, `recovering`, or `recovered`. This avoids discarding recovery
state merely to express that detailed observation continues.

- `disarmed -> armed`: usable qualifying production baseline established.
- `armed -> candidate`: qualifying baseline, at least 90% decline, and first
  valid near-zero sample at `T`.
- `armed -> subthreshold_observation`: same valid shape but baseline below
  1,500 W; it never enters the primary recovery/relapse machine under this
  default.
- `candidate -> qualified`: near zero persists for more than 30 continuous
  seconds; set `qualified_at`, preserve `T`, set `observation_active`, and open
  `T - 2 minutes` through `T + 20 minutes`.
- `candidate -> armed`: candidate reset rule is met before qualification.
- `candidate -> insufficient_data`: trigger gap exceeds allowed duration or
  quality prevents proving continuity.
- `qualified -> recovering`: valid production returns above near-zero.
- `recovering -> recovered`: stable-recovery rule passes.
- `recovering/recovered -> qualified`: a relapse qualifies inside the episode;
  add an attempt and reset detailed end to 20 minutes after the relapse origin.
- `qualified/recovering/recovered -> closed`: the active-window closure rules
  below pass; preserve the final recovery status and any later lower-detail
  recovery observation.

Continuous zero cannot create repeated events. ESP32/EG4 confirmation attaches
to the trigger episode. Equal timestamps alone neither deduplicate nor prove
identity; lineage and semantic occurrence control. Subthreshold observations
remain available for versioned future reanalysis but are not primary episodes.

### Candidate reset and gaps

The repository has no accepted anti-chatter or candidate-gap duration.
Proposed research defaults, requiring owner acceptance:

- a return above the near-zero ceiling resets the candidate only after 10
  continuous seconds of valid trigger data; shorter/tiny rises do not break the
  collapse; and
- a trigger-data gap longer than 15 elapsed seconds during qualification makes
  the candidate `insufficient_data` rather than pausing or treating the gap as
  zero.

Duration uses timestamps, not fixed sample counts, so irregular cadence remains
honest. Shorter gaps do not prove near-zero; qualification needs more than 30
seconds of valid near-zero observations spanning the interval. A later complete
sequence may start a new candidate if the immediate baseline remains usable.

## Subthreshold observations

An abrupt decline from a baseline below 1,500 W:

- does not create a primary episode or interfere with another episode;
- is retained logically when otherwise valid, without defining storage here;
- preserves baseline statistics, decline, near-zero duration, origin, source,
  time, availability, quality, and provenance;
- is labeled `subthreshold_production_baseline`;
- cannot claim the defined primary event; and
- may qualify only in a separately identified future reanalysis using a
  different versioned threshold set.

## Qualified-event, recovery, and relapse behavior

Qualification remains valid if later data is missing/unavailable; later gaps
reduce completeness rather than erase the event. Context never suppresses it,
and source disagreement remains explicit.

Preserve first return above near-zero; meaningful recovery; 25%, 50%, 75%, and
90% crossings relative to original baseline; stable recovery; maximum recovery
inside the window; staged steps; eventual recovery; and unresolved recovery.
Recovery may remain below 1,500 W and still satisfy its percentage rule. Do not
require 1,500 W unless the percentage threshold independently implies it.
Values above the original baseline are preserved without clipping.

For irregular cadence, duration is elapsed-time based and requires valid
boundary samples with no excessive gap. Missing/unavailable data makes the
affected milestone unknown until a later valid sequence proves it; it does not
coerce zero. Sunset during recovery stops new episodes but does not stop the
active episode. Source outage marks recovery unresolved until data returns or
observation closes.

A relapse requires meaningful recovery first. Merely rising from zero without
meaningful recovery, or remaining continuously zero, is not relapse and does
not extend the window. A later collapse after meaningful recovery is another
attempt in the same active episode; the detailed end becomes 20 minutes after
the newest qualified relapse.

For each relapse preserve both:

- decline relative to the original episode baseline; and
- decline relative to the immediate local recovered median.

This dual comparison is the preferred proposal and requires owner acceptance.
The local recovered baseline need not reach 1,500 W because that would hide
lower-power reconnect failures inside a qualified episode.

Each attempt preserves origin, qualification time, local pre-collapse
condition, minimum, duration, recovery, and provenance.

## Episode closure and hierarchy

One solar-day forensic case contains zero or more subthreshold observations,
one or more qualified episodes, and one or more attempts/relapses per episode.

Distinguish: detailed window ended; stable recovery achieved; unresolved at 20
minutes; later recovery observed; sunset reached; trigger observation ended;
and source data insufficient. High-detail observation ends at the latest active
20-minute boundary. Lower-detail case tracking may record eventual recovery
without keeping high-detail capture open indefinitely.

One trigger collapse creates one episode. Corroboration attaches to it. A
collapse during its active relapse window is an attempt in that episode. After
closure, a new episode requires a new immediate baseline of at least 1,500 W;
otherwise it is subthreshold. Production identifiers and storage keys remain
Deferred; examples use logical placeholders only.

## Availability and quality

- Numeric zero/near-zero is usable only when valid, available, fresh, numeric,
  correctly sourced, and unit-qualified.
- Null, missing, `unknown`, `unavailable`, malformed input, or outage never
  becomes zero.
- Stale/future-invalid data is excluded and disclosed.
- Clock uncertainty and repeated timestamps remain explicit; ingest/order and
  occurrence semantics resolve ties where available.
- Insufficient baseline coverage blocks primary qualification without making
  the underlying data invalid.
- Baseline below 1,500 W is valid but subthreshold.
- Candidate gaps follow the proposed 15-second rule; recovery gaps make
  milestones unresolved rather than resetting the accepted event.
- Conflicting SolarAssistant, ESP32, and EG4 values are preserved by source.

## Trusted SOC research condition

Use only SolarAssistant/JK BMS SOC for the `<98%` condition. Associate the
latest valid SOC at or before `T`. Maximum permissible SOC age is unresolved
and requires owner acceptance. Missing/stale SOC preserves the otherwise valid
collapse but labels the research filter `soc_filter_not_evaluable`; SOC at or
above 98% labels it `soc_filter_not_met`. Neither deletes or rewrites evidence.
EG4 SOC remains comparison only. The 1,500 W production gate and SOC filter are
separate conditions.

## Cross-source context

Attach when available, preserving native/canonical identity, source and receipt
times, freshness, availability, unit provenance, lineage, gaps, and alignment
uncertainty.

### SolarAssistant

The reviewed trigger once resolved; trigger values; baseline statistics and
1,500 W result; trusted combined/per-battery SOC; battery voltage/current and
direction; relevant source/inverter states; outages and gaps.

### ESP32/PZEM

Reported generator frequency, ramps/steps/extreme finite values, voltage,
current, estimated AC-coupled power, active-microinverter estimate,
availability, raw `value`/`state`, reconnects, and interruptions. The PZEM
measures one 120 V leg and estimates some split-phase quantities. Extreme
finite frequency remains valid source evidence and is not automatically the
physical AC fundamental.

### EG4

Semantically established AC-coupled production, generator/AC-coupling voltage
and frequency, grid/EPS values, operating state/mode, comparison SOC,
availability, and freshness. Never use ambiguous aggregate AC-use/load as
trigger production or household load.

### Context only

Volcast: expected production, available five-minute/hourly/daily context,
issued/generated time only when supplied, retrieval time, forecast age/stale
state, and actual-versus-forecast deviation.

KVBT: latest relevant observation time/age, temperature, dew point, humidity,
wind, pressure, visibility, sky, weather, and raw METAR/stable reference. KVBT
is about 1,000 metres west and is representative ambient context, not an
equipment/residence sensor.

National Weather Service: alert ID, type/headline, state, severity, certainty,
urgency, effective/onset/expiration/end, area, updates, and cancellations.

These sources never prove cause or veto actual valid production collapse.

## Logical outputs and descriptive classifications

Later implementation needs, without selecting storage: specification and
threshold-set version; trigger binding state; solar-day/episode/attempt logical
identity; qualified/subthreshold classification; `T`; `qualified_at`; detailed
window; trigger identity; baseline statistics/coverage and 1,500 W result;
collapse value/drop/duration; SOC value/time/age/evaluability; recovery
milestones; relapse count; availability/gaps; corroborating/contradictory
summaries; context times/ages; provenance; quality/reasons; and an explicit
non-causal statement.

Possible descriptive results: `recovered_under_10_minutes`,
`recovered_10_to_20_minutes`, `partial_recovery`,
`repeated_reconnect_attempts`, `not_recovered_at_20_minutes`,
`source_data_insufficient`, `measurement_source_disagreement`,
`soc_filter_not_met`, `soc_filter_not_evaluable`, and
`subthreshold_production_baseline`. Never label a subthreshold observation as a
qualified episode.

## Future Forensics controls

Future versioned reanalysis may adjust duration, decline, near-zero, baseline,
window, and recovery/relapse thresholds without rewriting raw evidence. The
initial displayed default is:

`Minimum pre-event production: 1,500 W`

Different threshold versions remain distinguishable. Lower thresholds do not
retroactively change events produced under the 1,500 W default. Subthreshold
observations may qualify only under a separately identified reanalysis set.
No portal/control implementation is authorized here.

## Reusable calibration architecture

The collapse examination must be production-shaped and reusable. Pilot,
calibration, lifecycle, checkpoint, weather, portal, reporting,
prompt-generation, and analysis work must use canonical telemetry contracts,
production-shaped interfaces, and reusable components intended for the final
Solar Digital Twin. Throwaway collectors, duplicate source parsers,
incompatible evidence formats, and calibration-only storage models are
prohibited unless independently justified.

The same preserved observations must support pilot analysis, calibration,
reanalysis, threshold comparison, shadow validation, and eventual production
forensics. Changing an interval or threshold must not require recollection.

### Collection layer

The collection layer:

- acquires source observations through accepted source adapters;
- preserves native/canonical source identity, provenance, observation and
  receipt times, availability, units, quality, and lineage;
- writes append-only evidence and never rewrites collected observations;
- creates durable run manifests and checkpoints;
- records enough source and software version information for later replay; and
- does not permanently determine detector thresholds.

### Analysis layer

The analysis layer:

- reads stored canonical observations without mutation;
- accepts a selected retained-evidence interval;
- may be rerun at any time with a versioned configuration;
- compares threshold versions without changing earlier classifications;
- identifies primary candidates and subthreshold observations;
- produces calibration recommendations, reports, and troubleshooting
  summaries; and
- never mutates raw or canonical source evidence.

## Examination intervals and operating modes

Supported analysis intervals are one through 30 days, including convenient
one-, three-, seven-, 14-, and 30-day selections and any valid custom interval
within retained evidence. The initial pilot defaults to approximately three
days. Collection and analysis must use the configured start and intended end;
a run must never silently extend beyond its configured duration.

Reusable modes are:

- `inventory`: bounded source/metric discovery and semantic fixture work;
- `pilot`: short end-to-end collection, lifecycle, and analysis validation;
- `calibration`: longer observation and threshold recommendation;
- `shadow`: accepted pipeline operating without official event effects;
- `production`: owner-accepted trigger and threshold classification; and
- `reanalyze`: read-only replay of retained observations under a named
  configuration.

Moving from calibration to production should primarily require acceptance of
the exact trigger binding and threshold version plus deployment of the accepted
mode. It must not require replacement of the collection, checkpoint, portal,
weather, reporting, or analysis foundations.

## Pilot and calibration learning

The approximately three-day pilot validates exact SolarAssistant trigger
behavior after resolution, cadence, availability semantics, gaps, checkpoint
durability, interruption recovery, partial reporting, storage growth, KVBT
availability, portal reliability, sanitized prompt generation, rerunnable
interval analysis, and threshold-recommendation output. The pilot remains
useful without a perfectly clear day.

Longer calibration should seek at least one clear or mostly clear period but
must not learn only from a clear day. When available, it should include partly
cloudy transitions, overcast periods, ordinary ramps, sunrise and sunset,
stable high production, low production, source gaps, ordinary recovery, and
naturally occurring irregularities.

Use robust statistics such as medians, percentiles, and distributions. Do not
silently average suspected failures into the learned normal-production
envelope. Flag or exclude suspected failures from normal-model training while
preserving them for forensic analysis with reasons and provenance.

## Calibration weather context

### KVBT

Include KVBT from the start of the pilot. The station is approximately 0.5 to
1 kilometre from the installation and provides strong nearby ambient-weather
context, not panel-mounted irradiance or equipment weather. A localized cloud
over the installation may not appear at the airport.

Preserve when available: station identity, observation time, retrieval time,
age, temperature, dew point, relative humidity, wind, pressure, visibility,
sky condition, reported weather, raw METAR or stable source reference,
availability, and provenance. KVBT may help identify clear-day candidates but
may never qualify, suppress, reject, or veto an electrical event.

### Volcast

Volcast is optional, non-blocking context. Pilot and calibration must work
without it. It does not train the primary detector, select thresholds, or
qualify/reject events. Later comparison may preserve expected production,
issuance time when supplied, retrieval time, age, availability, and provenance.

## Durable checkpoints and lifecycle

Collection appends source observations at normal acquisition cadence. At least
every five minutes, and immediately on pause, stop, or normal completion, it
creates a durable checkpoint containing:

- immutable run ID, operating mode, lifecycle state, configured start, and
  intended end;
- last checkpoint time and latest successful observation per source;
- record, invalid, and rejected counts;
- source gaps and freshness;
- storage consumed;
- threshold/configuration version;
- recent primary-candidate and subthreshold summaries;
- pause, resume, and interruption history; and
- latest successfully analyzed interval when applicable.

Implementation must select appropriate flush, synchronization, and atomic-write
mechanics. It must not claim that an unexpected crash can never lose
observations written after the most recent durable synchronization point.

Reusable lifecycle states are `not_started`, `starting`, `collecting`,
`paused`, `resuming`, `stopping`, `completed`, `interrupted`, `recoverable`,
`failed`, and `closed`.

The run manifest preserves run ID, mode, selected sources, configured duration,
configuration version, start/end times, every state transition, interruption
history, evidence locations, analysis products, and adapter/software versions.

- **Pause:** cleanly stop or suspend acquisition, flush, checkpoint, record the
  known gap, and preserve run identity.
- **Resume:** record resumption, preserve the pause/interruption interval,
  never interpret it as zero, and normally retain run identity.
- **Stop:** deliberately flush, checkpoint, preserve observations, close the
  run, and produce a partial or final summary without deletion.

After process, server, source, or network interruption, preserve everything
durably written; mark the run incomplete; represent the gap as unavailable or
interrupted, never zero; permit a partial report and analysis through the
latest trustworthy point; show the latest checkpoint and last success per
source; and allow deliberate resume or closure as interrupted. Never conceal
interruption through silent automatic resume.

## Calibration portal design

Plan a LAN-only, unprivileged calibration/forensic portal initially hosted on
`solardt` and reusing the existing portal architecture. It displays:

- run ID/state, mode, configured interval, start/intended end, and elapsed time;
- latest five-minute checkpoint;
- source health/freshness and latest successful observation per source;
- sample, invalid, and rejected counts, gaps, storage use, and growth;
- resolved SolarAssistant production when available and trusted
  SolarAssistant/JK BMS SOC;
- ESP32 forensic telemetry and EG4 comparison values;
- latest KVBT context and optional Volcast context;
- recent primary candidates, subthreshold observations, recovery/relapse
  activity, and pause/interruption state.

Raw, trusted, estimated, comparison, derived, and contextual values remain
visibly distinct.

Narrow application controls may provide Start, Pause, Resume, Stop, Checkpoint
now, partial/final report, rerun analysis, interval selection, threshold
comparison, and sanitized ChatGPT evaluation/troubleshooting prompt generation.
They provide no shell, arbitrary command execution, unrestricted service
control, credential/authenticated raw response, device configuration,
inverter/battery control, or WAN access.

## Sanitized ChatGPT prompts

Generate copyable Markdown without credentials or sensitive responses.

The evaluation prompt includes run ID; mode; intended/actual interval;
configuration/threshold version; source identities; cadence; completeness and
gaps; clear-day candidates; primary/subthreshold summaries; recovery; KVBT;
optional Volcast; unresolved questions; and safe artifact references.

The troubleshooting prompt includes run state; intended operation; latest
checkpoint and source successes; freshness; recent sanitized errors; storage
availability; pause/interruption history; expected/actual growth; and the exact
troubleshooting objective.

Never include credentials, authorization headers, cookies, credential-bearing
URLs, complete authenticated responses, or secret-bearing output.

## Threshold-learning output

The owner-selected initial new-primary-episode floor remains an immediate valid
two-minute median of at least 1,500 W. Calibration may recommend another
version but may never silently change the accepted default.

Recommend expected cadence, baseline coverage, maximum candidate gap,
near-zero ceiling, reset hysteresis and duration, decline/recovery thresholds,
stable-recovery duration, SOC freshness, suitability of the 1,500 W floor, and
subthreshold presentation. Each recommendation preserves:

- current and proposed values;
- analysis interval and observation count;
- effects on primary and subthreshold candidates;
- false-positive and false-negative implications;
- confidence and whether more data is needed; and
- the configuration/version provenance.

A new threshold version requires owner acceptance. Cadence-dependent values
remain provisional until the exact SolarAssistant trigger is characterized.
Expected-sample coverage depends on actual cadence. Maximum candidate gaps
should use a limited number of expected intervals plus an absolute cap. SOC
freshness uses canonical observation freshness, not retained-heartbeat spacing.
Near-zero entry/reset use hysteresis. Lower-power recovery and relapse remain
relevant after initial qualification at 1,500 W, and subthreshold observations
remain outside primary counts and alerts by default.

## Risks

Preserve explicitly: unresolved trigger identity; aggregate substitution;
missing/stale/outage masquerading as zero; gradual or fast storm irradiance
change; sunset/night shutdown; copied evidence counted twice; irregular
cadence; repeated timestamps; clock uncertainty; source disagreement; one-leg
ESP32 limitations; extreme estimator artifacts; Volcast error; airport versus
equipment temperature; correlation mistaken for causation; thresholds mistaken
for physical limits; the 1,500 W threshold hiding lower-output events if
subthreshold observations are lost; lower-power reconnect/relapse evidence
lost by applying 1,500 W after qualification; detector mutation of raw
evidence; and storage/UI silently changing semantics.

## Unresolved owner decisions

The owner has decided that a new primary episode requires an immediate
two-minute baseline median of at least 1,500 W; lower baselines are
subthreshold; and lower-output recovery/relapse remains relevant inside an
already qualified episode.

Still requiring owner acceptance:

- proposed baseline coverage: at least 90 seconds and 75% expected samples;
- proposed 10-second candidate-reset debounce;
- proposed 15-second maximum candidate trigger-data gap;
- maximum acceptable SOC age;
- exact stable-recovery handling at sunset;
- dual original/local relapse-baseline comparison; and
- summary and future-portal treatment of subthreshold observations.

## Planning acceptance gates

This specification passes review only if trigger binding stays proven or
explicitly unresolved; no ambiguous field is substituted; later inventory is
separately bounded; states/transitions, baseline, duration, relapse, recovery,
closure, quality, sunset/night, roles, context, and non-causal limits are
explicit; a new episode requires a valid two-minute median of at least 1,500 W;
subthreshold declines remain distinct; 1,500 W is not applied to in-episode
recovery/relapse; missing/unavailable never becomes zero; unresolved owner
decisions stay visible; one authority contains detailed semantics; no active
superseded baseline default or low-output qualifying example remains; and
implementation, storage, analysis, live access, and portal work remain
unauthorized. The reusable calibration portion additionally requires canonical
collection/analysis separation; one-to-30-day reruns without recollection; an
approximately three-day pilot; contextual KVBT and optional Volcast; durable
five-minute checkpoints; honest interruption gaps and partial reports;
production-shaped portal/prompt interfaces; and versioned threshold
recommendations requiring owner acceptance.

## Milestone sequence

1. Independent review and owner acceptance of this specification, the 1,500 W
   rule, subthreshold behavior, reusable calibration architecture, provisional
   defaults, and proposed trigger-inventory work.
2. Authorize one complete implementation/launch milestone for the bounded
   trigger inventory, accepted or deferred binding, reusable adapters,
   lifecycle/checkpoints/recovery, interval analysis, KVBT, optional Volcast,
   LAN-only portal, sanitized prompts, tests, deployment, and approximately
   three-day pilot.
3. Review pilot completeness, source semantics, calibration recommendations,
   and any proposed threshold version.
4. Bind the exact trigger and enable official classifications only after
   semantic and owner acceptance; use shadow mode while either remains
   unresolved.
5. Later authorize production operation, historical reanalysis, and Forensics
   controls.
6. Keep nighttime-output/reconnection and further contextual integrations as
   separately bounded questions.

## Protected boundary and recovery

No source, test, fixture, adapter, collector, detector, retention, storage,
schema, portal, service, timer, credential, evidence, database, runtime,
device, firmware, network, or weather integration is authorized or changed.
Production IDs and gate 16 remain Deferred. Recovery is a normal revert of the
planning documentation commit; no operational rollback applies.
