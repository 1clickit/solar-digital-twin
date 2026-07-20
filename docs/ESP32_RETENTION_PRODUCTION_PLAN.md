# ESP32 Conservative Retention Production Plan

## Implementation status

The repository implementation is complete and synthetically validated. The
collector now supports independent `esp32-frequency-v1` and
`esp32-conservative-v1` policy state, explicit opt-in `canary` mode, exclusive
output creation, and a separate append-only manifest. The current policy and
historical retained filename remain the default. No deployment, device access,
production activation, or live canary occurred during implementation.

Chris superseded the earlier 12-hour ESP32-only canary with one authorized
approximately 24-hour coordinated ESP32, EG4, and SolarAssistant capture. The
operational procedure is `docs/COORDINATED_FORENSIC_CAPTURE.md`. It preserves
the same explicit ESP32 canary policy comparison while adding nighttime,
sunrise, daytime, sunset, battery, load, and inverter context. Canary analysis
and retirement of the current policy remain separate later milestones. No real
availability transition occurred in the completed replay evidence; entry and
restoration behavior therefore remains synthetically validated until observed
in a future approved capture.

Host runtime and HTTP/SSE hardening are separate from retention-policy design.
`docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md` preserves the current default
and independent writers while planning destination, proxy, content-type,
input-size, failure-classification, identity, file-mode, and dormant-service
safeguards. That plan does not promote `esp32-conservative-v1` or authorize a
new canary or capture.

## Decision and boundary

The adopted conservative policy will be implemented as a versioned, opt-in
retained writer and introduced through a dual-policy canary. This document is a
design and rollout plan only. It changes no collector, policy, evidence,
service, device, permission, or runtime behavior.

The stable policy identifier is **`esp32-conservative-v1`**. The existing
frequency-only policy is identified in new metadata as
**`esp32-frequency-v1`**; historical files are not renamed or rewritten.

Complete raw ESP32 evidence remains full fidelity and authoritative. A retained
writer is a disposable derived consumer of each already-written raw record.
No retained failure may prevent or roll back a successful raw write.

## Current implementation findings

The collector is `src/solar_digital_twin/collectors/esp32_sse.py` and the pure
retention helpers are in `src/solar_digital_twin/collectors/retention.py`.

- The collector polls one read-only SSE endpoint and filters 17 approved entity
  IDs. It creates one UTC receipt timestamp per approved event.
- It writes and flushes the raw line before evaluating or writing retained
  output. Retained lines are unchanged copies of raw lines.
- The current retained policy passes every non-frequency entity through.
  Generator frequency alone retains its first valid numeric observation,
  changes of at least 0.04 Hz from the last retained value, and a 30-second
  monotonic heartbeat. Invalid frequency values do not alter policy state.
- Current frequency state is per collector run and survives SSE reconnects.
  The adopted candidate requires independent state for every entity.
- Raw fields contain both `value` and `state`. Current non-frequency pass-through
  preserves unavailable/null observations, but the candidate replay classified
  availability mainly from `value`. Production normalization must treat either
  `value` or `state` equal to null/`unavailable`/`unknown` as unavailable so a
  stale numeric value cannot hide a state transition. This resolves the one
  real-data ambiguity without changing the adopted availability-preservation
  rule.
- Heartbeats use `time.monotonic()`, avoiding wall-clock corrections. UTC
  receipt timestamps remain evidence chronology, not heartbeat clocks.
- Raw and retained names share one second-resolution UTC capture stamp. The
  existing retained name is `_retained.ndjson`. Files currently open in append
  mode; the implementation must use exclusive creation for newly generated
  capture files so a collision fails before polling rather than appending to an
  existing capture.
- A retained open, processing, write, flush, or close failure is reported once,
  disables that retained output, and leaves raw collection running. A raw write
  or flush failure propagates and stops collection, which is correct because a
  collector without authoritative raw evidence must not continue silently.
- Duration expiry returns through context managers; interruption unwinds the
  same contexts. Both close the outputs. SSE reconnect uses bounded backoff.
- Existing tests cover raw-before-retained order, unchanged records, allowlist
  and UTC receipt fields, reconnect state, per-run state reset, clean closure,
  and retained open/write/flush/processing failure isolation.

One process can safely produce all three canary streams. It consumes each SSE
event once, writes raw once, then evaluates two independent pure policies. A
second collector would duplicate device polling, create competing timestamps,
and weaken provenance without providing a safety benefit.

## Exact adopted policy

`esp32-conservative-v1` is the exact `conservative_combined_60s` policy
validated in `docs/ESP32_RETENTION_REPLAY.md`:

| Entity | Deadband |
|---|---:|
| Estimated AC-coupled power | 10 W |
| Estimated active microinverters | 0.1 |
| Estimated curtailment | 0.5 percentage point |
| Generator frequency | 0.04 Hz |
| GEN L1 current | 0.1 A |
| Estimated GEN L1-L2 voltage | 0.1 V |
| Estimated AC-coupled energy | 10 source units |
| Power ramp rate | 10 source units |
| Frequency ramp rate | 0.04 source units |
| Largest power drop | 10 W |
| Total events | 1 event |

For every entity, retain the first observation, every availability transition,
and a 60-second monotonic heartbeat. Text and binary values retain every exact
change. Numeric changes compare with the last retained numeric value. Existing
frequency-event text and binary crossing indicators remain exact-change data;
no new numeric alarm threshold is introduced.

An unavailable/null observation is retained before numeric comparison and does
not overwrite the last valid numeric comparison value. Restoration to an
available value is retained independently. The implementation tests must lock
this interpretation before any canary.

## Proposed implementation architecture

### Implemented source boundaries

The synthetic-only coding milestone changed only:

- new `src/solar_digital_twin/collectors/esp32_retention.py`: stable policy IDs,
  entity deadbands, availability normalization, and per-entity conservative
  policy state;
- `src/solar_digital_twin/collectors/esp32_sse.py`: opt-in mode selection,
  independent writer coordination, exclusive output creation, versioned path
  helpers, and capture-manifest writing;
- `scripts/analyze_esp32_retention.py`: import the canonical candidate
  definition instead of maintaining a competing copy;
- new focused `tests/test_esp32_retention.py` and bounded changes to
  `tests/test_esp32_sse.py` and `tests/test_esp32_retention_analysis.py`;
- directly related documentation and audit entries.

Do not change the SSE URL, allowlist, polling, reconnect/backoff, raw record
shape, receipt timestamps, firmware, portal, database, services, or existing
default policy behavior.

### Explicit modes

Add one explicit collector selection with default `current`:

- `current`: raw plus existing `_retained.ndjson`; behavior unchanged;
- `canary`: raw, existing `_retained.ndjson`, and versioned conservative output;
- `conservative`: reserved for a later approved default transition; raw plus
  versioned conservative output.

The coding work unit implements and tests all modes but does not invoke them
against a device. `canary` and `conservative` require an explicit collector
version string representing the implementation commit. The value is
non-secret provenance and must not be discovered by invoking Git from the
collector.

### Independent writer isolation

Use a small writer slot per retained output: path, policy ID, independent policy
state, handle, count, and disabled/error status. For each parsed observation:

1. serialize once;
2. write and flush raw;
3. evaluate current retained policy and write its unchanged line if selected;
4. evaluate conservative policy independently and write its unchanged line if
   selected.

A failure in either retained slot disables and closes only that slot, reports
one payload-free diagnostic, and preserves the other retained slot and raw.
Policy state is never shared between slots. A raw failure stops the run.

### Naming and provenance

Keep the raw convention:

- `esp32_sse_<UTC>.ndjson`

During canary, use:

- current: `esp32_sse_<UTC>_retained.ndjson`;
- candidate: `esp32_sse_<UTC>_retained_esp32-conservative-v1.ndjson`;
- manifest: `esp32_sse_<UTC>_manifest.ndjson`.

Create every path exclusively. Do not overwrite or append to a pre-existing
capture. Historical names remain unchanged.

The sidecar manifest avoids inserting non-telemetry records into NDJSON. Its
first flushed record identifies manifest schema, capture ID/start UTC,
collector version, mode, raw basename, retained basenames, policy IDs, and
`canary: true|false`. On clean completion, append a second record with end UTC,
duration, counts, writer status, and stop reason. An interrupted manifest with
only its start record remains valid evidence of an incomplete run. The manifest
contains no credentials, tokens, environment, or full command line.

Manifest creation failure occurs before polling and stops startup. A later
manifest-finalization failure reports the failure but does not alter completed
evidence. Hashes are generated by the post-capture verification procedure, not
continuously by the collector.

## Implemented synthetic validation requirements

Add synthetic tests for:

1. exact policy ID, deadbands, and 60-second heartbeat;
2. independent per-entity and per-policy state;
3. first observation for every supported value type;
4. unavailable/null entry and available restoration, including stale `value`
   with unavailable `state`;
5. exact text and binary changes and repeated-value suppression;
6. numeric changes below, at, and above each deadband in both directions;
7. frequency event ordering and existing binary crossing preservation;
8. monotonic heartbeat boundaries and wall-clock independence;
9. raw write/flush before either retained evaluation;
10. candidate failure leaves raw and current retained active;
11. current retained failure leaves raw and candidate active;
12. both retained failures leave raw active;
13. raw failure stops the run;
14. exclusive file collision stops before polling;
15. clean duration expiry and interruption close all open writers;
16. reconnect preserves both independent policy states;
17. current default produces the historical two-output behavior;
18. canary produces three streams without duplicate polling;
19. manifest start/completion identity and incomplete-run semantics;
20. analyzer replay and collector policy produce byte-identical selections from
    one synthetic raw fixture;
21. bounded-window analysis includes a pre-window seed when exact transition
    counts are compared; and
22. no evidence conversion, network addition, credential handling, or parser
    breakage.

## Dual-output production canary

### Duration and timing

Run one approximately 12-hour canary scheduled to cover normal daytime
AC-coupled production. Do not manipulate the physical system to induce a fault.
Extend or schedule a second canary if the run has no meaningful production or
text/binary transition, ends early, has incomplete data, or encounters writer
or collector errors.

The canary is a separate one-approval operational work unit after repository
implementation and review. It uses one collector process and one SSE
connection. No service deployment is required unless separately justified.

### Pre-canary checklist

- repository clean, synchronized, and at the identified implementation commit;
- focused and full tests passing;
- reviewed collector invocation and stop time documented;
- VM health reviewed immediately before the capture, including root space,
  inodes, memory, swap trend, and capacity for three outputs;
- destination and predetermined raw/current/candidate/manifest basenames
  confirmed absent;
- UTC synchronization confirmed through approved read-only checks;
- ESP32 endpoint reachability confirmed read-only once;
- capture mode `canary`, policy IDs, and collector version confirmed;
- clean-stop and rollback procedure available;
- bounded health monitoring method and expected automatic stop documented; and
- post-capture metadata and SHA-256 procedure prepared.

No secret, credential, token, authorization header, or environment value is
recorded in the invocation, manifest, audit, or report.

### Monitoring

Use compact metadata/count checks; never stream telemetry to the terminal.
Observe:

- exactly one collector process is alive;
- raw and both retained files exist and grow;
- raw remains the leading authoritative count;
- malformed and backward-timestamp counters remain zero;
- retained-slot status and payload-free write/flush errors;
- reconnect count/backoff, endpoint availability, and early termination;
- disk growth and remaining filesystem/inode capacity; and
- manifest start state and expected stop time.

Stop the canary cleanly if raw writing fails, malformed records grow, time moves
backward, disk growth is uncontrolled, paths collide, a duplicate collector is
found, the run cannot preserve raw evidence, or candidate processing measurably
interferes with raw collection. A candidate-only failure may allow raw/current
collection to finish if disk and raw integrity remain healthy, but the candidate
fails the canary gate. Preserve every completed file.

## Rollback

Rollback is immediate and non-destructive:

1. cleanly stop the canary collector if it is still running;
2. record final metadata and SHA-256 for raw, current, candidate, and manifest;
3. preserve the labeled canary files unchanged;
4. select `current` for the next invocation or return to the last verified
   invocation procedure;
5. record the defect and rollback reason in `CHANGE_AUDIT.md`;
6. if repository rollback is required, use a normal revert commit and normal
   push; never reset, rebase, amend, force-push, or rewrite evidence.

The preapproved canary work unit may include its documented clean stop and mode
fallback. A new service/configuration deployment, action outside that rollback
sequence, or materially expanded availability risk requires Chris's one
approval. Destructive Git or evidence action remains always gated and is not a
valid rollback method.

## Post-canary verification

Run deterministic read-only analysis after recording pre-analysis hashes.

### Capture integrity

- filenames, manifest policy IDs, collector version, canary flag, start/end UTC;
- size, modification time, SHA-256, record count, and duration for every file;
- malformed and backward timestamps, canonical UTC, approved-entity compliance,
  entity coverage, cadence, major gaps, early stop, and final-newline state;
- unchanged raw semantics and proof that every retained record is an unchanged
  raw record in the same order.

### Retention behavior

- totals and bytes, raw percentages, reduction versus current retained, and
  per-entity counts;
- first observations, heartbeat spacing, numeric deadbands, exact text/binary
  transitions, frequency crossing/order, and availability/null transitions;
- parity between implemented policy and deterministic offline replay.

### Event and control context

If a real candidate event occurs, run the bounded correlation method from
`docs/ESP32_RETENTION_REPLAY.md` against raw/current/candidate and compare event
type, confidence, frequency/state context, chronology, provenance, and missing
context. Do not claim causation.

If no event occurs, validate stable-control behavior and all observed
transitions but do not call the canary complete forensic validation. If no real
availability transition occurs, retain synthetic coverage as an explicit
qualification. Decide whether a second passive canary is required; never induce
an unsafe event.

### Resource behavior

Perform the documented VM health review immediately after the canary. Compare
CPU, memory, swap, disk/inode growth, write/flush errors, reconnects, raw
completeness, and evidence throughput with the pre-canary review. No automatic
remediation or deletion follows the measurement.

Repeat source hashes after analysis and confirm all evidence is unchanged.

## Production acceptance gates

The candidate cannot become default unless all gates pass:

1. raw capture semantics and completeness are unchanged;
2. retained failures cannot compromise raw capture;
3. no change-attributable malformed or backward timestamp exists;
4. all 17 approved entities are represented;
5. exact binary and text transitions are preserved;
6. synthetic availability/null tests pass and any observed real transition is
   preserved;
7. frequency crossings and event ordering are preserved;
8. stable periods produce no false forensic event;
9. any observed real event retains the same defensible classification;
10. storage reduction remains materially better than current retained output;
11. CPU, memory, disk, and writer behavior are operationally acceptable;
12. rollback is demonstrated synthetically and verified procedurally;
13. documentation, audit, tests, manifests, and hashes are complete; and
14. Chris receives the concise result and qualifications before retirement of
    the current policy.

Failure preserves the canary evidence, keeps `current` as the default, records
the defect, and leads to a precise correction or revised candidate. A failed
gate is not waived for storage savings.

## Retirement of the current policy

The first implementation and canary do not authorize retirement. A later
owner-reviewed decision may stop producing the old retained stream for future
captures only after all gates pass. Existing files remain unchanged; historical
parsers retain compatibility; the transition date and policy IDs are recorded;
and dual-output rollback capability remains available for at least one later
verification capture. No historical file is renamed, converted, or deleted.

## Phased work units

1. **Repository implementation:** implement the versioned policy, independent
   writers, manifest, opt-in modes, and synthetic tests. No live execution.
2. **Canary activation:** after one approval, verify VM health and run the
   approximately 12-hour three-output capture with bounded monitoring.
3. **Canary analysis:** hash and compare all streams, evaluate gates and any
   real event/control context, and make an evidence-backed recommendation.
4. **Policy transition:** only after Chris reviews the result, change the future
   default while preserving historical and rollback compatibility.

Implementation, activation, analysis, and retirement are separate auditable
milestones.

## Remaining risks and resolved decisions

- Real availability behavior remains unobserved; synthetic coverage is
  mandatory and a real transition remains a canary qualification.
- A quiet canary may validate storage and stability but not event equivalence;
  a second passive canary may be needed.
- Three outputs increase write volume temporarily, though the healthy VM
  baseline indicates ample capacity; pre/post measurements remain mandatory.
- Manifest and filename versioning are chosen instead of telemetry metadata to
  preserve parser compatibility.
- One process with independent writers is chosen instead of duplicate polling.
- Availability derives from both `value` and `state`; restoration is retained,
  and last valid numeric state is not replaced by unavailable text.
- Current behavior remains the default until a later approved transition.
