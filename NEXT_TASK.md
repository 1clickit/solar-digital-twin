# Next Task

## Objective

Review the synthetic input adapters and prepare an exact, separately approved
metadata-only SolarAssistant evidence inventory. Do not inspect metadata or run
the analyzer on real evidence without that approval.

## Context

The pure parsed-stream analyzer and synthetic input adapters are complete.
EG4 coverage is **Complete** for the full ESP32 overlap: 177 unique day-series
samples and 47 runtime snapshots, with no gap over 20 minutes and no malformed
overlap JSON. Timestamp semantics and the bounded analysis plan are recorded in
`docs/EG4_FORENSIC_CORRELATION.md`. The exact protected SolarAssistant raw
filename remains intentionally unresolved by the unprivileged planning work
unit.

## Scope

1. Review the implemented adapter schema, timestamp mappings, bounded-window
   workflow, and analyzer thresholds before real use.
2. Define the exact administrator-run metadata fields and named-file scope from
   the procedure in `docs/EG4_FORENSIC_CORRELATION.md`.
3. Require separate approval before obtaining protected filename, ownership,
   permission, size, modification-time, capture-window, and completion metadata.
4. Review those results before separately approving any source hash, controlled
   read-only copy, analysis read, real execution, report, or cleanup action.
5. Keep credentials, tokens, unrelated files, production runtime, evidence,
   databases, and permissions unchanged.

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

The reviewed work request is limited to exact metadata fields and one named
protected capture. It contains no secret retrieval, recursive inspection,
permission change, monitor restart, or real analysis. Every later access stage
remains separately approved.
