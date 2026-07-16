# Next Task

## Objective

Perform an offline, read-only characterization of existing SolarAssistant raw
NDJSON evidence and propose defensible numeric deadbands for voltage, current,
power, cell-voltage, cell-imbalance, and temperature topic families.

## Context

Commit `4e069bb` added the separate retained NDJSON stream and implemented all
currently approved exact-change policies. Raw evidence remains complete and
authoritative. The six meaningful-change families remain deliberately raw-only
because no numeric deadbands are approved.

## Scope

- Use only existing local raw SolarAssistant NDJSON evidence.
- Measure observable value resolution, repeated-value behavior, normal short-term variation, and apparent noise or jitter by topic family.
- Assess voltage, current, power, cell voltage, cell imbalance, and temperature separately by unit and metric family.
- Consider whether combined, Battery 1, and Battery 2 measurements need the same or different thresholds.
- Distinguish sensor or display resolution from a recommended meaningful-change threshold.
- Preserve planned heartbeats: 60 seconds for voltage, current, and power; 5 minutes for cell voltage, imbalance, and temperatures.
- Produce candidate deadbands with plain-language reasoning and compact representative statistical summaries.
- Keep policy source-specific and reusable mechanics source-independent for future collectors and sensors.

## Boundaries

- Read evidence without rewriting, migrating, renaming, or deleting it.
- Do not contact devices, authenticate, access credentials, or expose large raw extracts or unrelated private telemetry.
- Do not implement or approve a deadband during assessment; project-owner approval is required afterward.
- If evidence is insufficient, state the limitation and minimum additional evidence needed instead of inventing a threshold.
- Keep SQLite, portal, systemd, credentials, persistent services, and live verification deferred.

## Success

The assessment produces defensible candidate deadbands or a precise evidence-
insufficiency finding for each family, without modifying evidence or code, and
leaves every candidate pending explicit project-owner approval.
