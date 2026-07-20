# EG4 Home Assistant Telemetry

## Status and proven boundary

Home Assistant was successfully used as a read-only telemetry bridge for a
completed two-hour Solar Digital Twin capture. The temporary collector made
HTTP `GET` requests only. It requested `/api/states` once per second and
filtered an explicit entity allowlist locally; all 7,200 requests succeeded
with zero errors and terminal reason `duration_complete`.

Authentication used a protected external Home Assistant token. Its value and
storage location are not repository material. The token may have more
authority than the collector exercised. The proven safety boundary came from
structural GET-only behavior, an explicit local allowlist, and never invoking
service or state-changing endpoints. This result does not authorize a
production collector, broader entity access, or any control action.

The detailed evidence analysis is
[`capture_analyses/cooling-control-20260719T115613Z-analysis.md`](capture_analyses/cooling-control-20260719T115613Z-analysis.md).

## Proven collection method

The validated temporary workflow was:

1. issue one authenticated `GET /api/states` request at one-second cadence;
2. retain only the explicit allowlisted entities from the returned state set;
3. preserve the Home Assistant entity ID, raw value, unit,
   `last_updated`/equivalent source timestamp, and Solar Digital Twin receipt
   timestamp; and
4. write immutable NDJSON snapshots and an append-only capture manifest.

Home Assistant API access did not create another direct connection to the EG4
Wi-Fi dongle. It read entity states already populated inside Home Assistant.
Direct dongle access remains a distinct, separately gated path with unresolved
single-client and control-capability risks.

## Source cadence is not polling cadence

One-second polling produced one-second snapshots, not one-second independent
measurements. Repeated snapshots frequently carried unchanged entity source
timestamps. An entity is independently refreshed only when its
`last_updated`, or an explicitly documented equivalent source timestamp,
changes. Repeated snapshots with an unchanged source timestamp must not be
counted as new measurements.

The completed capture illustrates the distinction: 7,200 snapshots contained
only 52 distinct Radiator 1 source timestamps and 32 distinct Radiator 2 source
timestamps. Their coarse source cadence materially limited event timing and
cooling-rate interpretation. Consumers must preserve both source and receipt
timestamps, calculate freshness from the correct timestamp, and avoid
interpolation that implies unavailable resolution.

An unchanged source timestamp means no newly reported update was observed. It
does not prove that the underlying physical quantity was constant.

## Provenance and source roles

EG4 Web Monitor was configured in hybrid mode. Until lineage is proven per
entity, every value imported through this route must retain this provenance:

`Home Assistant → EG4 Web Monitor hybrid mode`

Hybrid mode does not establish whether an individual entity came from a local
dongle transaction, the EG4 cloud, cached state, or another upstream behavior.
Local-dongle versus cloud lineage remains unproven per entity. These values
therefore cannot be promoted as independent corroboration of existing EG4
measurements solely because Home Assistant exposed them.

Home Assistant may expose useful telemetry that SolarAssistant does not, but
it remains a separately identified source. SolarAssistant remains the trusted
JK BMS battery source. `solardt` remains the authoritative aggregation,
provenance, normalization, comparison, and evidence layer. Never silently
merge or substitute Home Assistant, SolarAssistant, direct-EG4, or EG4-cloud
measurements. Comparisons must preserve each source's identity, timestamps,
authority, and transformation lineage.

## Validated EG4 entity allowlist

The completed capture validated the following exact Home Assistant entity IDs.
Entity availability and meaning can change with integration, firmware, or
configuration updates and must be revalidated before future collection.

| Category | Logical role | Validated entity ID |
|---|---|---|
| Temperature | Radiator 1 temperature | `sensor.sna12k_us_44830p0125_radiator_1_temperature` |
| Temperature | Radiator 2 temperature | `sensor.sna12k_us_44830p0125_radiator_2_temperature` |
| Power | EPS power | `sensor.sna12k_us_44830p0125_eps_power` |
| Power | AC-couple power | `sensor.sna12k_us_44830p0125_ac_couple_power` |
| Power | PV total power | `sensor.sna12k_us_44830p0125_pv_total_power` |
| Power | Battery power | `sensor.sna12k_us_44830p0125_battery_power` |
| Power | Grid power | `sensor.sna12k_us_44830p0125_grid_power` |
| Battery context | EG4-reported state of charge | `sensor.sna12k_us_44830p0125_state_of_charge` |
| Battery context | EG4-reported battery status | `sensor.sna12k_us_44830p0125_battery_status` |
| Inverter context | Inverter status | `sensor.sna12k_us_44830p0125_status` |
| Inverter context | Status code | `sensor.sna12k_us_44830p0125_status_code` |
| Inverter context | Operating mode state | `select.sna12k_us_44830p0125_operating_mode` |

The operating-mode entity is a control-capable `select`. Its state was read
from `/api/states`; the entity was never called or changed. Future telemetry
collectors may observe an explicitly allowlisted state but must never invoke a
control-capable entity.

No fan command, state, RPM, PWM, speed, or duty telemetry was discovered.
Radiator temperature is not fan-state telemetry and must not be used to infer
fan operation.

## Control prohibition

Solar Digital Twin telemetry collectors must not call Home Assistant services
or control-capable `switch`, `select`, `number`, or `button` entities. They
must not write states or invoke integration-specific control endpoints. Hiding
a control entity in the UI or omitting it from output does not reduce the
underlying integration's authority.

Any future collector design must retain the GET-only construction, explicit
input allowlist, bounded cadence, timeout and error handling, and credential
separation demonstrated by the temporary capture. A future production design
requires its own bounded authorization and validation.

## Recommended retained metadata

For each retained observation, preserve at least:

- exact Home Assistant entity ID;
- raw and normalized value, with transformation identity when applicable;
- unit;
- upstream/source timestamp;
- Solar Digital Twin receipt timestamp;
- freshness and availability state;
- integration mode, currently `EG4 Web Monitor hybrid mode`;
- source confidence and known lineage limitations; and
- comparison source and alignment offset when a value is compared with
  SolarAssistant, direct EG4, ESP32, or another source.

Retained metadata must make stale repeated states, unavailable values,
normalization, aggregation, and source substitution visible rather than
silently flattening them into one measurement stream.

## Relationship to deferred fan investigation

The completed cooling capture is useful baseline evidence for reported
temperature-cycle behavior and for the Home Assistant collection method. It
does not measure fan activity. Further fan investigation requires additional
instrumentation capable of observing fan command, RPM, PWM/duty, electrical
current, or synchronized acoustic evidence and is deferred until after the
primary Solar Digital Twin milestones.
