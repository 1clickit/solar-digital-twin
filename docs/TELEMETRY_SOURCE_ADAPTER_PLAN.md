# Telemetry Source Adapter Plan

**Status:** Owner-accepted authoritative implementation plan
**Governing contract:**
`solar-digital-twin.telemetry-observation.v1`
**Boundary:** Planning only. This document does not authorize implementation,
migration, deployment, operational evidence access, device contact, credential
use, portal binding, Home Assistant configuration, or persistent collection.

## 1. Purpose and authority

This document is the single detailed implementation plan for translating
current and planned telemetry sources into the owner-accepted observation and
provenance contract. Source-specific documents remain authoritative for native
behavior and operational history. The contract remains authoritative when this
plan is incomplete or ambiguous.

The planned path is:

```text
caller-supplied source-native record or fixture
    -> source-specific parsing and validation
    -> canonical observation, scoped status, or rejection envelope
    -> later storage, analysis, portal, or export consumers
```

The adapter layer is not a collector, storage system, retention engine, portal
model, evidence editor, or Home Assistant transport. Raw evidence, native
parsing, canonical adaptation, normalization, derived production, storage,
retention selection, freshness evaluation, and presentation remain distinct.

## 2. Design constraints

- Inputs are explicit caller-supplied mappings, rows, or bounded iterables.
- No adapter infers a production path, opens a default file, connects to a
  database, contacts a network endpoint, loads credentials, or performs I/O at
  import time.
- Adapters never mutate input objects or raw evidence.
- Diagnostics use stable reason codes and bounded metadata, never payload text.
- Mapping is deterministic for a registry version, producer version, ID
  provider, and input sequence.
- Sources remain separate. Direct EG4 cloud, EG4 through HA hybrid mode,
  SolarAssistant, ESP32, and derived values are never silently merged.
- Storage serialization and indexing remain deferred.
- Iteration is streaming/bounded where the native source format permits it.

## 3. Small shared adapter boundary

### Recommended standard-library representation

Use frozen dataclasses internally for adapter configuration, lineage hops,
evidence references, and canonical record construction; expose records as
plain JSON-compatible mappings at the boundary. Use a small `Protocol` for
adapters and injected ID providers. Avoid a validation framework until repeated
implementation proves standard-library validation insufficient.

This provides typed construction and immutability without selecting a database,
serialization framework, or message bus. `TypedDict` may document returned
mappings but is not sufficient alone for runtime validation. Plain mappings
alone are too easy to construct inconsistently.

### Proposed protocol

```text
AdapterContext
  contract_version
  registry_version
  producer_name
  producer_version
  observation_id_provider
  record_id_provider

SourceAdapter.adapt(input_record, context, evidence_reference, ingest_sequence)
  -> bounded iterator[canonical record mapping]
```

One input may yield:

- one or more accepted observations;
- one scoped status record;
- one rejection record; or
- no record only when the documented caller-level grouping operation has not
  yet reached a complete input boundary.

The adapter must return diagnostics in canonical records or a bounded
payload-free error result. Exceptions are reserved for programming/configuration
errors; malformed source data should normally produce a rejection record.

### Common construction pipeline

1. Validate caller input type and required native fields without modifying it.
2. Identify root source, device scope, native metric, and acquisition path.
3. Resolve the versioned metric-registry entry; reject absent or ambiguous
   mappings.
4. Classify source time, receipt time, ordering, state, raw value/type, and unit.
5. Construct structured root and acquisition lineage hops.
6. Apply only the registry-authorized deterministic normalization.
7. Construct the complete contract record profile.
8. Validate record-profile applicability, enum support, and acyclic lineage.
9. Return a new JSON-compatible mapping.

## 4. Canonical record construction

The common builder must require every field applicable to the chosen profile;
it must not fill semantic fields by guessing.

| Contract area | Planned construction rule |
|---|---|
| Version/kind | Exact accepted contract version; `observation`, `status`, or `rejection`; observations also select `root`, `normalized`, or `derived` product kind |
| IDs | Obtain observation-only `observation_id` and per-persisted-instance `record_id` from separate injected provider methods after their distinct inputs are finalized |
| Metric identity | Resolve only through the versioned metric registry; status scope controls whether `metric_id` is required or null |
| Source | Registry provides root system, acquisition path, role, device-scope rule, and native-ID rule; input supplies actual device/native values |
| Lineage | Build minimal structured hops in root-to-current order; unresolved facts remain explicit |
| Time | Preserve raw source text; normalize only with an approved timezone rule; always preserve receipt/detection time and selected basis |
| Sequence | Caller supplies monotonically increasing ingest sequence within the input/evidence stream; source sequence remains separate |
| Value | Preserve raw presence, value, type, and unit; normalization adds fields and transformation metadata without replacement |
| State | Map availability, validity, capability, and quality independently; transport outages use scoped status records |
| Parents | Empty for root observations; explicit source parent for normalized observations; IDs or deterministic selectors for derived observations |
| Producer | Exact adapter/producer name and code version from context |
| Evidence | Caller supplies a non-secret structured reference; adapter validates form but never opens the target |
| Retention | Caller/source metadata identifies raw, retained, canary, snapshot, normalized, or derived stream and policy; no stream is treated as independent physical evidence |
| Diagnostics | Stable bounded reason codes; no raw payload or secret-bearing exception text |

### ID boundary

Production ID encodings remain deliberately deferred. Later implementation
must expose separate `observation_id_for(...)` and `record_id_for(...)` methods
(or equivalently distinct protocols) so their semantics cannot be conflated.

An **observation ID** identifies one semantic observation occurrence. For a
receipt-only SolarAssistant occurrence, its future descriptor uses established
facts such as root source, the `jk_bms` canonical telemetry namespace, device
scope, native and canonical metric identities, `solarassistant_rest_v1`
transport, completed poll-group or accepted-response occurrence, accepted
receipt/observation time, and a source-occurrence discriminator when required.
It excludes copy-local file/line references,
retention stream/policy, copy-local ingest sequence, producer version,
serialization, and copy-specific evidence paths. Consequently it remains
stable across raw/retained/current/conservative/canary copies, file relocation,
serialization differences, and adapter reprocessing that does not change the
semantic occurrence. A normalized or derived observation is a new semantic
observation with its own observation ID and explicit root/parent references.

A **record ID** identifies one persisted canonical record instance. Its future
descriptor may include record kind, observation ID where applicable, product
kind, producer/transformation version, retention stream/policy, copy/evidence
reference, and record-specific status or rejection identity. Thus raw and
retained records for one root occurrence share the root observation ID but have
different record IDs and retention/evidence provenance; they are not separate
physical measurements.

Before implementation, device-scope and poll-group occurrence rules,
evidence-reference shapes, and record-copy semantics must be finalized for the
selected source. Offline fixtures use separately injected deterministic test
providers or methods, such as distinct counters keyed by fixture case. Tests
must not imply that either format is the production encoding. Later production
algorithms plug into these boundaries without changing source parsing or
record construction.

## 5. Versioned metric registry

### Recommended format

Begin with a small, reviewable Python mapping in a dedicated adapter module,
using immutable dataclass entries and no import-time I/O. Python avoids adding a
YAML/schema dependency, permits focused validation, and matches the existing
standard-library-heavy project. If non-developers later need to edit mappings,
a versioned JSON representation can be evaluated separately.

Each entry plans these fields:

- registry version;
- root source and acquisition path;
- device-scope rule;
- exact native metric identifier;
- stable canonical metric ID;
- semantic quantity and source role;
- expected raw type and capability applicability;
- raw unit, unit basis, and unit-mapping reference;
- sign convention;
- optional normalization ID/version;
- aliases/deprecations; and
- uncertainty/qualification notes.

Registry lookup uses stable native identifiers, never display labels. Direct
EG4 cloud, EG4 via HA hybrid, and future local EG4 paths have distinct entries.
SolarAssistant combined/Battery 1/Battery 2 remain distinct. ESP32 entries
preserve exact entity IDs. Aliases represent actual replacement over time and
must never combine simultaneously valid sources. EG4 SOC remains comparison/
source-estimated; SolarAssistant combined SOC remains battery authority.

For the selected combined-SOC entry, the canonical metric ID is
`solarassistant.jk_bms.combined.state_of_charge`: `solarassistant` is the root,
`jk_bms` is the stable canonical namespace for JK BMS telemetry reported by
SolarAssistant, and `solarassistant_rest_v1` is the sole source transport. The
namespace does not represent a direct JK protocol, hardware connection,
collector, polling source, address, or credential path.

## 6. Unit-mapping registry

Unit rules may be fields within the metric registry initially; a separate unit
registry is warranted only after reuse appears across sources.

| Source case | Planned rule |
|---|---|
| SolarAssistant | Preserve nonempty `unit` verbatim as `source_supplied`; missing unit is `absent` and blocks numeric normalization requiring dimension |
| EG4 | Current raw responses do not consistently transmit unit metadata; documented field/scaling entries are `adapter_specified` with mapping ID/version |
| ESP32 | Current persisted record omits a unit field even if ESPHome supplies metadata elsewhere; approved entity specifications may establish `adapter_specified` units only after fixture/source documentation review |
| HA | Preserve `unit_of_measurement` when present as source-supplied-by-HA, while lineage states HA/integration mediation; absent stays absent |
| States/text | Use `not_applicable`; do not manufacture a unit |

Mappings declare dimension, raw unit, canonical unit, scale/offset, sign
convention, source precision if known, and version. Conversion is prohibited
when dimension or unit is unknown. Display rounding never changes canonical
storage values. A mapping change requires fixture review and a version change;
it must not rewrite old evidence.

Qualification is required for EG4 fields whose units exist only in SQLite
column names/current conversion code, ESP32 entities whose NDJSON omits units,
HA integrations with inconsistent attributes, and any SolarAssistant row with
missing/empty unit.

## 7. Source-specific mapping matrices

### 7.1 EG4 cloud runtime

| Concern | Planned mapping |
|---|---|
| Native input | Caller-supplied raw runtime mapping or explicitly supplied SQLite row plus parsed `raw_json`; adapters do not open SQLite |
| Identity | Root `eg4`; acquisition `cloud`; device from inverter serial; native metric from raw field/registry entry |
| Role | SOC `comparison` and `source_estimated`; direct telemetry otherwise source-specific measured/calculated classification |
| Time | `serverTime`/`server_time` interpreted UTC as source time; `deviceTime` retained as context; `captured_at` retained separately and is not silently called receipt time |
| Precision/clock | Preserve representation precision; source clock quality remains `unknown` unless separately established |
| Order | Caller row order plus ingest sequence; replacement/upsert history cannot prove arrival order |
| Value/unit | Preserve raw field; existing `vBat / 10`, `fac / 100`, `feps / 100`, power/temperature rules become versioned adapter-specified mappings |
| State | Missing fields are missing/not observed, not zero; status text/code is state; malformed numeric values reject that metric, not unrelated fields |
| Capability | Registry/device-version applicability; unsupported only with evidence, otherwise unknown |
| Evidence | Caller-supplied run/dataset/file/hash/table/row reference; raw JSON remains authoritative |
| Retention | Current SQLite snapshot is `snapshot`; it is not raw evidence and does not erase raw-file lineage |
| Lineage | EG4 root hop followed by direct cloud acquisition hop |
| Risks/fixtures | Wide row, raw/normalized duplication, `INSERT OR REPLACE`, nullable `server_time`, scaling, and lack of explicit receipt timestamp; fixtures cover complete, missing, malformed, zero, status, and estimated SOC |
| Gates | Especially 2–8, 10–12, 14–16; receipt semantics may initially qualify rather than pass |

### 7.2 EG4 cloud energy

| Concern | Planned mapping |
|---|---|
| Native input | Caller-supplied energy response or supplied SQLite row/raw JSON |
| Identity/role | Root `eg4`, acquisition `cloud`, inverter serial; endpoint/dataset remains distinct from runtime |
| Time | Current sync associates runtime `serverTime`; record that association explicitly rather than claiming the energy endpoint supplied it; preserve local `captured_at` |
| Value/unit | Raw counters preserved; `n10` tenths-of-kWh conversion becomes versioned adapter mapping; nonnumeric/absent remains null/missing |
| Counters | Registry declares cumulative/daily counter semantics; reset, wrap, timezone-day boundary, and monotonicity remain source-specific quality concerns |
| State/capability | Per-field rejection/status; no inference from runtime transport health |
| Evidence/retention | Energy dataset/run/file/table reference; snapshot stream; raw JSON authority retained |
| Lineage | EG4 root plus cloud energy acquisition; linked runtime time is a provenance association, not a parent measurement unless explicitly modeled |
| Risks/fixtures | Timestamp association, counter reset/day rollover, scaling, null/nonnumeric fields, independent freshness; synthetic fixtures cover each |
| Gates | All sixteen; gates 4, 5, 6, 11, and 14 require particular qualification |

### 7.3 EG4 day series

| Concern | Planned mapping |
|---|---|
| Native input | Caller-supplied day row or supplied SQLite mapping and row `raw_json` |
| Identity | EG4/cloud, inverter serial, raw row field, dataset `day_multiline_samples` |
| Time | Naive `sample_time` interpreted with `America/Chicago`; preserve raw text; DST gaps/folds require fixtures and fail/qualify when ambiguous |
| Receipt | No historical per-row receipt exists; do not invent it. A future adapter invocation time may be detection/processing metadata but cannot masquerade as historical receipt. Contract-profile feasibility requires an explicit compatibility decision before production backfill |
| Order | Native sample time plus caller ingest order; primary key `(serial_num,sample_time)` and replacement behavior may hide revisions |
| Value/unit | Raw row values preserved; units encoded in column names are adapter-specified mappings, not transmitted metadata |
| State/capability | Missing row/field and null remain distinct; invalid timestamp yields rejection; capability requires registry evidence |
| Evidence | Dataset file/run/hash and row reference where available; SQLite alone may be qualified provenance |
| Retention/lineage | Snapshot/translated view; EG4 root plus cloud day-series acquisition |
| Risks/fixtures | DST fold/gap, no receipt time, replacement key, raw-column scaling, table/raw disagreement; synthetic Central-time boundary fixtures required |
| Gates | Gates 4, 10, 12, and 14 are likely qualified until receipt/revision semantics are decided |

### 7.4 SolarAssistant / JK BMS

| Concern | Planned mapping |
|---|---|
| Native input | Caller-supplied SolarAssistant REST-derived NDJSON-like row or completed synthetic poll group; no path opening or direct JK input in the adapter |
| Identity | `metric_id=solarassistant.jk_bms.combined.state_of_charge`; `source.system=solarassistant`; stable telemetry namespace `jk_bms`; `source.device=jk_bms_bank`; `source.metric_id=total/battery_state_of_charge`; combined, Battery 1, and Battery 2 remain distinct |
| Role | Combined and per-battery BMS telemetry; combined SOC uses `source.role=authority` |
| Transport | `source.transport=solarassistant_rest_v1`; all JK telemetry enters exclusively through SolarAssistant REST, while `jk_bms` names the represented telemetry family |
| Time | No source observation time; all rows in one successful response share UTC millisecond `received_at_utc`, selected as observation time; preserve poll-group identity |
| Order | Input line/row order and ingest sequence; same timestamp does not collapse separate metrics |
| Value/unit | Preserve value/type and source-supplied unit; numeric validation is metric-specific; no guessed unit |
| State | Missing/malformed topic, absent value, nonnumeric numeric metric, unknown/unavailable, and unapproved topic yield bounded rejection or explicit state according to fixture rules |
| Capability | Topic allowlist plus device-scope registry; omission from one poll is `not_observed`, not unsupported |
| Evidence | Caller-supplied capture/file/line or poll-group reference; protected operational path is never embedded or opened by tests |
| Retention | Raw and retained records share one root `observation_id`, have distinct `record_id` values, and differ in retention/evidence provenance; retained reason/heartbeat is selection provenance, not a new measurement |
| Lineage | Root hop identifies `solarassistant`, `jk_bms_bank`, and native metric `total/battery_state_of_charge`; lineage preserves the `jk_bms` telemetry namespace and `solarassistant_rest_v1` transport without inventing a direct JK source |
| Direct-access boundary | Solar Digital Twin never polls or connects to either JK BMS directly; no direct protocol, address, credential, collector, polling, connection, or control path is planned |
| Risks/fixtures | No source time, mutable display fields, identity tuple currently includes name/unit, inferred poll grouping, raw/retained duplication; synthetic fixtures cover combined SOC first |
| Gates | Strong candidate for full offline gates using synthetic fixtures; production evidence/path validation remains later |

### 7.5 ESP32 SSE

| Concern | Planned mapping |
|---|---|
| Native input | Caller-supplied accepted record plus explicit manifest/capture metadata; native SSE framing remains collector responsibility |
| Identity/role | Root `esp32`, acquisition `esphome`, exact allowlisted entity ID, forensic role |
| Time/order | No complete source event time; receipt time is observation time; equal millisecond times remain distinct through ingest/file sequence |
| Value/unit | Preserve `id`, name, domain, value, state; current evidence has no unit field, so approved entity mapping is adapter-specified only after qualification |
| State | Entity-local null/`unknown`/`unavailable`; availability transitions are distinct from transport health; unapproved IDs reject |
| Capability | Fixed 17-entity allowlist for current probe/version; version changes require registry review |
| Evidence | Capture ID, manifest schema/file, collector version, file/line, source URL |
| Retention | Raw/current/conservative/canary copies reference one root event; stream and policy retained; copies never count independently |
| Lineage | ESP32 root and ESPHome/SSE acquisition hop; `solardt` retained-copy selection is provenance, not physical source |
| Risks/fixtures | Units absent, retained duplicate detection, manifest/record split, equal timestamps, availability strings, policy evolution |
| Gates | Synthetic fixtures can pass most; real manifest/evidence references and device-version capability remain later qualification |

The installed runtime remains static/dormant after its completed finite
verification. This plan neither inspects nor changes it.

### 7.6 Future Home Assistant import

| Concern | Planned mapping |
|---|---|
| Native input | Caller-supplied allowlisted HA state mapping and integration metadata; transport unselected |
| Identity | HA-native metrics use root `home_assistant`; transported EG4/other sources preserve that root and use HA acquisition path; exact entity ID remains a lineage reference |
| Time/order | Preserve source `last_updated`/equivalent and `solardt` receipt; repeated polls with unchanged source time are snapshots, not physical updates |
| State/unit | Preserve raw state, `unknown`, `unavailable`, and unit attribute; integration-mediated unit provenance remains explicit |
| Capability | Entity/integration/version allowlist; omission does not prove unsupported |
| Security | Read-only/GET-only semantics; never invoke control entities/services; credentials and transport are outside adapter code |
| Lineage | Structured root, unresolved integration/acquisition, and HA transport hops; hybrid cloud/local/cache remains `unresolved=true` |
| Loops/duplicates | Reject/quarantine known `solardt` export IDs, roots already observed, repeated snapshots, and cycles |
| Evidence | Future capture/snapshot reference supplied by caller; no current operational access |
| Risks/fixtures | Limited attributes, entity renames, hybrid ambiguity, duplicate EG4 route, stale repeated values, reflected exports |
| Gates | No production binding until transport, credential authority, lineage, restart/reconciliation, and loop fixtures pass |

#### Deferred `source.metric_id` fallback

Two viable options remain deliberately unresolved:

1. **Null root-native ID plus HA entity in lineage.** This is most honest when
   the upstream EG4 native metric cannot be proven, but root/normalized
   observation profiles currently require a native ID and may therefore need a
   qualified profile interpretation or contract clarification.
2. **Namespaced unresolved proxy ID**, for example an explicitly labeled
   `ha_entity_proxy:<entity_id>`, while preserving the exact entity in lineage.
   This satisfies non-null shape but risks consumers mistaking the proxy for an
   EG4-native identifier.

Adapter planning must obtain per-entity integration evidence and an owner-
reviewed compatibility decision before choosing. It must not silently use the
HA entity ID as though EG4 transmitted it. This does not block other sources or
the selected first slice.

### 7.7 Normalized producer

| Concern | Planned mapping |
|---|---|
| Native input | One valid canonical root observation supplied by the caller; never raw evidence directly |
| Identity/role | Preserve root system/device/native metric and stable canonical metric; product kind becomes normalized without creating a new physical source |
| Time/order | Preserve source, receipt, and observation time; add producer processing/receipt semantics and deterministic ingest order |
| Value/unit | Preserve raw value, raw unit, unit basis, and source nature; add only registry-authorized canonical value/unit and `normalized_source_value` result nature |
| State/capability | Preserve availability, validity, capability, freshness inputs, and quality; unavailable, invalid, or unknown-dimensional values are not converted |
| Transformation | Record deterministic ID, version, method, sign/scale rule, and source-parent observation reference |
| Evidence/retention | Preserve evidence reference; mark normalized stream/policy without treating it as independent physical evidence |
| Lineage | Append one normalization hop to the existing acyclic lineage |
| Risks/fixtures | False precision, guessed dimensions, lost estimate/calculation nature, sign errors, duplicate physical counts, and cycles; fixtures cover each |
| Gates | All sixteen, with deterministic unit fixtures, parent identity, cycle checks, and explicit later production-binding approval |

### 7.8 Derived producer

| Concern | Planned mapping |
|---|---|
| Native input | Explicit canonical parents or a caller-supplied deterministic bounded selector result |
| Identity/role | Stable `solardt.derived` metric mapping and derived producer role; no native source metric is fabricated |
| Time/order | Explicit anchor/window/derived/receipt fields; deterministic parent and output ordering |
| Value/unit | Result is labeled derived, aggregated, or inferred; output dimension/unit and precision follow a versioned method |
| State/capability | Method defines missing/stale/unavailable/invalid parent policy and categorical quality propagation |
| Transformation | Record method and producer versions, input window/anchor, parent IDs or reproducible bounded selector, and transformation order |
| Evidence/retention | Preserve parent evidence references; derived stream is not raw evidence |
| Lineage | Validate parent lineage, append one producer hop, and reject cycles or self-ancestry |
| Risks/fixtures | Incomplete parents, clock uncertainty, unbounded selectors, circular provenance, and unsupported causal claims; fixtures cover point, window, and rejection cases |
| Gates | All sixteen, including selector reproducibility, cycle rejection, quality propagation, and separate production-binding approval |

## 8. Existing implementation inventory

| Component | Classification | Planned use |
|---|---|---|
| EG4 client/sync collector | Semantic reference only; preserved compatibility | Native endpoint/field and capture-run behavior; must not become adapter I/O |
| `eg4_database.py` schema/upserts | Semantic reference; later translation/view candidate | Documents scaling, wide rows, keys, raw JSON, and null behavior |
| EG4 reports/portal generator | Preserved current consumer; later canonical wrapper/binding | Freshness and field compatibility; no immediate replacement |
| SolarAssistant collector | Semantic reference and unchanged evidence producer | Record shape, allowlist, shared poll receipt time |
| SolarAssistant retention/shared retention | Reusable semantic reference; remain separate | Stable-selection behavior and reasons, not adaptation |
| ESP32 SSE collector | Semantic reference and unchanged evidence producer | Allowlist, record/manifest shape, ordering, version, and safety |
| ESP32 retention policies | Reusable unchanged outside adapter | Availability mapping and stream policy provenance; no physical dedup logic |
| `normalize_timestamp` | Reusable behind a stricter wrapper | ISO/zone normalization; adapter adds precision, raw text, clock quality, DST policy |
| `TimedRecord` | Preserved for compatibility but superseded later at canonical boundary | Too small for complete state, IDs, units, profiles, lineage, and evidence |
| `correlation_adapters.py` JSON/SQLite readers | Lower-level parsing ideas reusable behind wrappers; current adapters remain specialized | Bounded read-only behavior, payload-free errors, grouping, ordering |
| Forensic correlation analyzer | Existing consumer; later canonical-input option | Keep stable until canonical adapters prove equivalence |
| Current tests/fixture builders | Patterns reusable; fixtures must be new synthetic canonical cases | Temporary SQLite/NDJSON, timestamp/state edge cases, immutability |
| No existing common registry/normalizer/provenance utility | New later implementation | Keep minimal and standard-library-first |

### Correlation-adapter decision

Do not replace current forensic adapters first. Keep them specialized and
stable for reproducibility. Later, share pure lower-level timestamp/row parsing
where semantics truly match, then add a canonical-to-`TimedRecord` compatibility
adapter or let a separately versioned analyzer consume canonical observations.
Require synthetic equivalence tests before switching. This avoids forcing the
full contract into a proven bounded forensic workflow or duplicating I/O in the
new adapter layer.

## 9. Compatibility strategy

- **EG4 SQLite:** adapt caller-supplied rows or read-only translation views
  later; no migration/backfill until receipt and replacement semantics resolve.
- **NDJSON:** preserve schemas and files; parse into new records in parallel.
- **Raw/retained/canary:** retain stream/policy identity and deduplicate by root
  reference; never rewrite or count copies independently.
- **Manifests:** retain capture-level provenance and link record references;
  do not flatten manifests into telemetry values.
- **CSV/reports/operational EG4 portal:** remain current consumers; later use
  translation or parallel canonical queries after equivalence testing.
- **Future portal:** bind only accepted canonical records and freshness
  projections; complete source tabs retain null/unavailable/unsupported fields.
- **TimedRecord/analyzer:** preserve now; add explicit compatibility boundary
  later rather than changing established event results.
- **HA metadata:** plan companion lineage mapping if entity attributes cannot
  carry the contract safely.
- **Future storage:** select schema only after adapter fixtures prove envelope
  shapes, volume, identity, and query needs.

Parallel adaptation and versioned views are preferred over migration. Raw
evidence and existing operational products remain untouched.

## 10. Sixteen acceptance gates

### Planned coverage

The matrix describes future coverage only. **C** means the adapter plan calls
for a fixture, test, review, or evidence item for that gate. It is not Pass or
Qualified Pass and makes no readiness claim.

| # | Gate / concrete evidence | EG4 runtime | EG4 energy | EG4 day | SolarAssistant | ESP32 | HA import | Producers |
|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Exact field/capability fixtures | C | C | C | C | C | C | C |
| 2 | Registry/alias review | C | C | C | C | C | C | C |
| 3 | Device identity validation | C | C | C | C | C | C | C |
| 4 | Time/zone/DST/precision/clock tests | C | C | C | C | C | C | C |
| 5 | Raw value/unit preservation | C | C | C | C | C | C | C |
| 6 | Deterministic normalization fixtures | C | C | C | C | C | C | C |
| 7 | Zero/false/empty/null/missing/unavailable/unknown/invalid/rejected | C | C | C | C | C | C | C |
| 8 | Transport and structured lineage | C | C | C | C | C | C | C |
| 9 | Duplicate/export-loop detection | C | C | C | C | C | C | C |
| 10 | Restart/tie/repeated-time/order | C | C | C | C | C | C | C |
| 11 | Gap/cadence/stale/future-time | C | C | C | C | C | C | C |
| 12 | Evidence/capture references | C | C | C | C | C | C | C |
| 13 | Synthetic/sanitized fixtures | C | C | C | C | C | C | C |
| 14 | Existing evidence/storage/consumer compatibility | C | C | C | C | C | C | C |
| 15 | No substitution/evidence mutation | C | C | C | C | C | C | C |
| 16 | Explicit production-binding approval | C | C | C | C | C | C | C |

### Current gate disposition

Every source and producer is currently **Deferred** for production binding
because its canonical adapter and required evidence do not yet exist. The
selected SolarAssistant slice has strong planned coverage but remains Deferred
until it is implemented, tested, independently reviewed, owner-accepted, and
separately approved for production binding.

Known likely qualifications must remain visible during later evaluation: EG4
runtime/energy receipt and revision semantics; EG4 day-series receipt, DST, and
replacement semantics; ESP32 unit provenance; HA device identity, hybrid
lineage, duplicate-loop behavior, and evidence references; and producer parent
and selector reproducibility. These are not Qualified Pass results today.

**Pass** may be assigned only after all applicable evidence exists and
independent review confirms no unresolved semantic risk. **Qualified Pass**
preserves a named limitation in records and restricts consumers accordingly.
**Fail** applies when evidence contradicts required identity, time, value,
lineage, compatibility, or safety semantics and blocks binding. **Deferred**
means implementation, evidence, review, or approval is incomplete; it is not a
pass.

## 11. Candidate first slices

Scores are 1 (weak) to 5 (strong); higher lock-in score means lower lock-in.

| Candidate | Clarity | Coverage | Fixtures | Safety | Reuse | Size | Testability | Storage independence | Dependency readiness | Low lock-in | Downstream value | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ESP32 generator frequency from synthetic NDJSON | 4 | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 3 | 4 | 4 | 48 |
| SolarAssistant SOC from synthetic poll fixtures | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 55 |
| EG4 runtime SOC/frequency from synthetic SQLite | 3 | 5 | 4 | 5 | 4 | 3 | 4 | 4 | 3 | 3 | 5 | 43 |
| Minimal shared envelope validator plus one source | 5 | 5 | 5 | 5 | 5 | 3 | 5 | 5 | 4 | 5 | 5 | 52 |

### Selected slice

Select **minimal shared envelope model/validator plus SolarAssistant combined
SOC from synthetic poll fixtures**. This is candidate 4 instantiated with the
highest-readiness source from candidate 2. It is one coherent slice: the shared
model is implemented only to the extent needed to construct and validate the
SolarAssistant cases, avoiding a speculative universal framework.

It covers trusted role, stable metric identity, receipt-only time, poll
grouping, source-supplied units, one root source-value product, raw/retained
provenance, scoped status, rejection, immutable input, and separate injected
observation/record IDs. It avoids SQLite, uncertain EG4 receipt/unit semantics,
ESP32 unit qualification,
HA ambiguity, live paths, storage, and credentials.

## 12. Exact later implementation boundary

### Proposed files

- `src/solar_digital_twin/telemetry/__init__.py`
- `src/solar_digital_twin/telemetry/model.py`
- `src/solar_digital_twin/telemetry/registry.py`
- `src/solar_digital_twin/telemetry/adapters.py`
- `src/solar_digital_twin/telemetry/solarassistant_adapter.py`
- `tests/fixtures/telemetry/solarassistant_combined_soc.json`
- `tests/test_telemetry_model.py`
- `tests/test_solarassistant_adapter.py`

Exact names may be adjusted during the later bounded work if repository
conventions require it; scope may not expand silently.

### Interfaces and subset

- Frozen context/lineage/registry dataclasses and JSON-compatible output.
- Minimal adapter `Protocol` and separate injected deterministic fixture methods
  for observation IDs and record IDs.
- Registry version `1` entries only for combined SolarAssistant SOC.
- One completed synthetic poll group with `total/battery_state_of_charge`.
- Exactly one normal valid root observation with metric ID
  `solarassistant.jk_bms.combined.state_of_charge`, source system
  `solarassistant`, device `jk_bms_bank`, native metric
  `total/battery_state_of_charge`, authority role, stable `jk_bms` telemetry
  namespace, and exclusive `solarassistant_rest_v1` transport.
- That root preserves numeric raw SOC, equal normalized numeric SOC, raw and
  canonical unit `%`, `raw_unit_basis=source_supplied`,
  `source_nature=measured`, `result_nature=source_value`, and null
  transformation fields (`transformation.id`, version, and method are null).
- Raw and retained records share the same root observation ID but have distinct
  record IDs and retention/evidence provenance.
- Source-level transport status fixture without metric fabrication.
- Rejections for malformed mapping, missing/invalid receipt time, unapproved
  topic, missing value, invalid numeric SOC, missing unit where normalization is
  requested, and registry mismatch.

### Focused tests

- complete envelope/profile validation and JSON compatibility;
- exact metric/source/device/role/lineage mapping;
- receipt-only time and shared poll grouping;
- zero SOC preserved as valid, null/missing/unavailable distinct;
- exact canonical/source/device/native/acquisition/role/transport mapping;
- source-supplied percent unit, equal raw/normalized value, source-value nature,
  and null transformation metadata;
- input deep equality before/after adaptation;
- raw/retained copies share root observation ID, differ in record ID and
  retention/evidence provenance, and are counted once as a measurement;
- source outage emits one source-scoped status;
- bounded reason codes contain no payload;
- injected test IDs are deterministic and explicitly non-production;
- unsupported enum/profile fields fail safely; and
- no imports open files, databases, networks, credentials, or runtime paths.

The selected slice emits no additional normalized observation because no
value, unit, sign, precision, or semantic transformation occurs. A later real
versioned transformation may emit `product_kind=normalized` with its own
observation ID, the root observation as parent, and explicit transformation
ID/version/method; that behavior is outside this slice.

### Acceptance criteria and exclusions

The later slice passes when focused and full offline tests, repository health,
immutability, deterministic output, and exact scope checks pass. It must not
open real NDJSON, evidence, SQLite, reports, credentials, or network endpoints;
change collectors or outputs; select production ID encoding or storage; add EG4,
ESP32, HA, portal, export, persistence, or migrations; or access installed
runtime. Recovery is a normal revert of the later implementation commit; no
operational rollback applies.

## 13. Deferred decisions and milestone sequence

Still deferred:

- final HA unresolved-root `source.metric_id` fallback;
- production record/observation ID encoding;
- exact persistent serialization and database schema;
- historical backfill and EG4 missing-receipt policy;
- ESP32 unit-specification qualification;
- HA transport, credentials, reconciliation, and export metadata surface;
- portal binding and replacement of current reports;
- persistent or long-duration ESP32 operation; and
- the separate unscheduled `solardt` reboot/recovery procedure.

Independent review passed and Chris accepted this plan and its selected
synthetic-only slice. Acceptance establishes planning authority only; separately
authorize implementation. Adapter implementation would not authorize storage,
production binding, device contact, or deployment.
