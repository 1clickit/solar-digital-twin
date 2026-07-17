# PROJECT INDEX

This document is the navigation map for the
Solar Digital Twin repository.

The repository is the project's memory.

Every important document, script and
directory should be referenced here.

## Session Startup

Read in this order:

1. START_HERE.md
2. TEAM.md
3. CONTRIBUTING.md
4. PROJECT_STATE.md
5. NEXT_TASK.md
6. AI_PROMPT.md
7. SESSION_END.md

## Engineering Documents
AGENTS.md
    Codex CLI entry point, communication guidance, guardrails, and local-agent operating rules.

AI_PROMPT.md
    Manual ChatGPT operating and communication guidance.

START_HERE.md
    Session startup instructions.

TEAM.md
    Team roles and communication.

CONTRIBUTING.md
    Engineering workflow and standards.

PROJECT_STATE.md
    Current engineering status.

NEXT_TASK.md
    Exactly where development resumes.

BACKLOG.md
    Future work and deferred ideas.

SESSION_END.md
    End-of-session checklist.

## Repository Layout

src/
    Application source code.

config/
    Configuration files.

docs/
    Project documentation.

docs/Engineering_Bible.md
    Solar Digital Twin design authority.

docs/EG4_LOCAL_PORTAL.md
    Current EG4 portal operations and the primary engineering-interface plan.

docs/PORTAL_UI_DESIGN.md
    Accepted design direction and synthetic-only boundary for the future primary portal.

docs/chat_ideas/README.md
    Non-authoritative holding area for deferred, open, and superseded portal ideas.

docs/EG4_FORENSIC_CORRELATION.md
    Offline-tested ESP32 frequency retention and planned AC-couple correlation design.

docs/ESP32_FORENSIC_TELEMETRY_PLAN.md
    Read-only ESPHome SSE collection and timestamp design.

docs/ESP32_RETENTION_ASSESSMENT.md
    Reproducible full-capture ESP32 retention measurements, candidate comparison, and policy recommendation.

docs/TELEMETRY_SOURCE_ROLES.md
    Agreed authority, comparison, forensic, and display roles for telemetry sources.

docs/SOLARASSISTANT_TELEMETRY_PLAN.md
    Read-only SolarAssistant collection, evidence, cadence, and retained-output policy.

docs/SOLARASSISTANT_RUNTIME.md
    Installed and manually verified dedicated runtime, credential boundary, operating paths, and recovery workflow.

docs/SOLARASSISTANT_MONITOR.md
    Offline-tested LAN-only live-capture monitor, dashboard, report, and narrowly validated abort design.

docs/SOLARASSISTANT_DEADBAND_ASSESSMENT.md
    Completed offline raw-evidence characterization; evidence was insufficient and no SolarAssistant deadbands are approved.

docs/SECURITY_MODEL.md
    Approved Home Assistant-style trust, runtime isolation, credential, authentication, network, and recovery model.

docs/DEVICE_ACCESS_RECOVERY.md
    Device access, effective-authority classification, credential, failure, and recovery inventory.

src/solar_digital_twin/collectors/solarassistant.py
    Standalone read-only SolarAssistant raw and separately retained evidence collector.

scripts/install_solarassistant_runtime.sh
    Reviewed fixed-path runtime installer with non-privileged checking and metadata verification.

scripts/install_solarassistant_credential.sh
    Reviewed controlling-terminal credential installer used for the completed secure installation.

scripts/run_solarassistant_monitor.sh
    Foreground-only SolarAssistant monitor launcher with a safe non-privileged check mode.

src/solar_digital_twin/reporting/solarassistant_monitor.py
    Read-only in-memory SolarAssistant evidence monitor and explicit local HTTP endpoints.

src/solar_digital_twin/collectors/solarassistant_retention.py
    SolarAssistant topic classification and per-metric exact-change/heartbeat policy.

src/solar_digital_twin/collectors/retention.py
    Shared source-independent change and heartbeat retention mechanics.

src/solar_digital_twin/collectors/esp32_sse.py
    Standalone read-only ESPHome SSE evidence collector.

scripts/analyze_esp32_retention.py
    Streaming offline raw/retained ESP32 retention assessment utility.

src/solar_digital_twin/analysis/forensic_correlation.py
    Pure offline three-source timestamp alignment and conservative synthetic
    AC-couple event analysis.

src/solar_digital_twin/analysis/correlation_adapters.py
    Explicit read-only, bounded-window EG4 SQLite and SolarAssistant/ESP32
    NDJSON adapters for offline correlation.

docs/AI_ENGINEERING_FRAMEWORK_MVP.md
    Reusable AI engineering framework MVP boundary design.


database/
    SQLite schemas and databases.

reports/
    Generated engineering reports.

evidence/
    Captured forensic evidence.

scripts/
    Utility and maintenance scripts.

## Repository Philosophy

GitHub is the authoritative record of
all committed engineering work.

The local VM is the engineering workspace.

Every session should improve the repository
so that future engineers require less
conversation and more documentation.
- docs/DEVICE_TIME_SYNC_INVENTORY.md - Device time synchronization inventory and NTP evidence
