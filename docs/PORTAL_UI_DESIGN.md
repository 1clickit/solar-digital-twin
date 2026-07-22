# Solar Digital Twin Portal UI Design

## Status and Boundary

This document is the authoritative design record for the reviewable Solar
Digital Twin portal prototype and its accepted future implementation direction.
It does not promote the prototype to an operational portal or authorize
deployment.

`prototypes/solar_portal_mockup.html` is a standalone offline file containing
synthetic example values only. It does not replace the operational EG4 portal,
collect telemetry, read evidence, or contact a device, service, API, or
filesystem.

## Hosting and Runtime Separation

The prototype and initial production Solar Digital Twin portal should be hosted
on `solardt`, remain operationally separate from collectors, and eventually run
under an appropriate unprivileged identity. This avoids an unnecessary VM or
container, network-filesystem dependency, duplicated state, and added
maintenance.

A separate frontend host should be reconsidered only for external or
less-trusted exposure, reverse-proxy or DMZ requirements, measurable resource
contention, independent availability or maintenance, or a shared web-services
platform. A separated frontend must use a controlled read-only interface and
must not mount or receive credentials, raw evidence directories, or the live
project filesystem.

## Accepted Navigation and Overview

`Overview` is the operation-first default tab. The compact current-operation
row is, in order:

1. Solar vs house load
2. Volcast forecast
3. System health
4. Current AC source

The Battery bank row is, in order:

1. Battery SOC
2. Battery voltage
3. Battery current
4. Battery cell voltage

Battery titles do not use the word `comparison`. Overview is curated and
operational rather than provenance-heavy. Long source, calculation, and
traceability explanations belong in `Sources & Traceability`, source-data tabs,
or metric-history views rather than beneath homepage dials.

The remaining primary tabs are `Trends`, `Forensics`, and
`Sources & Traceability`. Embedded tab behavior is local, stores no state, and
uses semantic buttons and panels with keyboard navigation and assistive-
technology relationships.

## Accepted Operational Cards

### Solar vs house load

The combined presentation centers:

- `3.3 kW`
- `13.8 A`
- `240.1 V`

There is no leading plus sign. Compact Solar and Load values remain. The
synthetic prototype includes subtle rolling 60-minute minimum/maximum context,
while provenance and calculation explanations are absent beneath the dial.

### Volcast forecast

Volcast remains synthetic-only. Its Overview card has the same general size as
the other top-row cards and uses the broad information organization of the
Volcast phone application without copying, embedding, or representing itself as
that application. The internal content region scrolls: initial content ends
around the multi-day bars, while hourly information and the following timestamp
require scrolling:

`Last update - Thursday - 07-16-2026 - 17:56`

Future production retrieval should run server-side every 30 minutes. Browser
F5 may request an immediate additional server-side refresh, with duplicate or
simultaneous refreshes coalesced. The browser must never receive the API key or
contact Volcast directly. A failed refresh retains the last successful
forecast. `Forecast issued` or generated time is shown only when Volcast
explicitly supplies that timestamp.

The complete Volcast source-data tab must expose daily, hourly, and all parsed
five-minute forecast entries. The compact Overview card must not render
hundreds of five-minute rows. API keys remain outside Git, chat, logs, command
arguments, reports, and ordinary backups.

### Battery SOC

Trusted SolarAssistant/JK BMS SOC remains central. EG4 SOC remains a separately
identified comparison estimate and is never merged, averaged, substituted, or
used to silently correct the trusted value.

### Battery voltage

The center reads `54.80 VDC`, without an `Average` label or homepage delta.
Battery 1 and Battery 2 pack voltages remain visible.

### Battery current

The center reads `51.1 A` and `54.8 V`; the earlier `2.8 kW DC` center line is
removed. Homepage current does not require a leading sign. Charging uses green
upper arcs, discharging uses red lower arcs, and near-zero uses neutral gray.
Precise signed values remain available in source-data and history views. Where
appropriate, future negative source/history values use accounting form such as
`(3000)`.

### Current AC source and health

AC source and freshness remain compact state cards rather than misleading
numeric sweeps. State, mode, availability, and source freshness must not be
represented as healthy when unknown or stale.

## Battery Cell Voltage

### Accepted homepage data model

The homepage needs only these four values per pack:

- average cell voltage;
- highest cell voltage;
- lowest cell voltage; and
- differential or imbalance.

They support normal visualization, spread, low-voltage detection, high-voltage
detection, simultaneous low/high detection, and future local events. Individual
cell voltages and identities, native BMS alarms, configured BMS thresholds,
protection states, and release thresholds may be useful later but are not
prerequisites for this homepage function. `Sum` is not interchangeable with
average cell voltage.

### Safety semantics

The Solar Digital Twin initially uses `2.50 V` as the low cell-voltage display
and alarm threshold and `3.65 V` as the high threshold. These must not be
claimed as exact JK BMS configuration unless later verified. Yellow caution
ranges are prototype visual guidance, not verified BMS settings. Green is the
normal operating region; yellow is caution near either limit; short red stop
markers identify the limits.

Each battery behaves independently. A minimum below `2.50 V` displays
`UNDER VOLTAGE` followed by the actual live value. A maximum above `3.65 V`
displays `OVER VOLTAGE` followed by the actual live value. When both conditions
exist, two stacked banners show both independently updating actual values.
Alarm banners take priority and may replace normal Avg/Max/Min content. The
actual abnormal value must never be replaced by the threshold value.

Future production behavior should create threshold-crossed and threshold-
cleared events and preserve first-observed and last-observed timestamps,
duration, battery identity, actual value, threshold, source, freshness, and
provenance. Related SolarAssistant and EG4 events may be linked without merging
source identities, and event history remains after the visible alarm clears.
This prototype does not implement live alarms or event logging.

### Current synthetic checkpoint

The current prototype has two enlarged Battery 1 and Battery 2 dials with:

- a shared open operating arc from the low limit near 5 o'clock clockwise to
  the high limit near 2 o'clock;
- short red threshold stops, yellow caution ends, and a dominant green normal
  region;
- short blue Min, white Avg, and red Max scale-crossing markers that share one
  fixed voltage-to-angle mapping and naturally overlap when values are close;
- a compact lower-center Min/Avg/Max readout with a differential calculated
  from the displayed synthetic maximum and minimum;
- normal, under-voltage, over-voltage, and simultaneous-fault structures; and
- actual alarm values in hidden synthetic alarm states.

The visually ambiguous moving inner green indicator has been removed. Exact
digital values are authoritative; marker positions provide approximate context.
Out-of-range positions clamp to the applicable endpoint while alarm banners
retain and prioritize the actual abnormal values.

## Trends

The Trends tab includes or will include solar energy generated today, house
energy consumed today, grid imported and exported today, and battery charged
and discharged today. Self-consumption percentage is shown only after its
accounting can be calculated reliably; the prototype must not present a
fabricated percentage as trustworthy.

## Future Forensics Controls

The future `Forensics` tab will reanalyze retained historical observations
without changing raw evidence. The authoritative event and episode semantics
are `docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md`. Planned controls include
minimum near-zero duration, drop percentage or amount, near-zero ceiling,
minimum pre-event production, pre/post windows, and optional recovery/relapse
thresholds.

Initial displayed research defaults are more than 30 seconds near zero, a
2-minute pre-event window, a 20-minute post-collapse window, approximately
250 W minimum baseline, approximately 90% collapse, and approximately 50 W
near-zero ceiling. They are adjustable analysis parameters, not proven
physical limits. Controls must not alter collectors, erase evidence, rewrite
historical records, or imply causation.

## Complete Source-Data Tabs

Production binding must consume the accepted version of
`TELEMETRY_OBSERVATION_CONTRACT.md`; the prototype does not define an
observation schema.

**Overview is curated; device tabs are complete.** The far-right tabs are
`EG4`, `SA` (with `SolarAssistant` as the panel heading), `ESP32`, and `Volcast`.
They are currently functional synthetic layouts, not live integrations.

In production, a true `Show all` view must expose every available parsed,
non-secret, read-only parameter preserved from each source, including present, null,
unavailable, stale, unsupported, and unknown values. It must retain original
source field names, normalized names, stable metric identifiers, units, source
or receipt timestamps, freshness and age, provenance, and measured,
calculated, normalized, derived, or estimated classification. Telemetry,
identity, status, mode, alarm, counter, and diagnostic fields remain accessible.
Grouping, search, filtering, and collapsed sections may improve usability but
must not silently omit parameters from a true `Show all` view.

The complete view excludes passwords, tokens, API keys, encryption keys,
credentials, and other secret material. Writable controls and device actions must not be mixed
into the read-only telemetry view. Large unparsed raw payloads are also excluded
from ordinary telemetry views. Raw evidence remains
available through controlled traceability rather than being confused with
parsed parameters.

## Metric History

Each stable metric identifier may later be clickable to open its history in a
dedicated parameter page or URL. History supports time-range selection,
minimum, maximum, average, last-change time, missing-data periods, source
identity, freshness, provenance, compatible comparisons, and related events.
Related sources may be compared but never silently merged. A side drawer may
support quick inspection while the dedicated page supports deeper analysis.

## Theme, Accessibility, and Data Binding

CSS custom properties centralize semantic colors, panel and text colors, ring
sizes, stroke widths, and geometry. Components use labels, placement, symbols,
and accessible descriptions so color is not the only cue. There is no flashing
or distracting animation, and responsive layouts preserve readable controls.

Future binding may use only source-labeled, freshness-aware normalized data.
Raw evidence remains authoritative, measured and calculated values remain
distinguishable, and unavailable or stale values are shown honestly. The
prototype's synthetic values are neither source records nor an integration
contract.

## Remaining Visual Question

Browser review must confirm whether the compact lower-center readout remains
clear at the existing four-card desktop size and responsive widths. Its exact
spacing may still be adjusted without changing the accepted fixed-scale marker
mapping or alarm priority.
