# ESP32 Full-Capture Retention Assessment

## Decision and scope

The completed 12-hour capture was assessed offline with the streaming utility
`scripts/analyze_esp32_retention.py`. Raw evidence remained authoritative and
both input files remained unchanged. The implemented policy behaved as
documented; no collector defect was found.

Keep the production retention policy unchanged for now. A conservative
candidate could reduce derived retained volume substantially, but its proposed
entity deadbands must first be replayed against known forensic windows and
reviewed with later cross-source correlation evidence. Storage reduction does
not justify weakening forensic evidence.

## Evidence and totals

- raw: 431,513 records and 156,174,965 bytes;
- retained: 394,327 records and 149,568,755 bytes;
- retained/raw: 91.382% by record and 95.770% by byte;
- coverage: `2026-07-16T18:05:14.599Z` through
  `2026-07-17T06:05:14.373Z`.

The analyzer reproduced the retained count and byte size exactly from current
policy semantics. It reads line by line, keeps bounded per-entity samples, and
does not write evidence.

## Entity contribution

All non-frequency entities are intentionally pass-through and therefore retain
100%. Generator frequency is the only selective entity.

| Entity | Raw | Retained | Retained % | Repeats | Retained bytes |
|---|---:|---:|---:|---:|---:|
| Forensic event log | 21,573 | 21,573 | 100.00 | 14,342 | 72,873,622 |
| Current status | 43,144 | 43,144 | 100.00 | 32,749 | 14,764,536 |
| AC-coupled power | 43,144 | 43,144 | 100.00 | 32,834 | 8,426,495 |
| Active microinverters | 43,144 | 43,144 | 100.00 | 34,625 | 8,409,674 |
| Curtailment percent | 43,144 | 43,144 | 100.00 | 34,604 | 8,363,464 |
| GEN L1-L2 voltage | 43,144 | 43,144 | 100.00 | 39,120 | 8,273,296 |
| Frequency ramp rate | 43,144 | 43,144 | 100.00 | 36,917 | 7,935,111 |
| GEN L1 current | 43,144 | 43,144 | 100.00 | 32,500 | 7,695,990 |
| Generator frequency | 43,144 | 5,958 | 13.81 | 38,161 | 1,055,552 |
| Power ramp rate | 43,144 | 43,144 | 100.00 | 32,732 | 7,567,797 |
| Largest power drop | 8,630 | 8,630 | 100.00 | 8,629 | 1,700,145 |
| Total events | 8,630 | 8,630 | 100.00 | 1,399 | 1,613,839 |
| AC-coupled energy | 4,317 | 4,317 | 100.00 | 3,043 | 876,389 |
| Four binary event entities combined | 67 | 67 | 100.00 | 0 | 12,845 |

The event log is the largest byte contributor because its text payload is much
larger than ordinary telemetry and every observation currently passes through.
This is expected, not evidence of malformed output. Repeated values are retained
unnecessarily for storage efficiency, but intentionally under the current
forensic-first pass-through policy.

## Frequency-policy verification

Frequency produced 43,144 raw observations, five unique displayed values, and
5,958 retained observations:

- first observation: 1;
- changes of at least 0.04 Hz from the last retained value: 4,982;
- 30-second heartbeats: 975.

Of 43,143 consecutive deltas, 38,161 were below 0.04 Hz and 4,982 were above;
none equaled the boundary. The observed range was 58.5-60.1 Hz. Median absolute
delta was 0 Hz and the 90th and 99th percentiles were 0.1 Hz. The reconstructed
aggregate count and byte size matched the actual retained file exactly.
Together with the prior record-order integrity check, this confirms that the
0.04 Hz deadband and heartbeat operated as designed and preserved abrupt
frequency movement.

No availability transitions occurred in this capture. Numeric types and
formatting did not trigger selective retention, attributes are not compared by
the implemented frequency policy, and canonical receipt timestamps only drive
heartbeats. Binary event transitions, changing status/event text, reduced-output
plateaus, and abrupt power/frequency changes remain available for later
correlation.

## Numeric observations

Routine exact repeats dominate most one-second entities. Selected absolute
delta results support evaluation, not approved thresholds:

| Entity | Range | Delta p50 | Delta p90 | Delta p99 |
|---|---:|---:|---:|---:|
| AC-coupled power | 0-4,649.8 W | 0 | 7.8 | 193.4 |
| GEN L1 current | 0.963-19.368 A | 0 | 0.042 | 0.798 |
| GEN L1-L2 voltage | 238.8-242.6 V | 0 | 0 | 0.2 |
| Power ramp rate | -3,252.8-1,257.4 | 0 | 8.200 | 202.8 |
| Frequency ramp rate | -1.5-0.199997 | 0 | 0.099998 | 0.199996 |

These measurements show that high retention is mostly pass-through policy plus
legitimately changing forensic data, not a comparison defect. They also show
large duplicate-reduction potential without requiring aggressive compression.

## Offline candidate comparison

Candidate estimates preserve first observations, availability transitions,
text and binary state changes, and periodic heartbeats. The entity-deadband
examples are assessment values only, not approved policy.

No additional numeric forensic threshold is currently approved. The candidates
therefore preserve existing binary threshold indicators and large changes, but
cannot prove preservation of an undefined future numeric crossing. Any later
implementation must add an explicit threshold-crossing override and test it
before a deadband can suppress the associated metric.

| Candidate | Records | Raw records % | Bytes | Raw bytes % | Principal risk |
|---|---:|---:|---:|---:|---|
| Current policy | 394,327 | 91.382 | 149,568,755 | 95.770 | High derived volume; strongest continuity |
| Entity deadbands, 30 s heartbeat | 67,862 | 15.727 | 37,433,261 | 23.969 | Small numeric movement may be hidden |
| Exact changes, 120 s heartbeat | 92,650 | 21.471 | 41,954,261 | 26.864 | Longer stable-data gaps; large text remains on change |
| Conservative combined, 60 s heartbeat | 61,724 | 14.304 | 36,174,692 | 23.163 | Candidate deadbands need event-window validation |

The conservative combined estimate retains 55,791 changes, 5,916 heartbeats,
and all 17 first observations. It would reduce the present retained file by
about 75.8% while leaving raw evidence untouched. Its power and ramp thresholds
remain well below the large transitions relevant to partial-collapse analysis,
but that inference is not enough to approve deployment. Known dropout,
recovery, plateau, binary-event, and availability scenarios must be replayed
before any implementation.

## Recommendation and following work

No policy or collector change is approved. Keep complete raw evidence and the
current retained policy until the candidate is validated against event windows.
The next bounded task is to establish matching EG4 evidence availability and
prepare the offline EG4/SolarAssistant/ESP32 correlation plan. That correlation
work should also identify representative ESP32 windows for later conservative
retention-policy replay. Any implementation remains a separate reviewed task.
