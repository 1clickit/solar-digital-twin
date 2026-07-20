# Next Task

## Objective

Review the completed coordinated three-source findings with Chris and decide
whether the evidence is sufficient or one narrowly targeted follow-up
measurement is justified. Do not activate a capture or measurement during the
review.

## Context

The authoritative result is `docs/COORDINATED_CAPTURE_CORRELATION.md`, with the
compact event/control table at
`docs/capture_analyses/solar-forensic-20260718T062127Z-events.tsv` and the
detailed battery review at
`docs/capture_analyses/solar-forensic-20260718T062127Z-battery-cell-review.md`.

The primary detector found five zero-output and two partial-collapse events.
ESP32 power corroborates real aggregate AC-couple loss/rejoin, but ordinary
controls show the same small frequency excursions and rolling frequency-event
text. No availability transition occurred. Two events have larger near-anchor
voltage excursions. Trusted battery context makes charge/SOC constraints
plausible for several events but not sufficient to explain all of them.

The follow-up cell review found only small event-anchor imbalance and no
positive JK overvoltage-protection signature. Because SolarAssistant did not
export MOS/protection state, an unobserved transient cannot be absolutely
excluded, but JK BMS protection is poorly supported for any event and is not a
supported common explanation for all seven.

The remaining investigation centers on EG4 AC-couple control, microinverter
response, independent irradiance, or a sub-second AC disturbance. The evidence
cannot distinguish these possibilities or identify an individual
microinverter. Correlation does not establish causation.

## Scope

1. Review the seven event summaries, three controls, fixed sensitivity result,
   evidence limitations, and owner questions.
2. Decide whether the result is already sufficient for the next owner decision.
3. If more evidence is necessary, select only one smallest useful next step:
   a targeted synchronized capture that adds an independent discriminator, a
   separately gated local-dongle one-shot measurement only if it exposes useful
   new control state safely, or no additional measurement.
4. Keep Home Assistant, MQTT, policy promotion/retirement, and unrelated portal
   work outside this decision.

## Runtime boundary

This is an owner-review task. It authorizes no device query, LAN request,
credential access, service/runtime action, capture, firmware/configuration
change, local-dongle contact, or physical-system manipulation.

## Success

Chris receives the evidence-backed conclusion and uncertainties, and explicitly
chooses whether the evidence is sufficient or which single targeted measurement
is justified. Any selected operational step receives a new bounded work unit.

## Deferred Post-Project Investigations

Investigate low-load inverter fan control using additional instrumentation
capable of measuring fan command, RPM, PWM/duty, electrical current, or
synchronized acoustic evidence. Begin only after completion of the primary
Solar Digital Twin milestones. Preserve the July 19, 2026 cooling-control
capture as baseline evidence. Do not infer fan operation from radiator
temperature alone.
