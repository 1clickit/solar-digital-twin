# Next Task

## Objective

Compare raw and current-retained ESP32 context against the conservative
retention candidate using validated real event windows. Do not change evidence
or production retention behavior.

## Context

The initial `solardt` VM health baseline is recorded in
`docs/operations/VM_HEALTH_LOG.md` and classified **Normal**. Root filesystem
use is 17%, inode use is 4%, memory availability is healthy, load is negligible,
systemd reports no failed units, and capacity is sufficient for this bounded
offline analysis. Swap use and evidence growth should be compared at later
health reviews but do not block the current task.

The real-evidence dry run validated the read-only adapters and analyzer against
the completed overlapping EG4, SolarAssistant, and ESP32 captures. It found
bounded partial-collapse and zero-output candidates, verified compatible UTC
alignment, preserved trusted SolarAssistant SOC versus estimated EG4 SOC, and
left all source evidence unchanged.

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
