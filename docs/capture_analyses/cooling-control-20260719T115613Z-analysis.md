# Cooling-control capture analysis

## Repository preservation note

The immutable, intentionally Git-ignored capture remains at
`evidence/cooling_control/cooling-control-20260719T115613Z/`:

- `raw_telemetry.ndjson`: 20,227,369 bytes; SHA-256
  `4c411fbd9e258ffc217da2d52f3690662c4c97f1a73281b00f71174ff687cf0f`;
  7,200 valid records.
- `capture_manifest.ndjson`: 3,066 bytes; SHA-256
  `96ed69112d9cfe8e78524557fedbe6afdf2e594f1386ee3b066cae44beac02f0`;
  two valid records with terminal reason `duration_complete`, 7,200 successful
  requests, and zero errors.

Both identities were unchanged by the read-only analysis and again matched
when this report was preserved. The analysis body below is copied faithfully
from the validated temporary report; this preservation note is the only
tracked-report addition.

## Scope and conclusion

This is a bounded, read-only offline analysis of `/home/chris/solar-digital-twin/evidence/cooling_control/cooling-control-20260719T115613Z`. The evidence files were not changed. The capture contains 7,200 valid one-second Home Assistant snapshots and 2 valid manifest records. The terminal record reports `duration_complete`, with 7,200/7,200 requests successful and 0 errors.

Using changes in each entity’s `source_last_updated`, Radiator 1 had 52 distinct source timestamps and Radiator 2 had 32. Eight Radiator 1 temperature-cycle episodes at 71–72 °C were observed under both the 5-minute and 10-minute grouping rules. The first is left-censored: its 71 °C source timestamp precedes capture receipt start by 52.703 seconds. Every episode was followed by a much lower next reported source value, but the roughly two-minute radiator source cadence cannot locate the physical onset, duration, or mechanism of cooling and cannot resolve a reported sub-15-second phenomenon.

No fan telemetry exists in this capture. No temperature change is characterized as fan operation. Findings below describe temperature-cycle episodes and reported cooling intervals only; associations do not establish causation.

## Provenance and limitations

Current provenance is **Home Assistant → EG4 Web Monitor hybrid mode**. Local-dongle versus cloud lineage has not yet been proven per entity. Home Assistant is therefore a presentation/source timestamp layer, not proof of independent local-device measurement for any entity.

- Fan command, state, RPM, PWM, speed, and duty were unavailable. Radiator temperature must not be used as a fan-state proxy.
- The capture polled Home Assistant approximately once per second, but source values repeated until the integration supplied a new `source_last_updated` value.
- Radiator source updates were slow enough that endpoint slopes are coarse interval averages. Actual threshold crossings could occur anywhere between adjacent source updates.
- A constant state with an unchanged source timestamp means “no newly reported source update,” not proof that the underlying physical quantity was perfectly constant.
- All times are UTC. “Contemporaneous” means the latest state visible to the capture at the episode receipt time; fields can have different and sometimes very old source timestamps.

## Evidence and schema validation

| Item | Result |
|---|---|
| Raw record count | 7,200 valid NDJSON records |
| Manifest record count | 2 valid NDJSON records (`capture_start`, `capture_terminal`) |
| Receipt window | `2026-07-19T11:56:13.358+00:00` through `2026-07-19T13:56:12.357+00:00` |
| Terminal status | `duration_complete`; elapsed 7200.000236 s; 7,200 successful; 0 errors; 7,200 complete responses |
| Raw SHA-256 | `4c411fbd9e258ffc217da2d52f3690662c4c97f1a73281b00f71174ff687cf0f` (before analysis; unchanged after validation) |
| Manifest SHA-256 | `96ed69112d9cfe8e78524557fedbe6afdf2e594f1386ee3b066cae44beac02f0` (before analysis; unchanged after validation) |

Every raw record used this top-level schema: `record_type`, `receipt_utc`, `monotonic_elapsed_seconds`, `source`, `request_latency_seconds`, and `values`. `values` is an object keyed by the 12 allowlisted logical entity names. Every observed entity object used: `entity_id`, `raw_state`, `unit`, `source_last_changed`, and `source_last_updated`. Numeric measurements were stored as strings in `raw_state`; this analysis parsed them as numbers only in memory. `receipt_utc` is collector receipt time. `monotonic_elapsed_seconds` is capture-process elapsed time. The two source timestamps are Home Assistant entity timestamps; `source_last_updated` is the primary deduplication key and `source_last_changed` is the documented fallback (the fallback was not needed).

| Logical key | Entity ID | Unit | Missing entity snapshots | Null raw states | Null units | Null source timestamps | Distinct source timestamps |
|---|---|---:|---:|---:|---:|---:|---:|
| `radiator1_c` | `sensor.sna12k_us_44830p0125_radiator_1_temperature` | °C | 0 | 0 | 0 | 0 | 52 |
| `radiator2_c` | `sensor.sna12k_us_44830p0125_radiator_2_temperature` | °C | 0 | 0 | 0 | 0 | 32 |
| `load_w` | `sensor.sna12k_us_44830p0125_eps_power` | W | 0 | 0 | 0 | 0 | 54 |
| `ac_couple_w` | `sensor.sna12k_us_44830p0125_ac_couple_power` | W | 0 | 0 | 0 | 0 | 24 |
| `pv_w` | `sensor.sna12k_us_44830p0125_pv_total_power` | W | 0 | 0 | 0 | 0 | 1 |
| `battery_w` | `sensor.sna12k_us_44830p0125_battery_power` | W | 0 | 0 | 0 | 0 | 56 |
| `battery_soc` | `sensor.sna12k_us_44830p0125_state_of_charge` | % | 0 | 0 | 0 | 0 | 1 |
| `battery_status` | `sensor.sna12k_us_44830p0125_battery_status` | null (categorical/unlabelled) | 0 | 0 | 7200 | 0 | 1 |
| `grid_w` | `sensor.sna12k_us_44830p0125_grid_power` | W | 0 | 0 | 0 | 0 | 1 |
| `operating_mode` | `select.sna12k_us_44830p0125_operating_mode` | null (categorical/unlabelled) | 0 | 0 | 7200 | 0 | 1 |
| `cloud_status` | `sensor.sna12k_us_44830p0125_status` | null (categorical/unlabelled) | 0 | 0 | 7200 | 0 | 1 |
| `status_code` | `sensor.sna12k_us_44830p0125_status_code` | null (categorical/unlabelled) | 0 | 0 | 7200 | 0 | 1 |

Null `unit` values for battery status, operating mode, inverter status, and status code reflect unlabeled/categorical source fields, not missing entity records. No entity object, `raw_state`, or `source_last_updated` was missing or null in any snapshot.

## Event-detection methodology

1. Parse every NDJSON line without modifying the input and require the observed stable schema.
2. For each logical entity independently, retain the first captured snapshot for each distinct `source_last_updated`. This prevents the one-second REST polling cadence from being miscounted as source updates. If `source_last_updated` were absent, use `source_last_changed`; no fallback was required here.
3. Define a Radiator 1 qualifying observation as a distinct source update with a numeric state ≥71 °C (there were no values above 72 °C). Group consecutive qualifying observations when their source timestamps are separated by no more than the grouping threshold.
4. Primary grouping threshold: 5 minutes, chosen to exceed the typical ~2-minute Radiator 1 source interval while remaining below observed recurrence times. Sensitivity threshold: 10 minutes. Both produce eight episodes with identical anchors, so episode count is not grouping-sensitive within this range.
5. Anchor each episode at its first qualifying source timestamp and first receipt. For threshold drops, search later distinct Radiator 1 source updates and report the first below each threshold. The elapsed interval is endpoint-to-endpoint source time, not exact crossing time.
6. For context, report the latest state visible at episode receipt plus summaries of distinct source updates received within ±5 minutes. A ±3-minute source-time trajectory is also shown for changing power channels. No interpolation is used.
7. Treat the initial 71 °C state as a left-censored observed episode because its source timestamp precedes the capture’s first receipt. Do not estimate its rise or earlier history.

### Grouping sensitivity

| Maximum gap joining qualifying observations | Episodes | Result |
|---:|---:|---|
| 300 s (5 min, primary) | 8 | 2026-07-19T11:55:20.655Z, 2026-07-19T12:07:26.708Z, 2026-07-19T12:19:33.683Z, 2026-07-19T12:45:43.022Z, 2026-07-19T12:57:48.702Z, 2026-07-19T13:13:57.809Z, 2026-07-19T13:28:04.709Z, 2026-07-19T13:40:10.664Z |
| 600 s (10 min) | 8 | 2026-07-19T11:55:20.655Z, 2026-07-19T12:07:26.708Z, 2026-07-19T12:19:33.683Z, 2026-07-19T12:45:43.022Z, 2026-07-19T12:57:48.702Z, 2026-07-19T13:13:57.809Z, 2026-07-19T13:28:04.709Z, 2026-07-19T13:40:10.664Z |

## Temperature summary and source cadence

| Metric | Radiator 1 | Radiator 2 |
|---|---:|---:|
| Minimum | 59 °C | 47 °C |
| Maximum | 72 °C | 51 °C |
| Median of 7,200 snapshots | 67 °C | 48 °C |
| Observed range | 13 °C | 4 °C |
| Median of distinct source-timestamp observations | 67.5 °C | 48.5 °C |
| Distinct source timestamps | 52 | 32 |
| First distinct source timestamp observed | 2026-07-19T11:55:20.655Z (first receipt 2026-07-19T11:56:13.358Z; source state predates capture) | 2026-07-19T11:55:20.655Z (first receipt 2026-07-19T11:56:13.358Z; source state predates capture) |
| Last distinct source timestamp observed | 2026-07-19T13:54:17.856Z (receipt 2026-07-19T13:54:18.357Z) | 2026-07-19T13:54:17.856Z (receipt 2026-07-19T13:54:18.357Z) |
| Source-update intervals | min 119.864 s; median 121.045 s; Q1–Q3 120.918–121.328 s; max 241.956 s | min 119.936 s; median 241.892 s; Q1–Q3 121.214–242.689 s; max 484.030 s |

The snapshot median is receipt-time weighted because repeated Home Assistant snapshots persist between source updates. The distinct-source median weights each observed source timestamp once. Neither should be interpreted as a calibrated thermal time average without proving upstream sampling behavior.

## Radiator 1 high-temperature episodes and reported cooling intervals

Recurrence intervals between episode anchors: 726.053 s (12.10 min), 726.975 s (12.12 min), 1569.339 s (26.16 min), 725.680 s (12.09 min), 969.107 s (16.15 min), 846.900 s (14.12 min), 725.955 s (12.10 min). Summary: min 12.09 min, median 12.12 min, max 26.16 min.

| Ep. | High source time | First receipt | Peak | Next reported value and elapsed | First reported <71 / <70 / <69 / <68 °C | Coarse endpoint cooling rate |
|---:|---|---|---:|---|---|---:|
| 1 | `2026-07-19T11:55:20.655Z`; left-censored | `2026-07-19T11:56:13.358Z` | 71 °C | 63 °C at 2026-07-19T11:57:21.494Z; 120.839 s | <71: 63 °C at 2026-07-19T11:57:21.494Z (120.839 s); <70: 63 °C at 2026-07-19T11:57:21.494Z (120.839 s); <69: 63 °C at 2026-07-19T11:57:21.494Z (120.839 s); <68: 63 °C at 2026-07-19T11:57:21.494Z (120.839 s) | -3.97 °C/min over endpoints |
| 2 | `2026-07-19T12:07:26.708Z` | `2026-07-19T12:07:27.357Z` | 71 °C | 60 °C at 2026-07-19T12:09:27.769Z; 121.061 s | <71: 60 °C at 2026-07-19T12:09:27.769Z (121.061 s); <70: 60 °C at 2026-07-19T12:09:27.769Z (121.061 s); <69: 60 °C at 2026-07-19T12:09:27.769Z (121.061 s); <68: 60 °C at 2026-07-19T12:09:27.769Z (121.061 s) | -5.45 °C/min over endpoints |
| 3 | `2026-07-19T12:19:33.683Z` | `2026-07-19T12:19:34.357Z` | 71 °C | 61 °C at 2026-07-19T12:21:34.653Z; 120.970 s | <71: 61 °C at 2026-07-19T12:21:34.653Z (120.970 s); <70: 61 °C at 2026-07-19T12:21:34.653Z (120.970 s); <69: 61 °C at 2026-07-19T12:21:34.653Z (120.970 s); <68: 61 °C at 2026-07-19T12:21:34.653Z (120.970 s) | -4.96 °C/min over endpoints |
| 4 | `2026-07-19T12:45:43.022Z` | `2026-07-19T12:45:43.357Z` | 71 °C | 59 °C at 2026-07-19T12:47:43.811Z; 120.789 s | <71: 59 °C at 2026-07-19T12:47:43.811Z (120.789 s); <70: 59 °C at 2026-07-19T12:47:43.811Z (120.789 s); <69: 59 °C at 2026-07-19T12:47:43.811Z (120.789 s); <68: 59 °C at 2026-07-19T12:47:43.811Z (120.789 s) | -5.96 °C/min over endpoints |
| 5 | `2026-07-19T12:57:48.702Z` | `2026-07-19T12:57:49.357Z` | 71 °C | 62 °C at 2026-07-19T12:59:49.949Z; 121.246 s | <71: 62 °C at 2026-07-19T12:59:49.949Z (121.246 s); <70: 62 °C at 2026-07-19T12:59:49.949Z (121.246 s); <69: 62 °C at 2026-07-19T12:59:49.949Z (121.246 s); <68: 62 °C at 2026-07-19T12:59:49.949Z (121.246 s) | -4.45 °C/min over endpoints |
| 6 | `2026-07-19T13:13:57.809Z` | `2026-07-19T13:13:58.357Z` | 71 °C | 60 °C at 2026-07-19T13:15:58.723Z; 120.913 s | <71: 60 °C at 2026-07-19T13:15:58.723Z (120.913 s); <70: 60 °C at 2026-07-19T13:15:58.723Z (120.913 s); <69: 60 °C at 2026-07-19T13:15:58.723Z (120.913 s); <68: 60 °C at 2026-07-19T13:15:58.723Z (120.913 s) | -5.46 °C/min over endpoints |
| 7 | `2026-07-19T13:28:04.709Z` | `2026-07-19T13:28:05.357Z` | 72 °C | 61 °C at 2026-07-19T13:30:05.951Z; 121.242 s | <71: 61 °C at 2026-07-19T13:30:05.951Z (121.242 s); <70: 61 °C at 2026-07-19T13:30:05.951Z (121.242 s); <69: 61 °C at 2026-07-19T13:30:05.951Z (121.242 s); <68: 61 °C at 2026-07-19T13:30:05.951Z (121.242 s) | -5.44 °C/min over endpoints |
| 8 | `2026-07-19T13:40:10.664Z` | `2026-07-19T13:40:11.357Z` | 71 °C | 59 °C at 2026-07-19T13:42:11.852Z; 121.187 s | <71: 59 °C at 2026-07-19T13:42:11.852Z (121.187 s); <70: 59 °C at 2026-07-19T13:42:11.852Z (121.187 s); <69: 59 °C at 2026-07-19T13:42:11.852Z (121.187 s); <68: 59 °C at 2026-07-19T13:42:11.852Z (121.187 s) | -5.94 °C/min over endpoints |

For these episodes, the next reported Radiator 1 source value was already below 68 °C in every case. Therefore, each tabulated threshold elapsed time is an **upper bound on when the first below-threshold state became visible at the available source cadence**, not the exact physical crossing time. Endpoint cooling rates range over intervals of roughly two minutes and materially under-resolve any faster transient. A lower numerical endpoint slope magnitude does not imply gentler instantaneous cooling.

## Episode context

“At anchor receipt” below is the latest state Home Assistant exposed when the qualifying Radiator 1 update was first captured. The parenthetical source time makes staleness explicit. The ±5-minute column uses only distinct source timestamps received in the window.

### Episode 1: 2026-07-19T11:55:20.655Z (71 °C)

This episode is left-censored: the high state was already present at capture start, so pre-episode context and rise timing are unavailable.

| Signal | At anchor receipt (source time) | Distinct-source ±5 min summary |
|---|---|---|
| EPS power | 1411 W (`2026-07-19T11:55:20.654Z`) | 1411–1471 W; 3 distinct source timestamp(s) |
| AC-couple power | 2 W (`2026-07-19T11:55:20.654Z`) | 1–2 W; 3 distinct source timestamp(s) |
| PV total power | 0 W (`2026-07-19T10:10:21.226Z`) | 0–0 W; 1 distinct source timestamp(s) |
| Battery power | -1646 W (`2026-07-19T11:55:20.654Z`) | -1712–-1618 W; 3 distinct source timestamp(s) |
| Grid power | 0.0 W (`2026-07-19T10:10:21.246Z`) | 0–0 W; 1 distinct source timestamp(s) |
| Battery SOC | 82 % (`2026-07-19T10:10:21.238Z`) | 82–82 %; 1 distinct source timestamp(s) |
| Battery status | Discharging (`2026-07-19T10:10:21.247Z`) | Discharging; 1 distinct source timestamp(s) |
| Inverter status | normal (`2026-07-19T10:10:21.242Z`) | normal; 1 distinct source timestamp(s) |
| Status code | 64 (`2026-07-19T10:10:21.242Z`) | 64–64 (unit null); 1 distinct source timestamp(s) |
| Operating mode | Normal (`2026-07-19T10:10:21.342Z`) | Normal; 1 distinct source timestamp(s) |

Short changing-power trajectories (distinct source updates, ±3 minutes of anchor receipt):

- EPS power: 2026-07-19T11:55:20.654Z=1411 W; 2026-07-19T11:57:21.494Z=1471 W
- AC-couple power: 2026-07-19T11:55:20.654Z=2 W; 2026-07-19T11:57:21.494Z=1 W
- PV total power: 2026-07-19T10:10:21.226Z=0 W
- Battery power: 2026-07-19T11:55:20.654Z=-1646 W; 2026-07-19T11:57:21.494Z=-1712 W
- Grid power: 2026-07-19T10:10:21.246Z=0.0 W

### Episode 2: 2026-07-19T12:07:26.708Z (71 °C)

| Signal | At anchor receipt (source time) | Distinct-source ±5 min summary |
|---|---|---|
| EPS power | 708 W (`2026-07-19T12:07:26.707Z`) | 708–1105 W; 5 distinct source timestamp(s) |
| AC-couple power | 1 W (`2026-07-19T12:05:25.780Z`) | 1–2 W; 2 distinct source timestamp(s) |
| PV total power | 0 W (`2026-07-19T10:10:21.226Z`) | no distinct source update observed in window |
| Battery power | -867 W (`2026-07-19T12:07:26.707Z`) | -1314–-867 W; 5 distinct source timestamp(s) |
| Grid power | 0.0 W (`2026-07-19T10:10:21.246Z`) | no distinct source update observed in window |
| Battery SOC | 82 % (`2026-07-19T10:10:21.238Z`) | no distinct source update observed in window |
| Battery status | Discharging (`2026-07-19T10:10:21.247Z`) | no distinct source update observed in window |
| Inverter status | normal (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Status code | 64 (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Operating mode | Normal (`2026-07-19T10:10:21.342Z`) | no distinct source update observed in window |

Short changing-power trajectories (distinct source updates, ±3 minutes of anchor receipt):

- EPS power: 2026-07-19T12:05:25.780Z=1105 W; 2026-07-19T12:07:26.707Z=708 W; 2026-07-19T12:09:27.768Z=727 W
- AC-couple power: 2026-07-19T12:05:25.780Z=1 W
- PV total power: none
- Battery power: 2026-07-19T12:05:25.780Z=-1297 W; 2026-07-19T12:07:26.707Z=-867 W; 2026-07-19T12:09:27.768Z=-901 W
- Grid power: none

### Episode 3: 2026-07-19T12:19:33.683Z (71 °C)

| Signal | At anchor receipt (source time) | Distinct-source ±5 min summary |
|---|---|---|
| EPS power | 669 W (`2026-07-19T12:19:33.682Z`) | 669–780 W; 4 distinct source timestamp(s) |
| AC-couple power | 1 W (`2026-07-19T12:17:32.760Z`) | 0–1 W; 2 distinct source timestamp(s) |
| PV total power | 0 W (`2026-07-19T10:10:21.226Z`) | no distinct source update observed in window |
| Battery power | -883 W (`2026-07-19T12:19:33.682Z`) | -922–-842 W; 4 distinct source timestamp(s) |
| Grid power | 0.0 W (`2026-07-19T10:10:21.246Z`) | no distinct source update observed in window |
| Battery SOC | 82 % (`2026-07-19T10:10:21.238Z`) | no distinct source update observed in window |
| Battery status | Discharging (`2026-07-19T10:10:21.247Z`) | no distinct source update observed in window |
| Inverter status | normal (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Status code | 64 (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Operating mode | Normal (`2026-07-19T10:10:21.342Z`) | no distinct source update observed in window |

Short changing-power trajectories (distinct source updates, ±3 minutes of anchor receipt):

- EPS power: 2026-07-19T12:17:32.760Z=752 W; 2026-07-19T12:19:33.682Z=669 W; 2026-07-19T12:21:34.652Z=780 W
- AC-couple power: 2026-07-19T12:17:32.760Z=1 W; 2026-07-19T12:21:34.652Z=0 W
- PV total power: none
- Battery power: 2026-07-19T12:17:32.760Z=-922 W; 2026-07-19T12:19:33.682Z=-883 W; 2026-07-19T12:21:34.652Z=-895 W
- Grid power: none

### Episode 4: 2026-07-19T12:45:43.022Z (71 °C)

| Signal | At anchor receipt (source time) | Distinct-source ±5 min summary |
|---|---|---|
| EPS power | 791 W (`2026-07-19T12:45:43.022Z`) | 616–816 W; 5 distinct source timestamp(s) |
| AC-couple power | 1 W (`2026-07-19T12:35:39.173Z`) | 0–0 W; 1 distinct source timestamp(s) |
| PV total power | 0 W (`2026-07-19T10:10:21.226Z`) | no distinct source update observed in window |
| Battery power | -941 W (`2026-07-19T12:45:43.021Z`) | -1023–-730 W; 5 distinct source timestamp(s) |
| Grid power | 0.0 W (`2026-07-19T10:10:21.246Z`) | no distinct source update observed in window |
| Battery SOC | 82 % (`2026-07-19T10:10:21.238Z`) | no distinct source update observed in window |
| Battery status | Discharging (`2026-07-19T10:10:21.247Z`) | no distinct source update observed in window |
| Inverter status | normal (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Status code | 64 (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Operating mode | Normal (`2026-07-19T10:10:21.342Z`) | no distinct source update observed in window |

Short changing-power trajectories (distinct source updates, ±3 minutes of anchor receipt):

- EPS power: 2026-07-19T12:43:41.798Z=787 W; 2026-07-19T12:45:43.022Z=791 W; 2026-07-19T12:47:43.811Z=806 W
- AC-couple power: none
- PV total power: none
- Battery power: 2026-07-19T12:43:41.798Z=-968 W; 2026-07-19T12:45:43.021Z=-941 W; 2026-07-19T12:47:43.810Z=-972 W
- Grid power: none

### Episode 5: 2026-07-19T12:57:48.702Z (71 °C)

| Signal | At anchor receipt (source time) | Distinct-source ±5 min summary |
|---|---|---|
| EPS power | 1001 W (`2026-07-19T12:57:48.702Z`) | 974–1007 W; 5 distinct source timestamp(s) |
| AC-couple power | 1 W (`2026-07-19T12:51:45.666Z`) | no distinct source update observed in window |
| PV total power | 0 W (`2026-07-19T10:10:21.226Z`) | no distinct source update observed in window |
| Battery power | -1243 W (`2026-07-19T12:57:48.702Z`) | -1243–-1182 W; 5 distinct source timestamp(s) |
| Grid power | 0.0 W (`2026-07-19T10:10:21.246Z`) | no distinct source update observed in window |
| Battery SOC | 82 % (`2026-07-19T10:10:21.238Z`) | no distinct source update observed in window |
| Battery status | Discharging (`2026-07-19T10:10:21.247Z`) | no distinct source update observed in window |
| Inverter status | normal (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Status code | 64 (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Operating mode | Normal (`2026-07-19T10:10:21.342Z`) | no distinct source update observed in window |

Short changing-power trajectories (distinct source updates, ±3 minutes of anchor receipt):

- EPS power: 2026-07-19T12:55:47.709Z=991 W; 2026-07-19T12:57:48.702Z=1001 W; 2026-07-19T12:59:49.948Z=974 W
- AC-couple power: none
- PV total power: none
- Battery power: 2026-07-19T12:55:47.709Z=-1182 W; 2026-07-19T12:57:48.702Z=-1243 W; 2026-07-19T12:59:49.948Z=-1214 W
- Grid power: none

### Episode 6: 2026-07-19T13:13:57.809Z (71 °C)

| Signal | At anchor receipt (source time) | Distinct-source ±5 min summary |
|---|---|---|
| EPS power | 427 W (`2026-07-19T13:13:57.809Z`) | 427–538 W; 5 distinct source timestamp(s) |
| AC-couple power | 1 W (`2026-07-19T12:51:45.666Z`) | 2–2 W; 1 distinct source timestamp(s) |
| PV total power | 0 W (`2026-07-19T10:10:21.226Z`) | no distinct source update observed in window |
| Battery power | -597 W (`2026-07-19T13:13:57.809Z`) | -719–-597 W; 5 distinct source timestamp(s) |
| Grid power | 0.0 W (`2026-07-19T10:10:21.246Z`) | no distinct source update observed in window |
| Battery SOC | 82 % (`2026-07-19T10:10:21.238Z`) | no distinct source update observed in window |
| Battery status | Discharging (`2026-07-19T10:10:21.247Z`) | no distinct source update observed in window |
| Inverter status | normal (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Status code | 64 (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Operating mode | Normal (`2026-07-19T10:10:21.342Z`) | no distinct source update observed in window |

Short changing-power trajectories (distinct source updates, ±3 minutes of anchor receipt):

- EPS power: 2026-07-19T13:11:56.491Z=538 W; 2026-07-19T13:13:57.809Z=427 W; 2026-07-19T13:15:58.722Z=464 W
- AC-couple power: none
- PV total power: none
- Battery power: 2026-07-19T13:11:56.491Z=-719 W; 2026-07-19T13:13:57.809Z=-597 W; 2026-07-19T13:15:58.722Z=-598 W
- Grid power: none

### Episode 7: 2026-07-19T13:28:04.709Z (72 °C)

| Signal | At anchor receipt (source time) | Distinct-source ±5 min summary |
|---|---|---|
| EPS power | 898 W (`2026-07-19T13:28:04.709Z`) | 831–911 W; 5 distinct source timestamp(s) |
| AC-couple power | 2 W (`2026-07-19T13:28:04.709Z`) | 1–2 W; 5 distinct source timestamp(s) |
| PV total power | 0 W (`2026-07-19T10:10:21.226Z`) | no distinct source update observed in window |
| Battery power | -1085 W (`2026-07-19T13:28:04.709Z`) | -1130–-999 W; 5 distinct source timestamp(s) |
| Grid power | 0.0 W (`2026-07-19T10:10:21.246Z`) | no distinct source update observed in window |
| Battery SOC | 82 % (`2026-07-19T10:10:21.238Z`) | no distinct source update observed in window |
| Battery status | Discharging (`2026-07-19T10:10:21.247Z`) | no distinct source update observed in window |
| Inverter status | normal (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Status code | 64 (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Operating mode | Normal (`2026-07-19T10:10:21.342Z`) | no distinct source update observed in window |

Short changing-power trajectories (distinct source updates, ±3 minutes of anchor receipt):

- EPS power: 2026-07-19T13:26:03.700Z=836 W; 2026-07-19T13:28:04.709Z=898 W; 2026-07-19T13:30:05.951Z=911 W
- AC-couple power: 2026-07-19T13:26:03.700Z=1 W; 2026-07-19T13:28:04.709Z=2 W; 2026-07-19T13:30:05.951Z=1 W
- PV total power: none
- Battery power: 2026-07-19T13:26:03.700Z=-1044 W; 2026-07-19T13:28:04.709Z=-1085 W; 2026-07-19T13:30:05.950Z=-1130 W
- Grid power: none

### Episode 8: 2026-07-19T13:40:10.664Z (71 °C)

| Signal | At anchor receipt (source time) | Distinct-source ±5 min summary |
|---|---|---|
| EPS power | 725 W (`2026-07-19T13:40:10.664Z`) | 501–763 W; 5 distinct source timestamp(s) |
| AC-couple power | 1 W (`2026-07-19T13:34:07.728Z`) | 2–2 W; 1 distinct source timestamp(s) |
| PV total power | 0 W (`2026-07-19T10:10:21.226Z`) | no distinct source update observed in window |
| Battery power | -910 W (`2026-07-19T13:40:10.664Z`) | -915–-699 W; 5 distinct source timestamp(s) |
| Grid power | 0.0 W (`2026-07-19T10:10:21.246Z`) | no distinct source update observed in window |
| Battery SOC | 82 % (`2026-07-19T10:10:21.238Z`) | no distinct source update observed in window |
| Battery status | Discharging (`2026-07-19T10:10:21.247Z`) | no distinct source update observed in window |
| Inverter status | normal (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Status code | 64 (`2026-07-19T10:10:21.242Z`) | no distinct source update observed in window |
| Operating mode | Normal (`2026-07-19T10:10:21.342Z`) | no distinct source update observed in window |

Short changing-power trajectories (distinct source updates, ±3 minutes of anchor receipt):

- EPS power: 2026-07-19T13:38:09.731Z=548 W; 2026-07-19T13:40:10.664Z=725 W; 2026-07-19T13:42:11.851Z=763 W
- AC-couple power: none
- PV total power: none
- Battery power: 2026-07-19T13:38:09.731Z=-717 W; 2026-07-19T13:40:10.664Z=-910 W; 2026-07-19T13:42:11.851Z=-915 W
- Grid power: none

## Patterns and associations

- At episode anchor receipts, EPS power was 427–1411 W (median 758 W), while battery power was -1646–-597 W (median -925.5 W). These co-occurred with the temperature cycles but do not identify their cause.
- AC-couple power at anchors was 1–2 W. PV total power remained 0 W, grid power 0 W, battery SOC 82%, battery status `Discharging`, inverter status `normal`, status code `64`, and operating mode `Normal` in every one-second snapshot. For these constant fields, each had only one source timestamp—predating the capture—so they are stale repeated states, not 7,200 independently refreshed confirmations.
- Radiator 1 repeatedly climbed through upper-60s/70 °C reports and then appeared at 59–63 °C on the next source update. Radiator 2 showed smaller contemporaneous cycles (47–51 °C). The synchronous source timestamps on many changing entities suggest batched upstream/integration refreshes, but the per-entity local-versus-cloud lineage is unproven.
- No causal claim is supported. In particular, the capture cannot determine whether fan behavior occurred, whether a control threshold was crossed between updates, or whether power changes caused, followed, or merely coincided with temperature changes.

## Explicit availability summary

- Available in all 7,200 snapshots: all 12 allowlisted entity objects, their `raw_state`, and their `source_last_updated`.
- Null units: battery status, operating mode, inverter status, and status code in all snapshots; these are categorical/unlabelled fields.
- Unavailable from the capture: fan command, fan state, RPM, PWM, speed, and duty. No proxy inference was made.
- Missing capture context: proven per-entity local-dongle/cloud lineage and any sub-source-cadence thermal or electrical behavior.

## Integrity and reproducibility notes

The analysis is reproducible from the two named NDJSON inputs using the numbered method above. It performs no interpolation, network access, device query, or evidence write. Input SHA-256 values were checked before and after report generation. The report intentionally contains no credential value, Authorization header, or protected credential path.
