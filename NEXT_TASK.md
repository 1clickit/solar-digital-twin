# Next Task

## Objective

Define and implement the smallest safe foundation for persistent,
multi-rate telemetry collection before portal or systemd integration.

## Scope

- harden persistent SolarAssistant collection
- define configurable observation and retention intervals
- suppress routine duplicate history while preserving freshness
- define ESP32 one-second forensic retention behavior
- document evidence rotation, credentials, recovery, and error visibility
- defer portal, SQLite schema, and systemd integration

## Agreed Design

- Use a persistent SolarAssistant collector.
- Poll the complete authenticated read-only metrics endpoint every 10 seconds.
- Apply topic-specific retention locally; separate intervals do not reduce API traffic.
- Keep SolarAssistant/JK BMS as the trusted battery source.
- Keep EG4 SOC as a separate inverter-reported comparison estimate.
- Do not apply a fixed correction to EG4 SOC.
- Update current-state freshness after every successful observation.
- Insert history only for meaningful changes, required heartbeats,
  availability transitions, and diagnostic-event overrides.
- Preserve source, last-observed time, and last-changed time separately.
- Keep portal and long-term archive design outside the first implementation.

## Initial Retention Policy

- Load power and battery voltage/current/power: observe every 10 seconds;
  retain changes plus a 60-second heartbeat.
- Battery 1, Battery 2, and combined SOC: retain changes plus a
  5-minute heartbeat.
- Cell voltage, imbalance, and temperatures: observe every 60 seconds;
  retain meaningful changes plus a 5-minute heartbeat.
- Health, capacity, and cycle count: observe every 15 minutes;
  retain changes plus a daily heartbeat.
- ESP32 AC-couple and electrical telemetry: observe at one-second cadence.
- ESP32 frequency: retain changes of at least 0.04 Hz plus a
  30-second heartbeat during active solar operation.
- Significant events may preserve complete one-second pre-event,
  event, and post-event samples, including duplicates.

## Event Interpretation

Field observation indicates that the EG4 appears to switch AC-coupled
microinverters on and off rather than continuously ramping them.

Primary event signatures are:

- abrupt AC-couple power steps
- reduced-output plateaus
- active-microinverter count changes
- later step recovery

Ramp rate remains useful supporting evidence but is not required for
event detection.

## Implementation Boundary

First harden standalone collection for:

- evidence rotation and retention
- protected credential handling
- single-instance operation
- last-observed and last-changed timestamps
- controlled retry and restart behavior
- visible collector and storage errors
- configurable telemetry intervals and change thresholds

Do not add portal, SQLite schema, or systemd integration until the
standalone design and implementation boundary are reviewed.


## Recovery Safeguards

- Keep validated source code and documentation committed and pushed to GitHub.
- Create and verify a dated Git bundle after important milestones.
- Copy recovery files off the solardt VM to protect against VM or disk failure.
- Back up databases, evidence, reports, credentials, and systemd configuration
  separately using encrypted storage.
- Test restoration periodically rather than assuming a backup is usable.
- Treat Repomix output as a temporary architecture-review snapshot, not as
  authoritative memory or a recovery backup.

## Success

The operating and retention policy is documented, configurable,
testable, and ready for one small standalone implementation step.
