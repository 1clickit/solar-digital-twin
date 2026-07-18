# Next Task

## Objective

Monitor, complete, preserve, and analyze the coordinated approximately 24-hour
ESP32, EG4, and SolarAssistant forensic capture. Verify automatic termination
and exact prior-service restoration before offline analysis.

## Context

Chris authorized one common 24-hour interval in place of the earlier 12-hour
ESP32-only canary. `docs/COORDINATED_FORENSIC_CAPTURE.md` defines isolated
native outputs, append-only common provenance, competing-writer handling,
automatic stop/restoration, monitoring, and evidence-preservation boundaries.
The current ESP32 policy remains the production default.

## Scope

1. Use compact read-only status checks; do not stream or rewrite evidence.
2. At terminal state, verify each source's completion, prior-unit restoration,
   metadata, hashes, parse integrity, cadence, gaps, and source errors.
3. Preserve all complete or partial evidence and append-only manifests.
4. Perform bounded offline correlation across the common UTC window and compare
   raw/current/conservative ESP32 context.
5. State source gaps, alternative explanations, and confidence without claiming
   causation or retiring `esp32-frequency-v1`.

## Runtime boundary

Use strict read-only, bounded offline access. Do not access credentials,
tokens, protected collector or monitor logs, device controls, services, or
unrelated files. Do not restart or modify the SolarAssistant monitor, EG4
workflow, installed ESP32 collector, evidence, database, permissions, or
runtime. Repository source changes remain limited to the implementation scope.

## Following task

After evidence analysis, decide whether another capture or a narrowly targeted
measurement is needed. Policy retirement remains a later owner-reviewed
decision after every production acceptance gate passes.

## Success

The capture ends cleanly, prior units are restored exactly, immutable source
evidence and hashes are preserved, correlation findings are reproducible, and
uncertainty is explicit.
