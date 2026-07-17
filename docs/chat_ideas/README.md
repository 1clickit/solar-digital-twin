# Portal Chat Ideas

## Purpose and authority

This is a non-authoritative holding area for ideas from design discussion. It
does not approve implementation, replace `docs/PORTAL_UI_DESIGN.md`, or add an
Engineering Bible decision. When an idea is accepted, the authoritative
document records the decision and this file links to it rather than duplicating
the full design.

Status legend:

- **Accepted direction** — promoted to an authoritative design document.
- **Open question** — more review or evidence is needed.
- **Deferred** — potentially useful, but not current work.
- **Superseded** — considered and replaced, with the reasoning retained.
- **Implemented in synthetic prototype** — visible offline, not operational.

## Future and open ideas

### Interchangeable portal skins — Deferred

Possible skins include the current modern circular style, a large-aircraft
engine-MFD or avionics style, and a compact technical style. Skins may change
rendering and layout only. They must not change metric identity, units, source
identity, thresholds, alarm meaning, freshness, provenance, accessibility, or
safety logic.

An avionics MFD skin may suit a full-screen operations display, wall-mounted
monitor, dense battery/inverter detail page, or alternate user-selectable mode.

### Battery temperature card — Deferred

A future homepage card may use two circles, one for each battery temperature.

### Complete source schema inventory — Deferred

Perform a read-only inventory of complete SolarAssistant and EG4 parsed source
responses only after current capture completion and evidence integrity are
handled. The accepted completeness rule is in
[`docs/PORTAL_UI_DESIGN.md`](../PORTAL_UI_DESIGN.md#complete-source-data-tabs).

### Cell-voltage Min/Max labels — Open question

Determine through browser review whether Min and Max numeric labels should
always remain visible or become conditional when differential is `10 mV` or
less. No threshold behavior is accepted by this note.

### Historical metric views — Deferred

Stable metric URLs or pages may provide selectable time ranges, Min/Max/average,
last-change time, missing-data periods, source identity, freshness, provenance,
compatible comparisons, and related events. The accepted direction is recorded
in [`docs/PORTAL_UI_DESIGN.md`](../PORTAL_UI_DESIGN.md#metric-history).

### Hosting separation — Deferred

Initial production hosting remains on `solardt`. A separate VM, LXC, or
frontend host should be reconsidered only for exposure, reverse-proxy/DMZ
requirements, resource contention, independent availability, or a shared web-
services platform.

### ESP32 security hardening — Deferred

After current evidence work is complete, consider protected OTA, encrypted
ESPHome API, protected web/SSE access, secrets outside source and logs, and
later network restrictions.

## Superseded visual approaches

- **Full moving green inner Battery cell voltage ring** — superseded because it
  resembles simultaneous occupancy of many voltages.
- **Full-length center needles** — superseded for the next experiment by short
  scale-adjacent tick or bug markers.
- **Hundreds of five-minute Volcast rows on Overview** — superseded by a compact
  forecast card and complete source-data view.
- **Long provenance and calculation explanations beneath homepage dials** —
  superseded by curated Overview cards and dedicated traceability/source views.
- **Treating `Sum` as average cell voltage** — rejected because these are not
  interchangeable measurements.

## Current synthetic checkpoint

The modern circular prototype, tab navigation, source-data layouts, and current
cell-voltage alarm structures are **Implemented in synthetic prototype**. Their
accepted design meaning is recorded in `docs/PORTAL_UI_DESIGN.md`; synthetic
implementation does not imply live deployment.
