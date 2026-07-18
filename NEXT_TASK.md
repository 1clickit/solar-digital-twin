# Next Task

## Objective

Perform a bounded offline comparison of the current ESP32 retained evidence
and the documented conservative retention candidate against the validated real
three-source event windows. Do not change production retention behavior.

## Context

The real-evidence dry run validated the read-only adapters and analyzer against
the completed overlapping EG4, SolarAssistant, and ESP32 captures. It found
bounded partial-collapse and zero-output candidates, verified compatible UTC
alignment, preserved trusted SolarAssistant SOC versus estimated EG4 SOC, and
left all source evidence unchanged. Commit `b88941d` contains the validated
compatibility corrections and is synchronized with `origin/main`.

Trusted read-only SolarAssistant telemetry analysis is now permitted through
the established least-privilege read model without repeated administrator
intervention. Credentials, tokens, protected logs, unrelated runtime files,
and write access remain outside that authority.

## Scope

1. Use only the already identified bounded real event and control windows.
2. Replay the documented conservative ESP32 retention candidate offline without
   modifying either raw or retained evidence.
3. Compare raw, current retained, and conservative-candidate context for event
   timing, plateau, recovery, frequency, binary events, availability, and
   confidence classification.
4. Quantify record and byte reduction for the bounded windows and state any
   forensic information lost or changed.
5. Preserve cloud cover and ordinary variability as alternative explanations;
   do not claim causation.
6. Recommend either keeping current retention or a separately reviewed bounded
   policy implementation. Do not deploy or recapture during this work unit.

## Runtime boundary

Use strict read-only, bounded offline access. Do not access credentials,
tokens, protected collector or monitor logs, device controls, services, or
unrelated files. Do not restart or modify the SolarAssistant monitor, EG4
workflow, ESP32 collector, evidence, database, permissions, or runtime.

## Following task

After retention equivalence is reviewed, prepare the smallest defensible
three-source forensic report of the validated candidate windows, including
provenance, limitations, confidence factors, and the narrowest useful next
physical or professional measurement if telemetry remains inconclusive.

## Success

The comparison is reproducible, bounded, evidence-preserving, and clear about
what the smaller candidate retains or loses. Any production policy change
remains a separate risk-classified operation.
