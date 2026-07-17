# Next Task

## Objective

Perform one bounded, synthetic-only Battery cell voltage visual experiment in
`prototypes/solar_portal_mockup.html` and its focused standard-library test.

## Scope

1. Preserve the fixed colored operating scale and red low/high endpoint limits.
2. Remove the ambiguous moving green progress ring.
3. Add three short tick or bug markers near the shared voltage scale instead of
   full-length center needles:
   - average: white;
   - highest: red;
   - lowest: blue.
4. Allow the markers to overlap when cells are closely balanced and separate
   visibly as differential increases.
5. Add a compact avionics-style digital readout below or within the lower
   center of each dial containing Min, average, Max, and dynamically calculated
   differential.
6. Treat the digital values as authoritative and the marker positions as fast
   approximate context. The differential is dynamic, not fixed at `13 mV`.
7. Preserve the existing normal, under-voltage, over-voltage, and simultaneous-
   fault structures and alarm-banner priority.
8. Keep exact Min/Avg/Max readout placement open for focused browser review if
   more than one layout remains viable.

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

The synthetic dials replace the ambiguous moving ring with readable shared-
scale markers and authoritative dynamic numeric values, focused tests and
repository checks pass, no live behavior is introduced, and the result is left
for browser review.
