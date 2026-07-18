# Home Assistant Telemetry Interoperability Plan

## Status and boundary

This is a future assessment and design plan. The current coordinated capture,
its completion review, evidence inventory, and first three-source analysis
remain the active work. No Home Assistant installation, connection, credential,
collector, export, device query, network change, or control action is approved
by this document.

The initial architecture is reciprocal **read-only telemetry exchange** on the
trusted LAN. It is not an equipment-control interface. Home Assistant remains a
complementary display and telemetry source; Solar Digital Twin preserves source
identity, evidence, provenance, and engineering authority.

## Direction A — Solar Digital Twin reads Home Assistant

`solardt` may later consume an explicit allowlist of Home Assistant entities,
including validated local EG4 entities. The bounded assessment must define:

- initial state snapshot, appropriate live change/event delivery, and periodic
  reconciliation or heartbeat;
- source and receipt timestamps, availability, cadence, units, scaling, stable
  entity/metric identifiers, freshness, and stale-data behavior;
- original source identity and whether each value is direct, calculated,
  rounded, aggregated, or normalized by Home Assistant;
- reconnect, gap, timeout, bounded-retry, rate-limit, local-buffering, and
  evidence-preservation behavior; and
- strict input allowlists and malformed/unavailable-value handling.

REST, Home Assistant event-stream/WebSocket, and MQTT-style transports are
candidates to assess. None is selected here. Selection must account for
timestamp semantics, replay/reconciliation, operational burden, security, and
whether MQTT is already available.

## Direction B — Home Assistant reads Solar Digital Twin

A later stable, LAN-only, read-only export may expose selected portal-safe
summaries such as collector health/freshness, trusted battery metrics, EG4
comparison metrics, ESP32 frequency/availability, AC-couple assessment,
coordinated-capture status, and derived diagnostic/event status.

The versioned metric schema must include:

- unique identifier and human-readable name;
- value and unit;
- source and origin;
- observed timestamp and changed timestamp where applicable;
- freshness and availability;
- quality or confidence classification; and
- schema version.

Home Assistant must not represent a derived Solar Digital Twin value as a
direct inverter register unless provenance explicitly establishes that fact.
The export must not expose credentials, tokens, authorization headers,
protected configuration, writable controls, shell/command execution, arbitrary
files, database mutation, evidence modification, unsafe diagnostics, or
unrestricted evidence directories.

## Lineage and feedback-loop protection

Bidirectional exchange must not turn one observation into apparently
independent corroboration. Every imported or exported metric requires source
lineage, an origin identifier, transformation identifiers, and an
observed/normalized/derived classification. Use explicit import and export
allowlists, deduplicate where necessary, and never re-export imported data
under a misleading source identity.

An HA value originally sourced from EG4 or SolarAssistant and then read by
Solar Digital Twin remains that source's observation through every derived
copy. If HA later reads a Solar Digital Twin export, that exported value must
not be ingested again as new evidence or counted twice when assigning
confidence.

## Security model

- LAN-only initially; no unsolicited WAN exposure.
- Dedicated service identities and the least practical privilege.
- Credentials remain outside Git, documentation, command arguments, reports,
  ordinary logs, and ordinary backups.
- Explicit entity/metric allowlists, bounded rates, timeouts, retries, and
  reviewable behavior.
- No control-capable endpoint in the initial Solar Digital Twin export.
- No weakening of existing credential ownership or permissions.

If Home Assistant authentication cannot be technically read-only, use a
dedicated minimally privileged identity, strict allowlists, no control calls,
and focused validation. Record that effective-authority limitation explicitly.

## `joyfulhouse/eg4_web_monitor` candidate pilot

`joyfulhouse/eg4_web_monitor` is the leading candidate for a controlled local
EG4 telemetry pilot in Home Assistant. It is not approved for installation and
is not an authoritative forensic source. Before any pilot, assess:

- compatibility with Chris's exact Home Assistant release, EG4 model,
  firmware, and existing communications topology;
- installation/update/maintenance model and local versus cloud modes;
- polling cadence, entity inventory, register identities, scaling, timestamps,
  availability, and direct versus calculated values;
- fault, warning, frequency, power, operating-state, and AC-couple/GEN-terminal
  coverage, including limitations separating that power from other loads;
- unavailable entities, update regressions, disconnect recovery, and gaps; and
- agreement and latency versus EG4 cloud and SolarAssistant observations.

Prefer an initial local-only assessment without additional EG4 cloud
credentials if the topology review supports it.

The integration can expose writable inverter controls. Hiding or disabling
writable entities does not make its underlying implementation intrinsically
read-only. No control automation or write operation is authorized for this
pilot. Treat it as control-capable software constrained by an explicit
read-only policy. Any later control use requires a separate owner decision and
bounded authorization.

## EG4 RS-485 and communications topology review

Before adding any new direct poller, document:

- exact EG4 model/firmware and every physical port in use;
- stock dongle, SolarAssistant, Home Assistant, USB/serial, Ethernet,
  Bluetooth, cloud, and gateway paths;
- RS-485 wiring, termination, protocol, baud, and master/slave or
  client/server roles;
- whether multiple active pollers would share a bus and whether the existing
  HA integration is its sole owner; and
- safe local-data options without collisions or disruption.

Do not connect or enable a second active RS-485 master until topology and bus
ownership are proven. Later options may include Home Assistant as sole reader
with normalized export, one shared read-only gateway, a purpose-built Solar
Digital Twin collector, or passive observation if electrically and technically
justified. Do not select among them before inspection.

## Questions for Chris before implementation

- What Home Assistant version and host are current?
- Is `joyfulhouse/eg4_web_monitor` installed, disabled, or removed, and how was
  it previously configured?
- Which EG4 entities exist in HA, and what currently sources each one?
- How does SolarAssistant currently connect to HA?
- What exact EG4 ports and communications wiring are in use?
- What is the stock dongle state, and is any USB/RS-485 adapter present?
- Is MQTT currently available?
- Which Solar Digital Twin metrics should HA display, and at what acceptable
  update cadence?
- What roof-array orientations and safe irradiance-sensor mounting locations
  are available?

Do not infer answers from old configuration or entity names.

## Future work sequence

1. Complete and verify the active coordinated capture.
2. Preserve and inventory its evidence.
3. Perform the first three-source analysis.
4. Inventory Home Assistant, entities, versions, and communications topology.
5. Assess `joyfulhouse/eg4_web_monitor` in a bounded non-production pilot.
6. Validate HA-provided EG4 telemetry against established sources.
7. Design and validate Solar Digital Twin's read-only HA export.
8. Design and validate on-site irradiance and temperature logging under
   `docs/IRRADIANCE_MEASUREMENT_PLAN.md`.
9. Run a separately authorized expanded coordinated capture.
10. Decide whether any added source is suitable for production retention or
    forensic reliance.

The expanded capture must preserve native provenance and UTC chronology and
must not count a feedback copy as independent evidence.
