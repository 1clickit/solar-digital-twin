# ESP32 Conservative Retention Replay

## Decision

**Adopt** the documented conservative candidate as the basis for a separately
reviewed production-retention implementation. This work changed no collector or
production policy. Complete raw evidence remains authoritative.

The candidate preserved the three validated event classifications, the stable
control, every binary/text transition across the full capture, UTC chronology,
entity identity, and source provenance while reducing the current retained
stream by 84.35% by records and 75.82% by bytes.

## Evidence identity

| Stream | Records | Bytes | SHA-256 |
|---|---:|---:|---|
| Raw | 431,513 | 156,174,965 | `c48d647f97175261e7e015886001acc5bb06207e5336b3677e949ef9fe447059` |
| Current retained | 394,327 | 149,568,755 | `f2f78957078ed50cd9162f54e669e00e1a23a5e9149c67092d8c11b38e06d6ca` |
| Candidate replay | 61,724 | 36,174,692 | `bb4e779963a6b4147784e18a73bf2067f6593af51f881ff7417102fb5fbd1cf8` |

The source files are the completed `esp32_sse_20260716_180514Z.ndjson`
capture and its `_retained.ndjson` sibling. Their window is
`2026-07-16T18:05:14.599Z` through `2026-07-17T06:05:14.373Z`. Pre/post size,
modification time, and hash checks matched. Candidate output was generated only
under restrictive `/tmp` storage and was not added to Git.

## Candidate replayed

The replay used the exact `conservative_combined_60s` definition from
`docs/ESP32_RETENTION_ASSESSMENT.md`: first observation, availability change,
exact text/binary change, entity-specific numeric deadband, and 60-second
heartbeat. Deadbands were 10 W for power/energy/power-ramp/drop, 0.1 for active
microinverters/current/voltage, 0.5 percentage point for curtailment, 0.04 Hz
for frequency/frequency-ramp, and 1 event for the event counter.

No new numeric alarm threshold was invented. Existing frequency-event text and
binary indicators are exact-change records and were preserved.

## Full-capture result

| Stream | Records | Raw records | Bytes | Raw bytes |
|---|---:|---:|---:|---:|
| Raw | 431,513 | 100.000% | 156,174,965 | 100.000% |
| Current retained | 394,327 | 91.382% | 149,568,755 | 95.770% |
| Conservative candidate | 61,724 | 14.304% | 36,174,692 | 23.163% |

The candidate retained 55,791 changes, 5,916 heartbeats, and all 17 first
observations. It had zero malformed records, zero backward timestamps, all 17
approved entities, no unapproved entity, and canonical UTC timestamps. Its last
record was 1.030 seconds before the raw capture end because no later observation
qualified; this does not change the documented capture coverage.

| Entity family | Raw | Current | Candidate | Candidate/raw |
|---|---:|---:|---:|---:|
| High/low/drop/rise binary events | 67 | 67 | 67 | 100.00% |
| Active microinverters | 43,144 | 43,144 | 1,790 | 4.15% |
| Curtailment | 43,144 | 43,144 | 3,013 | 6.98% |
| Voltage | 43,144 | 43,144 | 4,537 | 10.52% |
| Energy | 4,317 | 4,317 | 1,400 | 32.43% |
| AC-coupled power | 43,144 | 43,144 | 4,878 | 11.31% |
| Generator frequency | 43,144 | 5,958 | 5,467 | 12.67% |
| Current | 43,144 | 43,144 | 3,247 | 7.53% |
| Frequency ramp | 43,144 | 43,144 | 6,708 | 15.55% |
| Largest drop | 8,630 | 8,630 | 719 | 8.33% |
| Power ramp | 43,144 | 43,144 | 4,557 | 10.56% |
| Total events | 8,630 | 8,630 | 7,231 | 83.79% |
| Current status | 43,144 | 43,144 | 10,879 | 25.22% |
| Forensic event log | 21,573 | 21,573 | 7,231 | 33.52% |

The maximum generator-frequency gap was 1.208 seconds raw, 31.030 seconds in
current retained evidence, and 60.988 seconds in the candidate, consistent with
their heartbeat policies. Sparse binary entities naturally have longer gaps;
their transitions, not artificial periodic samples, are authoritative.

## Event and control preservation

| Window (UTC) | Raw | Current retained | Candidate |
|---|---|---|---|
| Event 1, `18:27:19`-`18:53:26` | partial collapse, high | partial collapse, high | partial collapse, high |
| Event 2, `20:55:58`-`21:18:03` | zero output, high | zero output, high | zero output, high |
| Event 3, `21:16:03`-`21:30:07` | zero output, high | zero output, high | zero output, high |
| Control, `18:52:26`-`19:04:30` | no event | no event | no event |

All streams preserved the frequency ranges (59.8-60.0 Hz for Event 1;
59.9-60.1 Hz for Events 2 and 3), nearest-anchor context within 0.443 seconds,
and event ordering. Across the full capture, raw, current-retained, and
candidate streams produced the same 17,687 binary/text changes with identical
timestamps, values, and order. No availability transition occurred in this
capture, so synthetic tests remain the validation for that required policy
path.

Window-local change counts can differ by one when the first sample retained in
a bounded window differs between streams. Full-capture comparison confirmed
that this is boundary seeding, not a lost transition. Analysis must retain
pre-window context when exact within-window transition counts matter.

## Acceptance criteria and limitations

All ten acceptance criteria passed: classifications and control were stable;
meaningful state and frequency events were preserved; no causation was added;
UTC/source/entity/provenance remained intact; routine loss did not weaken the
conclusions; reduction was material; replay is deterministic and tested; and
cloud cover remains an explicit competing explanation.

This single 12-hour capture has no real availability transition and cannot
validate every future operating state. EG4 cadence still limits exact transition
timing. The candidate does not create a new numeric threshold-crossing override;
implementation must preserve the existing exact-change binary/event indicators
and keep complete raw evidence. These are qualifications, not failures of the
tested candidate.

## Next implementation step

The production plan is now authoritative in
`docs/ESP32_RETENTION_PRODUCTION_PLAN.md`. The next work unit implements the
versioned policy and opt-in dual-output canary mode with synthetic tests only.
Live activation and capture verification remain separately approved milestones;
do not deploy from this replay report.
