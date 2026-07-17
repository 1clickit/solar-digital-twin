# Next Task

## Objective

Review and prepare the separately approved real-input phase for the bounded
offline EG4/SolarAssistant/ESP32 correlation analyzer. Do not run it on real
evidence during preparation.

## Context

The pure parsed-stream analyzer and 17 synthetic scenario tests are complete.
EG4 coverage is **Complete** for the full ESP32 overlap: 177 unique day-series
samples and 47 runtime snapshots, with no gap over 20 minutes and no malformed
overlap JSON. Timestamp semantics and the bounded analysis plan are recorded in
`docs/EG4_FORENSIC_CORRELATION.md`. The exact protected SolarAssistant raw
filename remains intentionally unresolved by the unprivileged planning work
unit.

## Scope

1. Review the implemented synthetic analyzer interface, thresholds, alignment
   tolerances, source roles, and confidence limitations before real use.
2. Define explicit bounded-memory adapters for the selected EG4 SQLite rows and
   SolarAssistant/ESP32 NDJSON without opening operational inputs in this
   preparation step.
3. Resolve only the SolarAssistant raw filename and access method through a
   separately approved metadata-only action without reading credentials or
   changing permissions.
4. Require separate approval before implementing or running adapters against
   protected SolarAssistant evidence and the completed real datasets.
5. Keep generated output in `/tmp` or ignored reports. Do not modify evidence,
   production retention, collectors, databases, services, or runtime state.

## Following task

After the bounded real analysis is reviewed, use its known event windows to
validate whether the conservative ESP32 retention candidate preserves dropout,
recovery, plateau, frequency, binary-event, and availability evidence.

## Monitor boundary

The SolarAssistant monitor remains running and healthy but stale after capture
completion. Its abort-control token requires rotation through a separately
approved restart before any future abort-capable capture. Do not restart or
deploy the monitor during correlation implementation or analysis.

## Success

The synthetic analyzer remains validated and offline-only; the reviewed next
work request defines exact adapters, protected access, output destination, and
real-run limits without weakening permissions. Real execution remains a
separate explicit approval, and all evidence and runtime state remain unchanged.
