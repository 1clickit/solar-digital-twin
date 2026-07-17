# Next Task

## Objective

Perform focused browser review of the completed synthetic Battery cell voltage
marker and avionics-style readout experiment.

## Scope

1. Confirm the short blue Min, white Avg, and red Max markers remain legible
   while naturally overlapping for closely balanced cells.
2. Confirm separation becomes useful as differential increases without adding
   artificial offsets or full-length needles.
3. Confirm the compact lower-center Min/Avg/Max and dynamic differential
   readout remains readable at desktop and responsive widths.
4. Confirm the red Max marker cannot be mistaken for the substantially larger
   under-voltage, over-voltage, or simultaneous-fault banners.
5. Preserve the fixed scale, red endpoints, caution regions, alarm priority,
   and actual abnormal values.

Do not connect the experiment to live data, evidence, collectors, APIs,
credentials, or an installed portal. Do not implement production alarms or
event logging.

## Operational boundaries

The configured ESP32 and SolarAssistant capture periods should have completed,
but completion and evidence integrity have not been verified. Until separately
approved read-only verification occurs, do not signal, attach to, restart,
redeploy, or modify either collector, its runtime, retention behavior, or
evidence. EG4 workflows remain unchanged. Repository work is allowed only when
it cannot affect protected runtime state or evidence outputs.

## Following operational work

Separately approved minimal read-only completion and evidence-integrity
verification remains required before detailed correlation, retention analysis,
monitor deployment, collector restart, or any evidence-dependent work. Preserve
the verification sequence and later ESP32 retention assessment in
`PROJECT_STATE.md` and `docs/ESP32_FORENSIC_TELEMETRY_PLAN.md`.

## Success

Chris can decide whether the marker and readout presentation is accepted or
needs one narrowly described visual adjustment without changing safety meaning.
