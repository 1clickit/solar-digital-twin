# Coordinated Capture Three-Source Correlation

## Result

The bounded analysis found seven EG4 AC-couple production-collapse candidates:
five zero-output observations and two partial collapses. Six occurred from
12:02 through 16:15 CDT. The ESP32 independently observed the same
electrical output changes at one-second resolution: estimated power and active-
microinverter count fell with EG4 AC-couple power and later recovered. No
availability transition occurred.

The evidence supports real aggregate AC-couple output transitions as observed by
two transports: the EG4 cloud-derived series and the local ESP32 forensic
probe. It does **not** prove why they occurred. Abrupt steps and low-output
plateaus are less cloud-like than the gradual control window, but cloud-driven
irradiance change remains viable because there is no independent irradiance
sensor or machine-readable weather series in this capture. Inverter/control
behavior or microinverter dropout remains plausible but unresolved. No fault,
warning, battery limit, voltage excursion, or availability loss provides a
unique causal explanation.

This analysis does not change retention policy. `esp32-frequency-v1` remains
production and `esp32-conservative-v1` remains canary-only.

## Inputs, identity, and method

Capture `solar-forensic-20260718T062127Z` is immutable at
`/var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z`.
The six explicit machine inputs were verified against
`capture_inventories/solar-forensic-20260718T062127Z-inventory.tsv` before and
after analysis. Their sizes, nanosecond mtimes, and SHA-256 identities were
unchanged. SQLite was opened with URI `mode=ro&immutable=1` plus
`PRAGMA query_only = ON`; NDJSON was streamed read-only. Derived output was
written outside the evidence directory.

The runner normalizes the EG4 day series from America/Chicago to UTC, treats
EG4 runtime `server_time` as UTC, and uses canonical `solardt` UTC receipt time
for SolarAssistant and ESP32. It detects candidates only from EG4 day samples,
then reads bounded high-rate windows around those candidates. No interpolation
is used. The EG4 event timestamp is the exact timestamp of the first qualifying
low sample, not a claim that the physical transition began at that exact
second. EG4's approximately four-minute day-series cadence limits onset and
plateau timing.

Primary thresholds found seven candidates; the strict configuration retained
the five largest zero-output events and the loose configuration found eight,
adding a second event at 14:38:59 CDT within the long 14:26 event window. Three
deterministic controls cover stable strong production, gradual daytime
variation, and nighttime near-zero output.

Analysis code was based on repository checkpoint
`54d9608f334c537b482047d628c0e77e8934d843`. Exact verified identities were:

| Input | Bytes | mtime_ns | SHA-256 |
|---|---:|---:|---|
| `eg4/eg4_capture.sqlite` | 647168 | 1784431424329281543 | `153070c4a8488d9b3c8719be68f2aedbf065ab25b84df7adafb71d3692975fb8` |
| ESP32 raw | 275220446 | 1784432180722722866 | `a3e720b1027ecf2927f1d98cf6cc113faebfc560cea5e7a6dadbd3b40d90122b` |
| ESP32 `esp32-frequency-v1` | 266259706 | 1784432180722722866 | `9e288bd184154cc6aa90823a5a6075260250fac03e89d3a43ee4b76149e8be5c` |
| ESP32 `esp32-conservative-v1` | 63972840 | 1784432174673015267 | `c81a3841291f91c6f32436bc05a88d3155debfb249c7776795c8ae650a9e8aa7` |
| SolarAssistant raw | 70969608 | 1784432171335176595 | `e4c1b1bbb3e288f139dc3bb9979f17adf59493851e347b588b950176f3d76e4e` |
| SolarAssistant retained | 1556735 | 1784432171334176643 | `aa6e87f22d9d79b2ad9bf29d3367552ac399e956bd2c26acc8d18ec9ffaf2048` |

All six rows matched before and after every final analysis pass.

The authoritative primary `CorrelationConfig` was: minimum baseline 1,000 W;
absolute drop 500 W; fractional drop 40%; two required plateau samples;
recovery 80%; zero-output threshold 100 W; search window 900 seconds; maximum
runtime/day gaps 600/420 seconds; and SolarAssistant/ESP32/runtime/day alignment
tolerances 15/2/600/420 seconds. The predeclared strict set changed only
baseline/drop/fraction/recovery to 1,500 W/750 W/45%/85%; the loose set changed
them to 750 W/350 W/25%/75%. No threshold was tuned after observing results.

The reproducible derived products are:

- `docs/capture_analyses/solar-forensic-20260718T062127Z-events.tsv` — compact
  event/control table;
- `docs/capture_analyses/solar-forensic-20260718T062127Z-events.svg` — compact
  visual overview suitable for a browser screenshot;
- this narrative report.

The richer deterministic JSON was written only to
`/tmp/solar-forensic-20260718T062127Z-correlation.json`. Exact generation
command (wrapped only for readability):

    .venv/bin/python scripts/analyze_coordinated_capture.py \
      --evidence-root /var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z \
      --inventory docs/capture_inventories/solar-forensic-20260718T062127Z-inventory.tsv \
      --eg4 /var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z/eg4/eg4_capture.sqlite \
      --esp32-raw /var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z/esp32/esp32_sse_20260718_062127Z.ndjson \
      --esp32-current /var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z/esp32/esp32_sse_20260718_062127Z_retained.ndjson \
      --esp32-conservative /var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z/esp32/esp32_sse_20260718_062127Z_retained_esp32-conservative-v1.ndjson \
      --solarassistant-raw /var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z/solarassistant/solarassistant_20260718_062127Z.ndjson \
      --solarassistant-retained /var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z/solarassistant/solarassistant_20260718_062127Z_retained.ndjson \
      --start-utc 2026-07-18T06:21:28.435Z \
      --end-utc 2026-07-19T03:20:55.000Z \
      --analysis-commit worktree-based-on-54d9608f334c537b482047d628c0e77e8934d843 \
      --json-output /tmp/solar-forensic-20260718T062127Z-correlation.json \
      --tsv-output docs/capture_analyses/solar-forensic-20260718T062127Z-events.tsv \
      --svg-output docs/capture_analyses/solar-forensic-20260718T062127Z-events.svg

### Screenshot explanation

The SVG overview is a compact visual aid, not a separate measurement. Each
event row plots three EG4 observations from left to right by power: green is
the pre-event baseline, red is the plateau nadir, and blue is the qualifying
recovery. The connecting line shows the baseline-to-nadir-to-recovery sequence;
it does not interpolate the physical path or exact transition time between the
roughly four-minute EG4 samples. The three gray control rows identify comparison
windows where the detector found no candidate. The chart deliberately omits
high-rate ESP32 and battery traces; those corroborating details and limitations
remain in the table and narrative below. A screenshot of this SVG therefore
supports quick comparison of event magnitude and recovery only, and must not be
read as evidence of cause or per-microinverter behavior.

### Battery-cell review addendum

The follow-up read-only SolarAssistant review is preserved at
`docs/capture_analyses/solar-forensic-20260718T062127Z-battery-cell-review.md`.
At event anchors, Battery 1 cell spread was 2–10 mV and Battery 2 was 1–8 mV;
capture-wide maxima were 24 mV and 19 mV respectively. Highest reported cell
voltages were 3.501 V for Battery 1 and 3.494 V for Battery 2. There is no
positive evidence of JK cell-overvoltage protection.

SolarAssistant did not export charge/discharge MOS, balancing,
alarm/protection, individual-cell, or charge-limit topics, so an unobserved
transient cannot be absolutely excluded. Within that limitation, existing
telemetry does not support JK BMS protection as the cause of any event and
cannot support it as a common explanation for all seven. The
`total/battery_voltage` value near 55.8 V is the representative parallel-bank
voltage, not a summed voltage.

## Event results

Times below are observed EG4 samples in CDT on July 18, 2026. “Drop” is the
initial qualifying reduction. For partial events the later plateau nadir is
also shown. Battery values are trusted combined JK BMS values within 30 seconds
of the event sample; positive power/current means charging and negative means
discharging in the captured SolarAssistant data.

| ID | Time CDT | EG4 baseline → nadir → recovery | Initial drop | EG4 load before → nadir → recovery | ESP32 near event | Trusted battery near event | Result |
|---|---:|---:|---:|---:|---|---|---|
| 01 | 14:26:55 | 4,018 → 0 → 3,640 W | 4,018 W (100%) | 1,105 → 1,244 → 1,118 W | 4,091 → 2 W; 5.70 → 0.003 active; 59.9–60.0 Hz; 239.4–240.8 V | 99% SOC; 55.0–55.8 V; +2,708 to −1,366 W | EG4 and ESP32 agree on abrupt full collapse; battery changed from charging to discharging; recovery sample at 15:07:05 |
| 02 | 12:26:26 | 3,857 → 0 → 3,309 W | 3,857 W (100%) | 850 → 1,306 → 812 W | already 1.6–2.4 W and ~0.003 active; 59.9–60.0 Hz; 240.6–240.8 V | 88% SOC; 53.3 V; −1,509 to −1,386 W | Both sources record sustained zero output; battery supplied load; recovery sample at 12:42:32 |
| 03 | 15:15:07 | 3,696 → 0 → 3,293 W | 3,696 W (100%) | 1,305 → 932 → 1,257 W | 3,830 → 2 W; 5.34 → 0.003 active; 59.9–60.1 Hz; 238.8–241.0 V | 99% SOC; 55.2–55.8 V; +2,732 to −1,034 W | Abrupt full collapse in both sources; charging changed to discharging; recovery sample at 15:23:09 |
| 04 | 15:35:14 | 3,103 → 0 → 3,206 W | 3,103 W (100%) | 1,102 → 1,123 → 1,087 W | 0–137 W and 0–0.192 active; 59.9–60.0 Hz; 240.6–240.8 V | 99% SOC; 54.7–54.8 V; −1,253 to −1,103 W | Full collapse followed by a roughly 533–603 W reduced plateau before recovery at 15:59:19 |
| 05 | 16:15:23 | 3,074 → 0 → 2,624 W | 3,074 W (100%) | 1,522 → 1,535 → 1,362 W | ~2 W and ~0.003 active; 59.9–60.0 Hz; 240.8 V | 99% SOC; 54.5–54.7 V; −1,719 to −1,609 W | Both sources record sustained zero output; battery supplied load; staged recovery began before the 16:39:30 recovery sample |
| 06 | 12:02:19 | 3,870 → 676 → 3,283 W | 2,735 W (70.7%); total baseline-to-nadir 3,194 W | 931 → 628 → 571 W | 810–2,486 W; 1.13–3.47 active; 59.9–60.0 Hz; 240.6–241.0 V | 86% SOC; 53.5 V; −270 to +1,274 W | Partial collapse and step recovery in both sources; no battery constraint is demonstrated |
| 07 | 08:41:29 | 1,100 → 575 → 967 W | 510 W (46.4%); total baseline-to-nadir 525 W | 552 → 556 → 592 W | 566–689 W; 0.79–0.96 active; 59.9–60.0 Hz; 240.6–240.8 V | 69% SOC; 53.2 V; −62 to −1 W | Smaller morning partial collapse |

The plateau/recovery durations were 40:10, 16:06, 8:02, 24:05, 24:07,
8:03, and 8:03 respectively for events 01 through 07. Event 01 includes
multiple zero/rebound samples within one long detector window, so it represents
a compound unstable interval rather than one uninterrupted flat zero.

## Cross-source findings

### EG4

All seven candidates are changes in EG4 `ac_couple_power_w`. The captured EG4
`solar_pv_w` field is zero throughout these records and was not used as the
production measure. Available runtime snapshots report operating state
`normal`, warning `0`, and fault `0`; runtime context is missing or sparse for
some events because its cadence is approximately 15 minutes. Absence of a
nearby fault or warning is therefore not proof that no short condition
occurred.

Load did not collapse in step with production. Instead, the battery moved from
charging toward discharge or remained discharging while supplying loads of
roughly 0.6–1.5 kW. This is consistent with the energy balance expected when
AC-coupled input disappears and is inconsistent with load disappearance being
the cause of the observed production drops.

### ESP32

ESP32 estimated power and active-microinverter estimates agree closely with the
EG4 reductions and recoveries. Active count approaches zero during every full
collapse. Estimated curtailment correspondingly approaches 100%; that field is
a calculation from measured current and configured capacity, not independent
proof of an inverter curtailment command. There were zero availability
transitions in every event and control window.

Frequency remained within 59.8–60.1 Hz across event windows and voltage within
238.8–243.4 V. The forensic log contains frequent `FREQ_DROP`/`FREQ_RISE`
tokens associated with 0.1 Hz quantization and some power tokens, but it shows
no unique frequency, voltage, or availability signature that explains the
collapses. These tokens support timestamped observation, not causation.

Raw, `esp32-frequency-v1`, and canary-only `esp32-conservative-v1` retained the
same seven event classifications and the critical power, active-count,
frequency, and voltage context in every event window. This supports retention
fidelity for the observed event classes but does not authorize retirement of
the production policy or promotion of the canary.

### SolarAssistant / JK BMS

Trusted BMS telemetry shows the battery responding to lost production, not a
common battery limit that precedes all events. SOC spans 69–99% across the day;
the large events occur at 86–99%. Events 01 and 03 change from charging to
discharging as production falls. Events 02, 04, 05, and 07 are discharging
near the event, while event 06 crosses low discharge into charging. Voltage
remains 53.2–55.8 V in the event neighborhoods. No shared SOC, voltage,
current, or charging-state threshold explains all seven events.

SolarAssistant raw evidence contains trusted battery topics only for this
analysis. It does not provide a machine-readable Solar PV or load series, so it
cannot provide a third independent production measurement.

## Gaps, reconnects, controls, and limitations

No source gap or reconnect overlaps an event. Capture-wide integrity found no
ESP32 gap over two seconds and no SolarAssistant gap over 20 seconds. EG4 day
samples are much coarser, so the report gives observed sample times and does
not interpolate physical onset. The source-specific ESP32 manifest lacks a
terminal record; the common manifest records controlled SIGTERM, all streams
end cleanly, and this provenance qualification remains attached to the result.

The stable strong-production control at 14:10:51 CDT, gradual-variation control
at 10:46:00, and nighttime control at 01:23:36 produced no candidate event.
The stable control held about 4.03–4.04 kW ESP32 power, 59.9–60.0 Hz, and
240.8–241.0 V. The gradual control retained ordinary broad variation with
59.8–60.0 Hz and 240.0–241.6 V. The night control held about 3.4–3.6 W with
59.9–60.0 Hz and 240.6–241.0 V. The same rolling frequency tokens appeared in
controls, weakening their value as an event discriminator.

Across the ten disjoint event/control windows, raw/current/conservative streams
used 133630/124941/31312 records and 48166510/46631880/12498671 bytes. All three
preserved event identity, classification, confidence inputs, and critical
context. This is supporting canary acceptance evidence only; no policy changes.

Threshold sensitivity is strongest for the five full collapses. The two
partial events disappear under strict thresholds, while the loose threshold
splits a further zero sample from the compound event-01 interval. Conclusions
about event count therefore depend on segmentation, while the underlying power
transitions do not.

The analyzer labels all seven primary candidates `high` correlation confidence,
but that is not causal confidence. Controls show the frequency/event-text
features are non-discriminating. Principal unresolved limitations are the lack
of independent irradiance, sparse EG4 runtime/fault cadence, calculated
rather than directly enumerated microinverter count, and lack of per-
microinverter telemetry. Cloud, electrical/control behavior, aggregation and
timing, and actual microinverter dropout remain explicit alternatives.

## Conclusion and next gate

The capture is sufficient to establish repeated real aggregate AC-couple
production collapses and battery response without evidence loss. It is not
sufficient to assign cause. Chris should review these findings before choosing
between a targeted follow-up capture, independent irradiance measurement, or a
separately authorized one-shot local-dongle measurement. Home Assistant and
irradiance work were not prerequisites for this first analysis and no live
measurement is authorized by this report.

## Owner-review questions

1. Is confirmation of repeated aggregate loss/rejoin sufficient for the owner
   decision, given that cause remains unresolved?
2. If cause matters, which one independent discriminator would most reduce the
   ambiguity: synchronized irradiance, a narrowly targeted capture, or a
   separately gated local-dongle one-shot that exposes genuinely new state?
3. Does the expected decision value justify another measurement, or should the
   project stop with the qualified correlation result?

Correlation does not establish causation.
