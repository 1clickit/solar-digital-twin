# Next Task

## Objective

Implement and synthetically test the bounded offline
EG4/SolarAssistant/ESP32 correlation analyzer. Run it on the completed real
datasets only after the protected SolarAssistant raw filename and evidence
access are separately approved.

## Context

EG4 coverage is **Complete** for the full ESP32 overlap: 177 unique day-series
samples and 47 runtime snapshots, with no gap over 20 minutes and no malformed
overlap JSON. Timestamp semantics and the bounded analysis plan are recorded in
`docs/EG4_FORENSIC_CORRELATION.md`. The exact protected SolarAssistant raw
filename remains intentionally unresolved by the unprivileged planning work
unit.

## Scope

1. Add a repository-local offline analyzer with synthetic tests for alignment,
   missing sources, offsets, abrupt steps, non-zero plateaus, recovery, gradual
   cloud-like ramps, availability transitions, and no-event controls.
2. Open EG4 SQLite read-only and stream SolarAssistant and ESP32 NDJSON with
   bounded memory; preserve source identity, native samples, and timestamp
   provenance.
3. Resolve only the SolarAssistant raw filename and access method through a
   separately approved metadata-only action without reading credentials or
   changing permissions.
4. Require separate approval before running against protected SolarAssistant
   evidence and the completed real datasets.
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

The analyzer passes synthetic validation, protected input resolution and real
execution remain separately approved, output is reproducible and source-
labeled, and all evidence and runtime state remain unchanged.
