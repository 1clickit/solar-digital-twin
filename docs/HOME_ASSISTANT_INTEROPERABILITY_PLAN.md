# Home Assistant Telemetry Interoperability Plan

## Status and boundary

This remains a future design plan. The coordinated capture is intentionally
closed with successful restoration; its immutable inventory, integrity review,
and first three-source analysis remain active. No Home Assistant connection,
credential, collector, export, device query, network change, broker migration,
or control action is approved by this document.

The initial architecture is reciprocal **read-only telemetry exchange** on the
trusted LAN. It is not an equipment-control interface. Home Assistant remains a
complementary display and telemetry source; Solar Digital Twin preserves source
identity, evidence, provenance, and engineering authority.

## Verified discovery checkpoint

- Home Assistant is a separate VM on the same Proxmox host as `solardt`, with
  static IPv4 `192.168.3.15/24`, gateway/DNS `192.168.3.1`, and IPv6 disabled.
  Its malformed prior static profile was repaired via temporary DHCP before
  assigning `.15`. `solardt` is `.11`, SolarAssistant `.12`, and the ESP32
  forensic logger `.13`. Reverify HA versions before compatibility-sensitive
  work.
- SolarAssistant connects directly to both JK BMS units through RS-485, not to
  the EG4 inverter, and remains trusted battery authority.
- HA MQTT was corrected from stale broker `.231` to SolarAssistant
  `192.168.3.12:1883`. It remains MQTT 3.1.1 because the broker did not support
  the requested MQTT 5 migration. The HA Mosquitto add-on was installed, but
  `.15:1883` was closed at discovery and it was not the active LAN broker.
- EG4 Web Monitor was functioning with approximately 3 devices and 115
  entities. It used the EG4 cloud account and `Manage Local Devices` showed
  none. Its path is `inverter -> EG4 cloud -> EG4 Web Monitor -> HA`,
  overlapping the solardt cloud source rather than adding independent physical
  evidence. Its writable entities remain unauthorized.
- HA directly integrates `EG4 Forensic Probe v3` at `.13`, with approximately
  21 entities. An older frequency dashboard contains stale/missing references.
  Do not remove it until firmware/API reboot behavior and the preferred `ESP32
  -> solardt -> selected read-only HA exports` path are proven.
- The existing EG4 dongle was observed at `192.168.3.20:8000`, MAC
  `d8:3b:da:21:92:c8`. It remains attached and may continue cloud reporting.
  The prepared path is `dongle -> solardt -> selected read-only HA exports`,
  not direct HA polling. See `docs/EG4_LOCAL_DONGLE_INVESTIGATION.md`.

Device/entity counts are observations, not invariants. MQTT architecture
remains open; migration requires rollback and circular-ingestion protection.

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

The proposed transport-neutral normative envelope and cycle-rejection rules are
centralized in `TELEMETRY_OBSERVATION_CONTRACT.md`, pending independent review
and owner acceptance. This plan does not select or implement a transport.

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

`joyfulhouse/eg4_web_monitor` is installed and currently provides cloud data;
it is not an authoritative independent forensic source. Public-source local
dongle research is recorded separately. Before any local pilot, assess:

- compatibility with Chris's exact Home Assistant release, EG4 model,
  firmware, and existing communications topology;
- installation/update/maintenance model and local versus cloud modes;
- polling cadence, entity inventory, register identities, scaling, timestamps,
  availability, and direct versus calculated values;
- fault, warning, frequency, power, operating-state, and AC-couple/GEN-terminal
  coverage, including limitations separating that power from other loads;
- unavailable entities, update regressions, disconnect recovery, and gaps; and
- agreement and latency versus EG4 cloud and SolarAssistant observations.

Prefer a purpose-built, technically read-only solardt assessment rather than
adding the dongle as a second HA poller, if later owner review supports it.

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

## Remaining questions before implementation

- What exact Home Assistant version is current at compatibility review time?
- What exact EG4 inverter/dongle firmware and serial identifiers apply?
- Can the dongle's single TCP slot coexist safely with cloud traffic?
- Which HA entities should remain after the future solardt export is proven?
- Should HA Mosquitto later become primary, and what bridge/rollback design
  prevents circular SolarAssistant and solardt ingestion?
- Which Solar Digital Twin metrics should HA display, and at what acceptable
  update cadence?
- What roof-array orientations and safe irradiance-sensor mounting locations
  are available?

Do not infer answers from old configuration or entity names.

## Future work sequence

1. Preserve, inventory, hash, and validate the closed coordinated capture.
2. Perform the first three-source analysis.
3. Review the prepared HA/MQTT/dongle discovery and reverify versions.
4. If justified, authorize one minimal read-only dongle transaction under
   `docs/EG4_LOCAL_DONGLE_INVESTIGATION.md`.
5. Validate local dongle telemetry against established cloud evidence.
6. Validate HA-provided EG4 telemetry against established sources.
7. Design and validate Solar Digital Twin's read-only HA export.
8. Design and validate on-site irradiance and temperature logging under
   `docs/IRRADIANCE_MEASUREMENT_PLAN.md`.
9. Run a separately authorized expanded coordinated capture.
10. Decide whether any added source is suitable for production retention or
    forensic reliance.

The expanded capture must preserve native provenance and UTC chronology and
must not count a feedback copy as independent evidence.
