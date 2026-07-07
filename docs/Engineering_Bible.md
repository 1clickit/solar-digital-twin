# Solar Digital Twin Engineering Bible

**Version:** 0.1  
**Status:** Living Document

## Mission

Build an engineering-grade Digital Twin for a residential power system that preserves raw evidence, correlates data from multiple sources, and produces defensible engineering analysis.

## Guiding Principles

- Preserve raw evidence.
- Never overwrite historical evidence.
- SQLite is the engineering source of truth.
- Reports are derived products.
- Home Assistant is a consumer, not the owner, of engineering data.
- Optimize only after measurement.
- Prefer simple architectures until complexity is justified.

## Current Architecture

```
Proxmox VE
├── Home Assistant OS
└── Ubuntu Server (solardt)
      └── Solar Digital Twin
            ├── EG4 Collector
            ├── SQLite
            ├── Analysis Engine
            ├── Reporting
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
2. Home Assistant consumes Digital Twin data.
3. Preserve raw evidence.
4. SQLite first; expand only if justified.
5. Build incrementally and verify with real data.

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

- Import Engineering Bible
- Import EG4 connector
- Build SQLite schema
- Build reporting

### Phase 3

- Add Solar Assistant
- Add JK BMS
- Add ESP32 logger

### Phase 4

- Event correlation
- Engineering reports
- REST API

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
