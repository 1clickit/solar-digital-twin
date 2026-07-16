# Solar Digital Twin Portal UI Prototype

## Status and Boundary

This is a reviewable visual prototype, not an accepted Engineering Bible
decision. `prototypes/solar_portal_mockup.html` is a standalone offline file
containing synthetic example values only. It does not replace or modify the
operational EG4 portal, collect telemetry, read evidence, or contact a device,
service, API, or filesystem.

## Initial Hosting Decision

The prototype and initial production Solar Digital Twin portal should be hosted
on `solardt`. The portal should remain operationally separate from collectors
and eventually run under an appropriate unprivileged identity. Keeping it on
`solardt` initially avoids an unnecessary additional Proxmox VM or container,
a network-filesystem dependency, duplicated state, and extra maintenance.

A separate Proxmox web VM or LXC should be reconsidered only when justified by
external or less-trusted network exposure, reverse-proxy or DMZ requirements,
measurable resource contention, independent availability or maintenance needs,
or a shared web-services platform.

If the frontend is separated later, it should consume a controlled read-only
interface from `solardt`. It must not mount or receive direct access to
credentials, raw evidence directories, or the live project filesystem.

This is a reviewable architecture decision. It does not authorize deployment,
installation, service startup, or any change to an operational portal.

## Current-Operation-First Tabs and Layout

The operation-first `Overview` tab is selected by default. It contains only the
current health, solar/load, battery-current, AC-source state, SOC comparison,
and voltage comparison needed for quick reference. The
other primary tabs keep deeper material available without making Overview
unnecessarily tall:

- `Trends` contains source-labeled historical-chart placeholders;
- `Forensics` contains the synthetic latest notice and future timeline,
  confidence, and cross-source-correlation space;
- `Sources & Traceability` contains source freshness, provenance, normalized-
  data boundaries, and evidence traceability.

The embedded tab behavior makes no network request and stores no state. Semantic
tab buttons and panels expose their relationships and selected state to
assistive technology, and support click, Left/Right Arrow, Home, and End
navigation.

The first row answers the normal operational questions in quick-glance order:

1. Are the system and its sources healthy and fresh?
2. How does solar input compare with house load, and what is the net result?
3. Is the battery bank charging or discharging, and by how much?
4. Which AC source is active?

The Solar/load widget combines distinct concentric arcs and places the net power
result in the center. The next section combines Trusted Battery SOC from
SolarAssistant/JK BMS and EG4 Estimated SOC in one comparison ring while keeping
their values and sources distinct. The trusted SOC remains the dominant center
value, and EG4 remains labeled comparison only; the values are never merged,
averaged, substituted, or silently corrected. Battery 1 and Battery 2 voltage
share a comparison ring whose center shows their calculated average and whose
legend preserves each measured value and a voltage delta. Source and
observation-age labels remain visible but compact.

Battery current is the primary quick-reference battery-flow gauge in the top
operational row. The battery section below is a balanced two-card row containing
SOC and voltage comparisons. The previous `Combined bank` card and the separate
Battery bank power ring have been removed.

## Ring Family and Geometry

All rings share component classes, sizing variables, track treatment, typography,
and SVG geometry. Comparison rings use paired concentric arcs. Their center
shows the most trusted or actionable summary: trusted SOC for the SOC comparison,
average DC voltage for the battery-voltage comparison, and net power for the
solar/load comparison. Compact legends associate each arc with its individual
value and source so color is not the only cue.

The battery-current comparison uses independent outer and inner bipolar rings
for Battery 1 and Battery 2 from a shared neutral point. Positive DC current
fills the upper green semicircle and negative DC current fills the lower red
semicircle. Individual signed current labels identify each battery, while the
center shows compact net DC current. Net battery kW and bank voltage remain
useful supporting values but do not require a separate ring. Numeric angles,
coordinates, and other ring-geometry labels are implementation details and must
not be visible to users.

Solar input versus grid return/export remains an available directional concept,
but the primary operational power comparison is solar input versus house load.

Single-direction rings remain part of the visual family for measurements where
comparison or direction is not meaningful. Voltage arcs show position within a
labeled operating range rather than implying direction. AC source and freshness
remain state cards because numeric sweeps would be misleading.

## Electrical Display Hierarchy

Each ring centers the most actionable unit: net kW for solar/load and signed net
DC current for battery flow. The battery-current ring keeps net battery kW and
DC voltage as smaller supporting values. Every current remains explicitly
labeled AC or DC, and each card identifies its example as `Synthetic measured`
or `Synthetic calculated`. Source names and synthetic observation ages remain
visible.

The prototype display convention is positive current = charging and negative
current = discharging. Before binding live data, SolarAssistant's native current
field polarity must be verified. If its convention differs, polarity must be
normalized at the adapter boundary rather than silently reinterpreted in the
portal.

## Central Theme and Scale Variables

The page's `:root` custom properties are the adjustment point for the visual
system:

- `--battery-charging`: green charging arc
- `--battery-discharging`: red discharging arc
- `--solar-input`: yellow solar-input arc
- `--grid-export`: blue grid-return/export arc
- `--neutral-track`: available but inactive ring track
- `--state-healthy`, `--state-warning`, `--state-stale`, and
  `--state-unavailable`: freshness and availability states
- `--panel-bg`, `--text`, and `--muted`: panel and typography colors
- `--ring-size`, `--ring-stroke`, and `--ring-radius`: shared ring scale

Changing one of these variables changes the corresponding component treatment;
SVG markup does not contain individually hard-coded theme colors.

## Future Data Binding

A future implementation may bind only source-labeled, freshness-aware normalized
data. It must preserve the authority of raw evidence, keep measured and
calculated values distinguishable, and show unavailable or stale data honestly.
The prototype's embedded values and trend shapes must not be treated as source
records or an integration contract.

## Future Device Navigation and Parameter History

**Overview is curated; device tabs are complete.** Overview presents the small
set of trusted, actionable summaries needed for normal operation. In contrast,
each future `EG4`, `SolarAssistant`, and `ESP32` tab must make every available
parsed, non-secret, read-only parameter exposed by that source accessible, not
merely a selected or commonly useful subset.

Future device-specific technical tabs should appear at the far right of the
primary navigation. Complete device views include current values and null,
unavailable, stale, unsupported, and unknown values where the source exposes
them. They include status, mode, alarm, identity, counter, diagnostic, and
telemetry fields. Each parsed parameter should retain its original source field
name, stable portal metric identifier, normalized display name, unit, source
timestamp, observation age and freshness, provenance/source, and classification
as measured, calculated, normalized, estimated, or derived.

Device fields should be grouped by purpose rather than presented as one
unstructured table. Search, filtering, collapsed sections, and `show all`,
`show changed`, and `show unavailable` controls may improve usability, but they
must not silently omit parameters from a true `Show all` view.

Complete does not include passwords, tokens, API keys, encryption keys,
credentials, or other secret material. Writable controls and device actions
must not be mixed into the read-only telemetry view. Enormous unparsed raw
payloads must not be presented as ordinary parameters; raw evidence remains
reachable through controlled traceability mechanisms instead of being confused
with parsed device parameters.

Each parameter should have a stable metric identifier and later be clickable to
open its history. Parameter history should retain source, units, freshness,
provenance, measurement type, and time-range selection. Related metrics may be
compared without silently merging their sources. A side drawer may support
quick inspection, while a dedicated parameter page or URL may support deeper
forensic analysis. These are reviewed intentions only and are not implemented
or authorized for deployment by this prototype.

## Browser-Review Choices

The following remain intentionally easy to adjust after visual review:

- card density and the desktop column balance;
- ring diameter, stroke width, and center-value type scale;
- exact theme hues and contrast within the named semantic roles;
- half-ring magnitude scales for solar/grid and battery power;
- placement and wording of compact direction legends;
- trend height and the amount of lower-page detail visible at once.
