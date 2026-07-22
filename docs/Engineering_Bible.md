# Solar Digital Twin Engineering Bible

**Version:** 0.2
**Status:** Living Document

## Primary engineering mission

Solar Digital Twin is not primarily a dashboard project. Its immediate mission
is to produce trustworthy, reproducible evidence that helps determine whether
the observed AC-coupled solar-production problem is caused by EG4 inverter
failure, unsuitable or defective EG4 AC-coupling behavior, configuration or
control behavior, Chilicon microinverter behavior, frequency or grid-forming
interaction, communications or data limitations, or another identifiable
system condition.

The practical target is defensible, reproducible evidence strong enough for an
informed decision; telemetry alone may not provide overwhelming proof. The
project should help Chris decide whether to continue with the current system,
correct a configuration or targeted defect, pursue warranty or manufacturer
escalation, obtain one narrowly scoped professional measurement, convert some
or all production to DC coupling, replace a specific component, or stop
investing in a path that evidence shows is unlikely to succeed.

The portal, collectors, evidence store, reports, correlation analyzer, and
future automation serve this mission. They may become more broadly useful, but
software expansion must not obscure the original problem. When professional
electrical testing is necessary, identify the narrowest useful test rather
than recommending open-ended expensive troubleshooting.

The accepted semantic direction for abrupt daytime production-collapse cases,
episode/recovery tracking, multi-source context, and cautious competing-
hypothesis handling is centralized in
`docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md`. That plan does not itself
authorize implementation or operational access.

## Primary User and Intended Use

Chris is the primary user, project owner, and system operator. The dedicated
local portal is the intended primary engineering interface for normal system
awareness, historical review, and evidence-based forensic investigation.
Home Assistant may later provide complementary convenience, status, and alerts,
but it is not an authoritative data store.

Future Home Assistant interoperability begins as allowlisted, LAN-only,
reciprocal read-only telemetry. Source lineage must prevent circular imports or
copied values from being counted as independent evidence, and control-capable
integrations remain constrained by separate authorization. See
`docs/HOME_ASSISTANT_INTEROPERABILITY_PLAN.md`. The canonical
observation and provenance semantics are centralized in
`docs/TELEMETRY_OBSERVATION_CONTRACT.md`, accepted by the project owner after
final independent review. The owner-accepted authoritative implementation
mapping and first synthetic-only slice are centralized in
`docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md`. Its acceptance does not authorize
implementation automatically.

## Operational Completion Baseline

The project reaches an operationally complete baseline when it provides a
trustworthy normal-operation view, freshness awareness, source-labeled
historical records, reproducible reports, and evidence-based forensic event
correlation. Automatic equipment control is not required. Further integrations
may continue after this baseline.

## Guiding Principles

- Raw evidence files are the authoritative source material.
- Never overwrite historical evidence.
- SQLite is the normalized engineering history and query layer.
- Reports, the portal, Home Assistant, and future APIs are derived consumers.
- Optimize only after measurement.
- Prefer simple architectures until complexity is justified.

## Cost and practical discipline

Chris is working within meaningful fixed-income and cash-flow constraints.
Prioritize existing equipment, available telemetry, low-cost diagnostics,
reversible changes, preserved evidence, and targeted professional help only
where necessary. Establish clear decision thresholds before major spending.
Do not recommend replacing equipment merely to exchange one poorly understood
problem for another. Recommend major purchases or architecture replacement
only when evidence shows lower-cost paths are unlikely to produce a reliable
result.

### Custom Diagnostic Equipment Capability

Chris is able and willing to build and install purpose-designed testing or
measuring equipment when ChatGPT can provide the technical design, component
guidance, firmware, software, and validation procedure.

This materially expands the project's available diagnostic options.

When additional measurements are needed, the ChatGPT project lead should
consider, in this order:

1. Existing equipment and telemetry already available.
2. A safe, practical device Chris can build and install.
3. Modification or extension of an existing ESP32, sensor, logger, or test
   fixture.
4. Purchase of a commercial tool or instrument.
5. Narrowly targeted professional testing when necessary.

Purchasing tools online is not Chris's preferred first option. However,
ChatGPT should recommend purchasing an appropriate instrument when:

- the required device cannot be built safely or practically;
- certified electrical isolation or protection is required;
- calibration or measurement accuracy cannot be established adequately;
- a commercial tool would be more reliable or less expensive than a custom
  build;
- building the device would create unacceptable electrical, fire, equipment,
  or personal-safety risk;
- the measurement must be defensible for warranty, manufacturer escalation,
  insurance, or professional diagnosis; or
- a custom device would delay the investigation without providing meaningful
  additional value.

Do not avoid recommending a purchase merely because Chris is capable of
building hardware. Explain:

- what the instrument would measure;
- why the measurement matters;
- why a custom device is or is not appropriate;
- the minimum required specifications; and
- how the result would change the project's next decision.

Custom diagnostic designs should prioritize:

- electrical isolation;
- safe voltage and current limits;
- fused and protected inputs;
- appropriate enclosures and connectors;
- non-invasive measurement where practical;
- UTC-synchronized timestamps;
- raw-data preservation;
- reproducible calibration or comparison checks;
- clear failure modes;
- safe installation and removal; and
- no unintended effect on inverter, microinverter, battery, grid, or generator
  operation.

ChatGPT should treat Chris as capable of assembling, wiring, installing,
testing, and troubleshooting purpose-built diagnostic hardware when provided
with clear instructions. This capability should be used to reduce unnecessary
expense while never substituting improvised equipment for required safety,
isolation, accuracy, or professional electrical work.

On-site plane-of-array irradiance and module/reference-cell temperature are
future diagnostic options for separating environmental variation from system
behavior. They must use UTC chronology, raw provenance, reproducible
calibration, safe installation, and cautious non-causal interpretation as
defined in `docs/IRRADIANCE_MEASUREMENT_PLAN.md`.

## Current Architecture

```
Proxmox VE
├── Home Assistant OS
└── Ubuntu Server (solardt)
      └── Solar Digital Twin
            ├── EG4 Collector
            ├── SolarAssistant NDJSON Collector
            ├── ESP32 NDJSON Collector
            ├── EG4 SQLite History
            ├── Analysis Engine
            ├── Reporting
            ├── Local Engineering Portal
            └── REST API (future)
```

## Infrastructure Baseline

### Proxmox Host

- Datto appliance
- Intel Core i3-7100U (2C/4T)
- 16 GB RAM
- HP EX900 500 GB NVMe
- Realtek Gigabit Ethernet
- Proxmox VE on Debian 13

### Current ISOs

- Ubuntu Server 24.04.3 LTS
- Debian 13.5 Netinst

### Home Assistant

- Installed and restored
- 64 GB virtual disk
- CPU type: host
- 2 vCPU
- 4 GB RAM

### Solar Digital Twin VM

- Hostname: `solardt`
- Ubuntu Server 24.04.3 LTS (Minimized)
- 2 vCPU
- 4 GB RAM
- 80 GB VirtIO SCSI disk
- UEFI (OVMF)
- QEMU Guest Agent enabled
- Python virtual environment
- Git repository initialized

## Engineering Decisions

### Accepted

1. Digital Twin runs in its own Ubuntu VM.
2. The dedicated local portal is the primary engineering interface.
3. Home Assistant may later consume Digital Twin data as a complementary interface.
4. Preserve raw evidence as authoritative source material.
5. Use SQLite for normalized history and engineering queries; expand only if justified.
6. Build incrementally and verify with real data.

### Working Philosophy

- Observation
- Evidence
- Analysis
- Conclusion

Hypotheses remain separate from measured facts.

## Security Direction

Solar Digital Twin follows the practical trusted-host security model documented
in `docs/SECURITY_MODEL.md`, comparable to a well-configured Home Assistant
installation. `solardt` is trusted; compromise of that host requires isolation,
rebuild, verification, and affected credential rotation. Conventional protected
credential files and unprivileged collectors are the default direction, while
future OPNsense VLANs and firewall rules provide the planned primary network-
containment boundary. Credential architecture, authentication-failure behavior,
and recovery choices must be approved before additional credentialed collector
work.

Risk is managed rather than eliminated. Controls protect credentials, evidence,
recovery options, and the physical system while remaining proportional to
plausible harm in a trusted home-lab. Ordinary read-only telemetry and offline
analysis should not carry the same friction as credentials, configuration,
control, public exposure, or destructive action. Delay, manual burden, and
unnecessary complexity are also engineering risks. The authoritative approval,
preservation, and audit policy is `CONTRIBUTING.md`.

## Roadmap

### Phase 1

- ✅ Install Home Assistant
- ✅ Restore backup
- ✅ Create Ubuntu VM
- ✅ Initialize Git repository

### Phase 2

- ✅ Import Engineering Bible
- ✅ Import EG4 connector
- ✅ Build EG4 SQLite foundation
- ✅ Build EG4 reporting and local portal

### Phase 3

- ✅ Add standalone SolarAssistant access to trusted JK BMS telemetry
- ✅ Add standalone ESP32 raw evidence collector
- ✅ Add offline-tested ESP32 retained-frequency stage
- Planned: normalize SolarAssistant and ESP32 history into SQLite
- Planned: integrate trusted JK BMS and ESP32 data into the portal

### Phase 4

- Planned: evidence-based event correlation
- Planned: broader engineering and forensic reports
- Deferred: REST API
- Deferred: Home Assistant publishing and broader automation

## Session Notes

### 2026-07-07

Completed:

- Installed Proxmox VE
- Installed Home Assistant OS
- Restored Home Assistant backup
- Created Ubuntu Digital Twin VM (`solardt`)
- Enabled QEMU Guest Agent
- Created Python virtual environment
- Initialized Git repository
- Created Solar Digital Twin project skeleton

Next:

- Import Engineering Bible
- Import EG4 Portal Collector
- Design SQLite schema
- Begin engineering data acquisition

## Maintenance

At the end of each major milestone this document should be revised.

Version numbers increase whenever architecture or accepted engineering decisions change.
