# SolarAssistant Deadband Assessment

## 1. Purpose and approval status

This assessment characterizes the existing local raw SolarAssistant NDJSON evidence for the topic families that do not yet enter the retained stream.

**Candidate only — pending project-owner approval.** No deadband is approved, implemented, or activated by this report. The available evidence is too narrow to support a defensible numeric candidate for any assessed family, so each remains raw-only.

## 2. Evidence analyzed

The collector defines raw files as `evidence/solarassistant/solarassistant_<UTC timestamp>.ndjson`. Retained files use a distinct `_retained.ndjson` suffix and were excluded.

- Raw files: 2
- Valid raw records: 294
- Invalid or unparseable records: 0
- Receipt-time coverage: 2026-07-14 05:08:44.354 UTC through 05:12:31.574 UTC
- Wall-clock span: about 3 minutes 47 seconds
- Active capture time: about 7.4 seconds across two short runs
- Topics: all 42 approved topics, with 7 samples per topic
- Assessed samples: voltage 21; current 21; power 21; cell voltage 63; cell imbalance 21; temperature 63
- Device scopes: combined `total`, Battery 1, and Battery 2

The first file contains four polls over about 4.4 seconds. The second contains three polls over about 2.9 seconds. The runs are separated by about 3 minutes 40 seconds, consistent with a collector stop or restart rather than continuous sampling. Within-run polling intervals were approximately 1.47 seconds; no material within-run gaps were found.

All current and power samples have the same negative sign and are materially away from zero. Subject to the device's sign convention, this is consistent with one narrow discharge-like condition. The evidence does not demonstrate charging, idle or near-zero behavior, broad load transitions, or meaningful temperature evolution.

## 3. Method

Metrics were analyzed independently by stable topic identity, preserving combined, Battery 1, Battery 2, average, highest, lowest, probe, general, and MOS distinctions.

Consecutive changes were calculated only within each file and within continuous runs. A conservative five-second gap threshold was chosen from the observed approximately 1.47-second cadence. File boundaries were always segmented, so the long interval between files was not treated as ordinary variation.

For each identity, the analysis considered sample and distinct-value counts, unchanged percentage, range, smallest positive observed increment, common nonzero changes, absolute consecutive-change percentiles and maximum, and repeated-value runs. Observed increments are not automatically treated as source resolution, and source resolution is not automatically treated as a meaningful-change deadband.

## 4. Evidence limitations

Seven observations per identity and about 7.4 seconds of active capture cannot distinguish display quantization, ordinary jitter, and diagnostically meaningful movement reliably. Repeated runs lasted at most about 4.4 seconds. There is no demonstrated charging period, idle or near-zero current/power period, sustained high-load transition, wide battery operating range, several-hour temperature trend, or cell behavior near full charge.

The collector can safely continue preserving these families in complete raw evidence while excluding them from retained output.

## 5. Candidate-policy summary

| Family or metric scope | Observable resolution or step | Representative short-term variation | Candidate deadband | Heartbeat | Confidence | Status |
|---|---:|---:|---:|---:|---|---|
| Voltage: total, Battery 1, Battery 2 | displayed to 0.1 V; only Battery 1 changed by 0.1 V | mostly flat | None proposed | 60 s | Insufficient | Insufficient evidence |
| Current: total and individual batteries | displayed to 0.1 A; observed nonzero steps varied by scope | 0.3-1.1 A changes in this narrow run | None proposed | 60 s | Insufficient | Insufficient evidence |
| Power: total and individual batteries | integer W; observed steps were 20-62 W | mostly flat with a few 21-62 W changes | None proposed | 60 s | Insufficient | Insufficient evidence |
| Cell voltage: average, highest, lowest by scope | displayed to 0.001 V; observed steps 0.001-0.002 V | flat or one/two displayed increments | None proposed | 300 s | Insufficient | Insufficient evidence |
| Cell imbalance: total average, Battery 1, Battery 2 | 0.001 V shown; observed steps 0.001-0.003 V | several small changes in one condition | None proposed | 300 s | Insufficient | Insufficient evidence |
| Temperature: general, probes 1/2, MOS by scope | displayed to 0.1 degrees C | mostly flat; a few 0.1-degree changes | None proposed | 300 s | Insufficient | Insufficient evidence |

Any future numeric proposal must be labeled **Candidate only — pending project-owner approval** until Chris explicitly approves it.

## 6. Voltage findings

Combined voltage remained at 52.3 V and Battery 2 at 52.2 V. Battery 1 ranged from 52.3 to 52.4 V. The source displays tenths of a volt, but one changing identity is not enough to determine whether 0.1 V reflects routine movement, quantization, or a useful event signal.

No common or scope-specific deadband is defensible yet. Minimum additional evidence is a continuous run covering sustained charging, sustained discharging, idle behavior, and load or charger transitions for all three scopes. The 60-second heartbeat remains planned.

## 7. Current findings

Combined current ranged from -22.5 to -21.0 A, Battery 1 from -11.9 to -10.8 A, and Battery 2 from -11.0 to -10.2 A. The source displays tenths of an ampere. Within-run nonzero changes ranged from 0.3 to 1.1 A, but no near-zero values, sign changes, or charging values were observed.

Combined and individual behavior cannot yet be judged equivalent. Minimum additional evidence must include near-zero/idle behavior, both current directions if supported by the sign convention, stable charge and discharge periods, and transitions. The 60-second heartbeat remains planned.

## 8. Power findings

Combined power ranged from -1157 to -1095 W, Battery 1 from -604 to -563 W, and Battery 2 from -573 to -532 W. Values are reported as integer watts; observed consecutive changes were sparse and ranged from 21 to 62 W. This does not establish whether the true display resolution is 1 W or whether power is derived from rounded voltage and current.

No common or scope-specific deadband is defensible. Minimum additional evidence should cover near-zero power, stable and changing loads, charging and discharging if applicable, and wider transitions. The 60-second heartbeat remains planned.

## 9. Cell-voltage findings

Average, highest, and lowest values were kept distinct for every scope. Values are displayed to 0.001 V. Some identities were flat; others changed by 0.001 or 0.002 V. The short sample cannot determine whether one displayed increment is normal BMS quantization, useful cell movement, or both.

No common threshold across average, highest, and lowest measurements is justified. Minimum additional evidence should cover longer charge and discharge periods, load transitions, and behavior near full charge. The 300-second heartbeat remains planned.

## 10. Cell-imbalance findings

All imbalance topics use volts. Combined average ranged from 0.003 to 0.004 V, Battery 1 from 0.001 to 0.004 V, and Battery 2 from 0.003 to 0.005 V. Observed changes ranged from 0.001 to 0.003 V. Battery 1 changed more frequently than the other scopes during the brief sample.

This potentially diagnostic metric needs longer coverage before suppressing even the smallest displayed changes. Minimum additional evidence should include stable periods, load transitions, charge/discharge conditions, and behavior near full charge. The 300-second heartbeat remains planned.

## 11. Temperature findings

General temperature, temperature sensors 1 and 2, and MOS temperature were kept separate. Values are displayed to 0.1 degrees C. Most identities were flat; only a few probe readings changed by 0.1 degree. The capture is far too short to characterize slow thermal movement or determine whether MOS temperature needs a different policy.

Minimum additional evidence is several continuous hours spanning measurable thermal and operating changes. General, probe, and MOS measurements should remain separate until that evidence supports a common threshold. The 300-second heartbeat remains planned.

## 12. Recommended next decision

Do not approve or implement numeric deadbands from this evidence. Continue these families as raw-only and collect a longer, explicitly authorized raw evidence window later that covers the missing operating conditions. Reassess at the same stable metric-identity level before deciding whether combined and individual batteries, or individual submetrics, can share thresholds.

The dedicated unprivileged runtime, protected credential boundary, metadata
verification, and one short authenticated collector verification are now
complete. That 25-second run created 126 raw records and a separate retained
file and confirmed the expected combined and per-battery topics, but remains a
point-in-time verification rather than evidence for numeric thresholds.

The later 86,400-second capture completed normally and passed its completion
review with qualifications. It provides substantially broader raw coverage of
the missing operating conditions than the short evidence assessed here. A new,
separately reviewed deadband assessment may use that capture only after an
approved evidence-access and analysis plan. The collector is no longer
running, and no numeric deadband or retention change is approved by the capture
result or this document.

## 13. Explicit exclusions

This assessment did not use retained output, contact a device, authenticate, inspect credentials, change evidence, implement retention policy, or approve a threshold. The findings are SolarAssistant-specific. Shared retention mechanics remain source-independent for future collectors and sensors.
