# On-Site Irradiance and Module-Temperature Measurement Plan

## Purpose and status

This future diagnostic plan addresses a central ambiguity: aggregate PV power
can fall because sunlight fell or because electrical, control, inverter,
microinverter, or communications behavior changed. It is not an active-capture
requirement, an approved purchase/build, or authorization for rooftop or
electrical work.

The preferred starting concept is plane-of-array irradiance measured at a
representative panel tilt and azimuth, synchronized to Solar Digital Twin UTC
chronology, with reference-cell or representative module temperature when
practical. Installation must be weather-resistant, safely accessible, and
non-invasive.

## Sensor assessment

Compare a calibrated PV reference cell with a thermopile pyranometer before
selecting hardware:

- required accuracy, response time, spectral/angular behavior, calibration,
  cost, maintenance, and defensibility;
- mounting at representative tilt/azimuth, shading, soiling, drainage,
  weatherproofing, sensor self-heating, and temperature response;
- whether multiple roof orientations require multiple sensors or a documented
  qualification;
- module/reference-cell temperature placement and attachment;
- sampling cadence sufficient to resolve the electrical events without
  creating unnecessary volume;
- UTC timestamp source, local raw logging, gaps, freshness, availability,
  source identity, and immutable provenance; and
- calibration or comparison checks before installation and periodically after.

Weather-station or airport cloud observations remain supporting context, not a
substitute for plane-of-array irradiance at the site.

## Interpretation boundary

- Concurrent irradiance and PV collapse supports an environmental explanation.
- Steady irradiance during PV collapse strengthens the case for electrical,
  control, inverter, microinverter, or communications behavior.
- Irradiance alone does not prove causation; timing, calibration, orientation,
  temperature, shading, soiling, and source gaps remain qualifications.

## Safety, build, and validation boundary

Apply the Engineering Bible's cost and custom diagnostic equipment decision
order. A custom design must preserve safe voltage/current limits, electrical
isolation where applicable, fused/protected inputs, suitable enclosures and
connectors, clear failure modes, reproducible calibration, safe installation
and removal, and no effect on inverter, microinverter, battery, grid, or
generator operation.

Do not use unsafe rooftop access or licensed/hazardous electrical work. Prefer
an accessible representative mounting location when it can produce defensible
measurements. Recommend certified commercial equipment or narrowly scoped
professional assistance when isolation, calibration, accuracy, safety, or
warranty evidence cannot be achieved practically with a custom device.

## Later expanded capture

After bench validation and a separate installation authorization, a later
coordinated capture may add irradiance and temperature as independent native
sources alongside EG4, SolarAssistant, ESP32, and validated HA telemetry. It
must record sensor identity, calibration, orientation, units, timestamps,
freshness, gaps, and provenance. It must preserve raw sensor evidence and must
not replace or rewrite existing evidence.
