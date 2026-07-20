# Telemetry Observation and Provenance Contract

**Contract version:** `solar-digital-twin.telemetry-observation.v1`
**Status:** Proposed authoritative contract; pending independent ChatGPT review
and owner acceptance
**Authority:** This is the single normative repository contract for normalized
telemetry observations and provenance. Source-specific documents remain
authoritative for native behavior and evidence history.

## 1. Scope and non-goals

This contract covers observations adapted from EG4 cloud data,
SolarAssistant/JK BMS, the ESP32 forensic probe, future allowlisted Home
Assistant imports, and normalized or derived observations produced by
`solardt`. The words **must**, **must not**, **required**, and **conditionally
required** are normative. Examples are synthetic and illustrative.

`solardt` is the authoritative aggregation, normalization, comparison, and
provenance layer. Raw source evidence remains authoritative; normalized
records, SQLite rows, reports, portals, APIs, Home Assistant entities, and
analyses are derived consumers or transformations.

This design does not migrate data, change a collector or retention policy,
bind a portal, select a Home Assistant transport, configure Home Assistant,
read runtime evidence, or authorize persistent ESP32 operation. Adapters,
storage, UI binding, export, and runtime decisions are separate milestones.

## 2. Current-semantics inventory

| Stream | Native identity and fields | Time semantics | Value, availability, and retention | Evidence, lineage, and role |
|---|---|---|---|---|
| EG4 cloud runtime | inverter serial; `serverTime`, `deviceTime`, status, SOC, voltage, frequency, power, temperatures; complete `raw_json` | `server_time` is interpreted as UTC; local `captured_at` is separate collector provenance; `device_time` is Central context | SQLite columns apply documented scaling, including tenths of volts and hundredths of hertz; missing fields become null | runtime evidence file/run and `runtime_snapshots`; direct EG4 cloud; EG4 SOC is an inverter estimate |
| EG4 cloud energy | inverter serial; energy counters plus complete `raw_json` | current implementation associates runtime `serverTime`; `captured_at` is local collection time | numeric energy fields are converted from tenths of kWh where possible; absent/non-numeric values become null | energy endpoint/file/run and `energy_snapshots`; direct EG4 cloud |
| EG4 cloud day series | inverter serial; row `time`, power, SOC, complete row `raw_json` | naive `sample_time` is explicitly interpreted in `America/Chicago`, including DST rules | source rows are upserted by serial and sample time; units are encoded in current column names, not always native metadata | day endpoint/file/run and `day_multiline_samples`; direct EG4 cloud; no per-row receipt timestamp in the current table |
| EG4 through HA Web Monitor | HA entity ID, raw state, unit, `last_updated`, receipt time, integration metadata | source update time may repeat across many one-second polls; polling time is not measurement time | explicit `unknown`/`unavailable` states must remain visible | `Home Assistant -> EG4 Web Monitor hybrid mode`; cloud/local/cache lineage is unresolved per entity and is not independent corroboration |
| SolarAssistant/JK BMS | topic, device, number, group, name, value, unit | source supplies no observation timestamp; every accepted row from one successful response shares one UTC millisecond receipt timestamp | allowlisted raw rows; retained SOC and slow-changing topics use exact change plus heartbeat; other approved topics may remain raw-only | source URL and NDJSON file/line or poll group; trusted battery source; combined, Battery 1, and Battery 2 remain distinct |
| ESP32 SSE | exact entity `id`, name, domain, value, state, source URL | no complete source event time; UTC millisecond receipt time is the correlation basis; equal timestamps may occur in ordered events | entity-local `unknown`, `unavailable`, null, or state transitions; raw stream is complete allowlisted input; retained streams are policy-selected subsequences | capture/manifest/file/line, collector version, stream kind, policy ID; forensic electrical source, not SOC authority |
| Future HA import | entity ID, raw state, unit, source/changed time, receipt time, integration identity/mode, selected lineage attributes | distinguish source changes from repeated polling snapshots | preserve unknown/unavailable and source capability; GET-only and allowlisted | HA is transport/display context, not automatically the root source; reflected `solardt` exports are excluded |
| `solardt` normalized | stable metric ID plus preserved native identity/value/unit | preserves all native times; selects an explicit observation-time basis | adds a deterministic canonical value/unit without replacing raw fields | transformation ID/version and input evidence reference are required |
| `solardt` derived | stable derived metric ID and parent set/selector | derivation time is separate from parent observation times | result is calculated/aggregated/inferred, never relabeled as direct | acyclic parent lineage, method/version, input window, and producer version are required |

Current SQLite tables, NDJSON schemas, report rows, and `TimedRecord` are input
formats, not this canonical envelope. `TimedRecord` currently preserves source,
normalized UTC time, original timestamp, `timestamp_kind`, values, and a
provenance dictionary; it is a useful adapter boundary but not a complete
contract implementation.

## 3. Canonical envelope

The logical envelope is a JSON-compatible object. Dotted names below denote
nested objects; a storage implementation may flatten them only through a
versioned, lossless mapping. `string(enum)` means only documented values are
allowed. Required fields may contain null only where explicitly stated.

| Field | Type and presence | Meaning, source, and invariant | Example |
|---|---|---|---|
| `contract_version` | string, required, non-null | exact contract used to produce the record | `solar-digital-twin.telemetry-observation.v1` |
| `record_kind` | enum, required | `observation`, `source_status`, or `rejection` | `observation` |
| `observation_id` | string, conditionally required | globally unique semantic record reference; required for persisted observations and parent references; never a storage surrogate | `obs:sha256:<digest>` |
| `metric_id` | string, required for observations/status | stable canonical metric identity, distinct from an occurrence | `solarassistant.jk_bms.combined.state_of_charge` |
| `source.system` | string, required | root reporting system, not merely the last transport | `solarassistant` |
| `source.device` | string, required | stable non-secret device/scope identity | `jk_bms_bank` |
| `source.metric_id` | string, required for observations | exact native identifier, unmodified | `total/battery_state_of_charge` |
| `source.role` | enum, required | `authority`, `comparison`, `forensic`, `display`, or `derived`; role is policy, not quality | `authority` |
| `source.transport` | string, required | acquisition path/protocol, kept separate from root source | `solarassistant_rest_v1` |
| `source.lineage` | array of lineage hops, required | ordered root-to-current systems/transports; unresolved hops are labeled, never guessed | `["eg4","ha_eg4_web_monitor_hybrid","home_assistant"]` |
| `time.source_at` | UTC timestamp or null, required | source-provided event/measurement time after explicit interpretation; null when absent/unusable | `2026-01-15T18:00:00.000Z` |
| `time.source_at_raw` | string or null, required | original source timestamp text before normalization | `2026-01-15 12:00:00` |
| `time.source_changed_at` | UTC timestamp or null, optional | source's last-change time when semantically distinct | `2026-01-15T17:59:30.000Z` |
| `time.received_at` | UTC timestamp, required | time `solardt` accepted the source response/event | `2026-01-15T18:00:01.123Z` |
| `time.observed_at` | UTC timestamp, required | selected correlation time; equals source time only when its semantics are established, otherwise receipt time | `2026-01-15T18:00:01.123Z` |
| `time.basis` | enum, required | `source_event`, `source_changed`, `solardt_receipt`, or `derived_window` | `solardt_receipt` |
| `time.source_timezone` | IANA zone, `UTC`, or null, required | interpretation applied to naive source text; null if no source time | `America/Chicago` |
| `time.precision` | enum, required | `day`, `second`, `millisecond`, or `unknown`; does not claim accuracy | `millisecond` |
| `time.clock_quality` | enum, required | `trusted`, `synchronized`, `unknown`, `uncertain`, or `invalid` | `unknown` |
| `time.uncertainty_ms` | nonnegative number or null, required | known bound only; null means unknown, not zero | null |
| `sequence.ingest` | nonnegative integer, required within evidence stream | preserves accepted input/file order and breaks timestamp ties | `42` |
| `sequence.source` | string/integer or null, optional | source-native sequence if provided | null |
| `value.raw_present` | boolean, required | distinguishes missing field from explicit null | true |
| `value.raw` | JSON scalar/object/array or null, required | immutable native value; null may be an explicit source value | `51.2` |
| `value.raw_type` | enum, required | `number`, `boolean`, `string`, `object`, `array`, `null`, or `missing` | `number` |
| `value.normalized` | JSON scalar or null, required | deterministic normalized value; null when none is valid | `0.0512` |
| `value.raw_unit` | string or null, required | source unit exactly as supplied or documented; null means absent/unknown | `V` |
| `value.canonical_unit` | string or null, required | unit of normalized value; null when not applicable/unknown | `kV` |
| `value.classification` | enum, required | `measured`, `source_estimated`, `source_calculated`, `normalized`, `derived`, `aggregated`, `inferred`, or `state` | `measured` |
| `availability` | enum, required | `available`, `unavailable`, `unknown`, or `not_observed` | `available` |
| `validity` | enum, required | `valid`, `invalid`, or `rejected` | `valid` |
| `capability` | enum, required | `supported`, `unsupported`, or `unknown` | `supported` |
| `quality.categories` | array of enums, required | small factual set: `direct`, `source_estimate`, `source_calculation`, `normalized`, `derived`, `lineage_uncertain`, `clock_uncertain`, `invalid`, `rejected` | `["direct","clock_uncertain"]` |
| `quality.reasons` | array of stable reason codes, required | explains categories/status without false numeric confidence | `["source_time_absent"]` |
| `transformation.id` | string or null, required | deterministic transform/derivation ID; null for untouched source value | `unit.w_to_kw` |
| `transformation.version` | string or null, required | implementation rule version | `1` |
| `transformation.method` | string or null, required | concise method, not executable code | `divide_by_1000` |
| `parents` | array of lineage references, required | empty for roots; parent observation IDs or bounded deterministic selectors for derived data | `[]` |
| `producer.name` | string, required | adapter/collector/derivation producer | `solarassistant_adapter` |
| `producer.version` | string, required | commit, release, or adapter version | `git:<commit>` |
| `evidence` | object or null, required | non-secret capture, manifest, file, table/run, record/line reference; null only when source has no durable evidence yet | `{"file":"capture.ndjson","line":42}` |
| `retention.stream` | string, required | `raw`, `retained`, `canary`, `normalized`, `derived`, or `snapshot` | `raw` |
| `retention.policy_id` | string or null, required | policy selecting this copy; null when no selective policy applies | `esp32-frequency-v1` |
| `diagnostics.reason_codes` | array of strings, required | stable payload-free reasons for abnormal/status/rejection records | `[]` |

Freshness is an evaluation, not an immutable property of the observation. A
consumer attaches or computes a projection containing `evaluated_at`,
`policy_id`, `state`, and `age_seconds`; it must not rewrite the envelope.

## 4. Stable identity

Metric IDs use lowercase dot-separated components:

`<root-source>.<transport-or-product>.<device-scope>.<semantic-metric>`

Components must be mapped in a versioned adapter registry, not generated from
display labels. They remain stable across restarts and files, preserve the
exact native ID separately, and distinguish device scope and transport. A real
native-ID change requires a new ID or a reviewed alias from old to new;
display-name changes do not. Aliases never collapse two simultaneously valid
sources.

Representative synthetic IDs:

- `solarassistant.jk_bms.combined.state_of_charge`
- `solarassistant.jk_bms.battery_1.cell_voltage_max`
- `eg4.cloud.inverter_demo.estimated_state_of_charge`
- `eg4.cloud.inverter_demo.ac_couple_power`
- `esp32.esphome.forensic_probe.generator_frequency`
- `home_assistant.eg4_web_monitor_hybrid.inverter_demo.radiator_1_temperature`
- `solardt.derived.battery.soc_disagreement_sa_minus_eg4`

The source-native topic, entity ID, field name, endpoint/table, serial/device
identity, and transport remain independent fields. Direct EG4 cloud, EG4 via
HA hybrid mode, and a future local-dongle route are different metric streams
even when their semantic metric names match.

## 5. Observation-state semantics

State uses independent axes; a single overloaded status is prohibited.

| Term | Exact meaning and record behavior | Normalization/use |
|---|---|---|
| present/valid | field exists, parses, passes source and contract rules | observation may normalize, derive, display, and export if other gates pass |
| missing | expected field/row was absent from a response/window | usually `source_status`/gap record or absence plus gap metadata; never invent a value |
| null | field was explicitly present with JSON null | observation preserves `raw_present=true`, raw null; no numeric normalization/derivation |
| unavailable | source explicitly says a currently supported metric cannot provide a value | observation preserves raw state; display/export as unavailable; not a numeric parent |
| unknown | source explicitly reports indeterminate state | preserve verbatim; display as unknown; not a numeric parent without a source-specific rule |
| stale | otherwise valid observation exceeds a named freshness policy at evaluation time | original remains valid and immutable; display/export must disclose stale; derivations require an explicit stale-parent policy |
| invalid | received value/timestamp cannot satisfy semantic/type/range rules | rejection/status record with safe reason and evidence reference; raw evidence remains; no normalized value |
| rejected | adapter refuses an input for allowlist, schema, destination, lineage, or policy reasons | `rejection` record where durable diagnostics are required; never becomes an observation |
| estimated | source itself estimates the quantity | valid observation classified `source_estimated`; never promoted to measured |
| normalized | deterministic unit/name representation of a source observation | same observation lineage with raw fields preserved and transform recorded |
| calculated | source reports a calculation rather than a direct sensor measurement | classified `source_calculated` |
| derived | `solardt` combines/transforms one or more parent observations | new observation ID and metric ID with parents/method/version |
| unsupported | capability is absent for this device/integration/version | source-status/capability record; may appear in complete source view; no invented value |

Numeric zero, boolean false, an empty but source-valid string, missing, explicit
null, unavailable, unknown, and stale are distinct. `unknown` and `unavailable`
from HA or ESPHome remain in `value.raw` and map to the matching availability
state; they must not become zero or null silently. Complete source views may
show every state. Only available, valid, sufficiently fresh observations may
be default calculation inputs or normal numeric HA exports.

## 6. Time and ordering

1. Preserve source, source-changed, receipt, and selected observation times.
2. Select source time only when field meaning and timezone are established;
   otherwise select receipt time and record `time.basis=solardt_receipt`.
3. SolarAssistant rows from one response share one receipt timestamp and poll
   grouping. ESP32 SSE uses receipt time. Neither claims source event time.
4. EG4 runtime `server_time` is UTC. EG4 day-series naive time is interpreted
   with `America/Chicago` zone rules. Ambiguous DST local times require an
   offset/fold rule from the adapter or rejection; fixed `CST` offsets are not
   acceptable year-round.
5. HA `last_updated`/equivalent is source-changed time. Repeated snapshots with
   the same timestamp are copies, not new physical measurements.
6. Naive source time without an approved timezone is invalid for canonical
   correlation. Preserve its raw text and use receipt time only if the adapter
   explicitly permits that fallback.
7. Future-dated values are valid only if parsing succeeds, but freshness is
   `future_dated` and quality includes clock uncertainty until within tolerance.
8. Unknown clock accuracy uses null uncertainty, never zero. Precision describes
   representation, not sensor accuracy.
9. Raw evidence order is immutable. `sequence.ingest` breaks equal-time ties.
   Normalized queries may order by observation time then ingestion sequence,
   but must expose disagreements between source and receipt order.
10. Derived time is explicit: point comparisons use a documented anchor;
    windows use `derived_window` plus start/end and `derived_at`. Derivation
    time never replaces parent times.

## 7. Freshness

Freshness is separate from availability and validity. It is evaluated against
an explicit time using a versioned policy chosen by source, stream, and metric
family. A freshness result contains `evaluated_at`, `policy_id`,
`basis_timestamp`, `age_seconds`, and `state` (`fresh`, `stale`,
`future_dated`, or `indeterminate`). There is no global threshold.

The basis normally follows `time.observed_at`, except a source adapter may name
a more conservative source-changed basis. HA snapshots with an unchanged
source timestamp age from that source timestamp even when polling succeeds.
Receipt-only sources age from receipt. Future-dated, invalid, or clock-uncertain
times produce `future_dated` or `indeterminate` under the policy. Missing-data
intervals are gap/status records or query results, not rewrites of the last
observation. Portals and exports must retain the policy identity and evaluation
time so freshness can be recomputed honestly.

## 8. Availability and capability

- **Transport health:** whether a request/stream succeeded; represented as a
  source-status record and never copied onto every metric as physical state.
- **Device availability:** whether the source reports or the adapter can
  establish device reachability.
- **Metric availability:** whether a supported metric currently has a value.
- **Validity:** whether the received representation is acceptable.
- **Freshness:** whether a valid observation is timely at evaluation.
- **Capability:** whether the metric exists for this device/integration/version.

Unreachable source means transport status unavailable and a gap, not fabricated
metric observations. Reachable-but-omitted is `not_observed` unless the source
defines omission as unavailable. Explicit unavailable remains unavailable.
Unsupported is capability state. A temporarily absent response row is missing,
not unsupported. No new measurement is a cadence fact, not necessarily failure.
A retention policy omitting a valid raw observation changes only stream
selection; it does not mean unavailable or physically unchanged.

## 9. Quality and authority

Use the categorical `quality.categories` and stable reason codes; do not invent
confidence percentages. Direct source measurement, source estimate, source
calculation, normalization, derivation, unresolved lineage, clock uncertainty,
and invalid/rejected data are distinct. Source authority answers which source
the project trusts for a role; quality describes a particular record;
availability and freshness describe other axes. Thus SolarAssistant/JK BMS may
be SOC authority while a particular record is stale, and EG4 SOC may be valid
and fresh while remaining a comparison estimate.

## 10. Normalization boundaries

Normalization is non-destructive and versioned. It must preserve raw value,
raw unit, native ID, source identity, and all times. It adds rather than
replaces canonical value/unit. Conversions must be deterministic and
dimension-compatible; missing units produce no conversion unless an adapter's
versioned source specification establishes the unit. Unitless values are
explicitly `1`. Sign conventions must be documented before conversion.
Display rounding never changes stored values, and normalized precision never
claims greater source accuracy.

Supported families include W↔kW, V↔mV, A, Hz, percent, documented energy units,
and temperature conversions with scale/offset. Counters preserve reset/wrap
semantics. Text and enum states are canonicalized only through explicit maps.
Null, missing, unavailable, invalid, and rejected inputs never become invented
numbers. Sources are never merged. In particular, no fixed correction may be
applied between EG4 SOC and trusted SolarAssistant SOC; disagreement is a
derived observation.

## 11. Derived observations and lineage

A derived record requires a stable derived metric ID, unique observation ID,
method ID/version, producer version, derivation time, input window when used,
classification, and parent lineage. Direct derivations list parent observation
IDs plus source/metric IDs. Large aggregates may use a bounded selector with
metric IDs, UTC window, evidence/capture references, ordering rule, filter,
input count, and an optional deterministic digest instead of embedding every
parent. The selector must reproduce the exact parent set.

Lineage is a directed acyclic graph. Before writing a derived record, the
producer must reject duplicate/self parents and any parent whose ancestor set
contains the prospective observation or export identity. Missing, stale,
unavailable, invalid, rejected, or clock-uncertain parents are handled by an
explicit method policy; omission is disclosed. Quality reasons propagate
without automatically making all results invalid.

Examples include SolarAssistant SOC minus EG4 estimated SOC (two explicit
parents); window average/range (bounded selector); an AC-couple-collapse event
(EG4 and ESP32 parents, alignment tolerances, no causal claim); and an HA entity
that references rather than replaces a `solardt` observation.

## 12. Home Assistant export and loop prevention

A future export must carry, in transport-appropriate attributes or a companion
mapping: contract version, canonical metric ID, original source/device/root
metric, observation or lineage reference, observation time, processing/receipt
time where relevant, availability, freshness evaluation and policy, quality,
derivation identity, `origin_instance=solardt`, and a stable export ID. HA must
label it as a `solardt` export, not a direct sensor register.

A future HA importer must exclude or quarantine an entity when its origin is
`solardt`, its lineage/export ID is already known, its root observation is
already present, or accepting it would create a cycle. It must not count a
copied EG4 or SolarAssistant view as independent corroboration. Transport
selection (MQTT, REST, WebSocket, or other) is deferred. The current direct
ESPHome integration remains untouched until the `ESP32 -> solardt -> HA` path
passes lineage, freshness, availability, restart, interruption, and reboot
validation in separately authorized work.

## 13. Adapter responsibilities

Every adapter must enforce an exact source allowlist; preserve native ID,
device, raw value/unit, transport, timestamp text/classification, availability,
evidence/capture reference, and producer version; map stable metric IDs through
a reviewed registry; reject malformed input with bounded payload-free reasons;
avoid substitution; and never mutate raw evidence.

### EG4

Keep runtime, energy, and day-series timestamp semantics separate. Preserve
serial, endpoint/table, raw JSON/evidence run, `captured_at`, and cloud time.
Distinguish cloud, HA hybrid, and any future local transport. Classify EG4 SOC
as a source estimate/comparison. Define freshness independently per dataset.

### SolarAssistant

Use topic plus device scope/number where needed. Keep combined, Battery 1, and
Battery 2 distinct. Record absent source time and shared poll receipt/group
identity. Preserve trusted battery-role metadata separately from record
quality, and distinguish raw observations from retention decisions.

### ESP32

Preserve exact entity ID, name, domain, raw value/state, availability, URL,
receipt-time basis, capture/manifest/file/record, collector version, stream
kind, and policy ID. Equal millisecond timestamps remain distinct by stream
order. Raw/current/conservative copies are not independent measurements.

### Home Assistant import

Preserve entity/integration identity and mode, source/change and receipt times,
raw state/unit, lineage attributes, and availability. Distinguish polls from
updates, retain uncertain hybrid lineage, never invoke services or controls,
and reject reflected `solardt` exports.

### Derived producer

Validate parent lineage and time policy, reject cycles, preserve algorithm and
producer versions, disclose incomplete parents, and never overwrite sources.

## 14. Acceptance gates

Before a source binds to normalized storage, portal, or export, its bounded
work unit must pass:

1. exact source-field and capability inventory;
2. stable metric-ID registry and alias review;
3. source-device identity validation;
4. timestamp-basis, timezone, DST, precision, and clock-uncertainty tests;
5. raw value/unit preservation;
6. deterministic normalization fixtures;
7. zero/false/empty/null/missing/unavailable/unknown/invalid/rejected tests;
8. transport and full lineage validation;
9. duplicate and feedback-loop detection;
10. restart, tie, repeated timestamp, and ordering tests;
11. gaps, source cadence, stale, and future-time behavior;
12. evidence/capture references where applicable;
13. source-specific synthetic or sanitized fixtures;
14. compatibility review against existing evidence/storage/consumers;
15. proof of no source substitution or raw-evidence mutation; and
16. explicit approval before production binding.

**Pass** means every required gate has evidence and no unresolved semantic
risk. **Qualified pass** means named non-safety limitations are preserved in
quality/lineage and the approved consumer can operate honestly despite them.
**Fail** means required identity, time, value, lineage, or safety semantics are
unknown or contradicted. A qualified pass must not be described as stronger
evidence than it is.

## 15. Compatibility and migration risks

- EG4 SQLite stores dataset-specific wide rows, uses replacement keys, embeds
  some units in column names, and lacks one canonical per-field receipt/evidence
  reference. Preserve it and adapt through views or parallel versioned records.
- SolarAssistant raw/retained NDJSON is row-oriented; poll grouping is inferred
  from shared receipt timestamps, and retained rows add reasons. Avoid rewriting.
- ESP32 raw/retained/canary streams and manifests have different schemas;
  copies must deduplicate to one root event while preserving stream provenance.
- Coordinated capture manifests provide capture-level identity but not a
  universal per-observation key.
- Reports and the operational portal depend on current CSV names and wide
  fields. Bind through translation rather than changing them implicitly.
- The synthetic future portal has presentation requirements, not a schema.
- Existing retention policies use monotonic process time for heartbeat choices;
  that decision provenance is not a physical timestamp.
- `TimedRecord` groups SolarAssistant polls and flattens selected values; it
  lacks explicit state axes and durable observation IDs.
- HA entity attributes have limited, integration-dependent metadata surfaces;
  an export may need a companion lineage map.
- Missing/inconsistent units and source-ID changes after updates require
  adapter qualification and aliases, not guesses.
- Direct EG4 and HA EG4 views may duplicate one upstream source.

Future implementation should favor source adapters plus parallel normalized
records or versioned views before any migration. Exact storage keys,
observation-ID generation, lineage digest format, HA attribute limits, and
backfill policy remain deferred until implementation inspection. Existing
evidence is never rewritten.

## 16. Versioning

Version 1 is `solar-digital-twin.telemetry-observation.v1`. Adding optional
fields or enum values that old consumers are required to ignore is backward
compatible. Removing/renaming fields, changing meanings, identity rules, time
selection, or unit semantics requires a new major version. Metric renames use
versioned aliases and deprecation periods. Adapter and transformation versions
are independent fields. Historical records keep their original contract
version. Consumers must accept explicitly supported versions and quarantine or
reject unsupported future major versions without partial reinterpretation.

## 17. Synthetic worked examples

Examples omit unchanged required fields only for readability; implementation
fixtures must include the complete envelope.

```json
{"case":"trusted SOC","metric_id":"solarassistant.jk_bms.combined.state_of_charge","source":{"system":"solarassistant","device":"jk_bms_bank","metric_id":"total/battery_state_of_charge","role":"authority","transport":"solarassistant_rest_v1","lineage":["solarassistant"]},"time":{"source_at":null,"received_at":"2026-01-15T18:00:01.123Z","observed_at":"2026-01-15T18:00:01.123Z","basis":"solardt_receipt"},"value":{"raw_present":true,"raw":82,"normalized":82,"raw_unit":"%","canonical_unit":"%","classification":"measured"}}
{"case":"ESP32 frequency","metric_id":"esp32.esphome.forensic_probe.generator_frequency","source":{"system":"esp32_esphome","device":"forensic_probe","metric_id":"sensor-01_gen_frequency","role":"forensic","transport":"http_sse","lineage":["esp32_esphome"]},"time":{"source_at":null,"received_at":"2026-01-15T18:00:02.004Z","observed_at":"2026-01-15T18:00:02.004Z","basis":"solardt_receipt"},"value":{"raw_present":true,"raw":60.01,"normalized":60.01,"raw_unit":"Hz","canonical_unit":"Hz","classification":"measured"}}
{"case":"EG4 estimated SOC","metric_id":"eg4.cloud.inverter_demo.estimated_state_of_charge","time":{"source_at":"2026-01-15T18:00:00.000Z","received_at":"2026-01-15T18:00:03.000Z","observed_at":"2026-01-15T18:00:00.000Z","basis":"source_event"},"value":{"raw_present":true,"raw":57,"normalized":57,"raw_unit":"%","canonical_unit":"%","classification":"source_estimated"},"quality":{"categories":["source_estimate"],"reasons":[]}}
{"case":"HA hybrid temperature","metric_id":"home_assistant.eg4_web_monitor_hybrid.inverter_demo.radiator_1_temperature","source":{"system":"eg4","device":"inverter_demo","metric_id":"sensor.demo_radiator_1_temperature","role":"comparison","transport":"home_assistant_rest","lineage":["eg4","eg4_web_monitor_hybrid_unresolved","home_assistant"]},"quality":{"categories":["lineage_uncertain"],"reasons":["hybrid_upstream_unresolved"]}}
{"case":"W to kW","value":{"raw_present":true,"raw":3250,"normalized":3.25,"raw_unit":"W","canonical_unit":"kW","classification":"normalized"},"transformation":{"id":"unit.w_to_kw","version":"1","method":"divide_by_1000"}}
{"case":"stale projection","freshness":{"evaluated_at":"2026-01-15T19:00:00.000Z","policy_id":"eg4.runtime.v1","state":"stale","age_seconds":3600}}
{"case":"explicit unavailable","availability":"unavailable","validity":"valid","value":{"raw_present":true,"raw":"unavailable","normalized":null,"raw_unit":"Hz","canonical_unit":"Hz","classification":"state"},"diagnostics":{"reason_codes":["source_reported_unavailable"]}}
{"case":"rejection","record_kind":"rejection","validity":"rejected","source":{"metric_id":"unexpected.entity"},"diagnostics":{"reason_codes":["source_metric_not_allowlisted"]},"value":{"raw_present":false,"raw":null,"normalized":null,"raw_type":"missing"}}
{"case":"SOC disagreement","metric_id":"solardt.derived.battery.soc_disagreement_sa_minus_eg4","value":{"raw_present":false,"raw":null,"normalized":25,"raw_unit":null,"canonical_unit":"percentage_point","classification":"derived"},"transformation":{"id":"battery.soc_difference","version":"1","method":"trusted_sa_soc_minus_eg4_estimated_soc"},"parents":[{"observation_id":"obs:synthetic:sa"},{"observation_id":"obs:synthetic:eg4"}]}
{"case":"HA export","metric_id":"esp32.esphome.forensic_probe.generator_frequency","export":{"origin_instance":"solardt","export_id":"export:synthetic:1","root_observation_id":"obs:synthetic:esp32","display_copy":true},"source":{"lineage":["esp32_esphome","solardt","home_assistant_display"]}}
```

## 18. Separated future milestones

1. Independent review and owner acceptance of this contract.
2. Source-specific adapter planning and selection of the first bounded slice.
3. Adapter implementation against offline fixtures.
4. Storage/schema and compatibility-migration planning.
5. Separately approved production normalized storage.
6. Portal binding to accepted normalized records.
7. Read-only `solardt` export to Home Assistant with loop validation.
8. Validation and separately authorized retirement/reconfiguration of duplicate
   direct ESP32 ingestion.
9. Independent owner decision on persistent or long-duration ESP32 operation.

None of these later milestones is authorized by this document.
