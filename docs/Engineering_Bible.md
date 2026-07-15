# Solar Digital Twin Engineering Bible

**Version:** 0.2
**Status:** Living Document

## Mission

Build an engineering-grade Digital Twin for a residential power system that preserves raw evidence, correlates data from multiple sources, and produces defensible engineering analysis.

## Primary User and Intended Use

Chris is the primary user, project owner, and system operator. The dedicated
local portal is the intended primary engineering interface for normal system
awareness, historical review, and evidence-based forensic investigation.
Home Assistant may later provide complementary convenience, status, and alerts,
but it is not an authoritative data store.

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
