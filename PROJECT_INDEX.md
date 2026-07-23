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
7. AGENTS.md
8. PROJECT_INDEX.md
9. SESSION_END.md when ending a session

## Engineering Documents
AGENTS.md
    Codex CLI entry point, communication guidance, guardrails, and local-agent operating rules.

AI_PROMPT.md
    ChatGPT project-lead duties, communication, continuity, and recalibration.

START_HERE.md
    Session startup instructions.

TEAM.md
    Chris, ChatGPT, and Codex roles and working relationship.

CONTRIBUTING.md
    Sole detailed canonical policy for workflow, risk and approval classes,
    preservation, audit, bounded Codex completion, commits, pushes, protected
    operational boundaries, and post-push verification.

PROJECT_STATE.md
    Current engineering status.

NEXT_TASK.md
    Exactly where development resumes.

PROJECT_CONTEXT.md
    Long-lived mission, architecture, and engineering principles; workflow
    details defer to CONTRIBUTING.md.

PROJECT_STATUS.md
    Superseded early July 7 status pointer retained for historical navigation;
    not current authority.

BACKLOG.md
    Future work and deferred ideas.

SESSION_END.md
    End-of-session checklist.

CHANGE_AUDIT.md
    Append-only record of persistent repository, host, runtime, permission,
    service, device, database, and network changes.

docs/operations/VM_HEALTH_LOG.md
    Append-only read-only solardt VM performance, capacity, and storage-health
    review procedure and log.

## Repository Layout

src/
    Application source code.

config/
    Configuration files.

docs/
    Project documentation.

docs/Engineering_Bible.md
    Solar Digital Twin mission and design authority, including cost discipline
    and custom diagnostic equipment capability and safety guidance.

docs/TELEMETRY_OBSERVATION_CONTRACT.md
    Owner-accepted authoritative common telemetry observation, provenance,
    timestamp, state, freshness, normalization, derived-lineage, and adapter
    contract.

docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md
    Owner-accepted authoritative source-specific mapping, registry,
    compatibility, acceptance-gate, and first offline implementation-slice plan
    under the accepted telemetry contract. Acceptance does not authorize
    implementation automatically.

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

docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md
    Implemented collector safeguards, installed and metadata-verified
    credentialless runtime, completed finite passive verification, and the
    separately gated persistent-operation decision.

docs/capture_analyses/esp32_sse_20260721_041439Z-integrity.md
    Immutable evidence identities, deterministic current-retention replay,
    ownership reconciliation, runtime closure, and accepted PASS WITH ONE
    QUALIFICATION result for the completed post-hardening ESP32 endurance
    capture.

docs/ESP32_RETENTION_ASSESSMENT.md
    Reproducible full-capture ESP32 retention measurements, candidate comparison, and policy recommendation.

docs/ESP32_RETENTION_REPLAY.md
    Deterministic real-window replay of raw, current-retained, and conservative
    ESP32 streams, with the accepted candidate decision and qualifications.

docs/ESP32_RETENTION_PRODUCTION_PLAN.md
    Versioned dual-output implementation, canary, rollback, verification, and
    production-acceptance plan for the adopted conservative ESP32 policy.

docs/COORDINATED_FORENSIC_CAPTURE.md
    Operational runbook for an isolated 24-hour ESP32, EG4, and SolarAssistant
    capture with append-only provenance and exact service restoration.

docs/COORDINATED_CAPTURE_INTEGRITY.md
    Immutable inventory, native-format integrity, coverage, cadence, source
    identity, and qualified-pass result for the closed coordinated capture.

docs/COORDINATED_CAPTURE_CORRELATION.md
    First reproducible real-capture three-source correlation, controls,
    retention comparison, sensitivity review, conclusions, and owner questions.

docs/capture_analyses/solar-forensic-20260718T062127Z-events.tsv
    Deterministic compact table for seven selected events and three controls.

docs/capture_analyses/solar-forensic-20260718T062127Z-battery-cell-review.md
    Detailed read-only Battery 1/Battery 2 cell, pack, temperature, and topic-
    coverage review at the seven event anchors and three controls, including
    capture-wide extrema and immutable evidence identities.

docs/capture_analyses/cooling-control-20260719T115613Z-analysis.md
    Source-update-aware analysis of the completed two-hour Home Assistant
    cooling-control capture, including temperature-cycle episodes, power
    context, cadence limits, provenance, and the no-fan-inference boundary.

docs/capture_inventories/solar-forensic-20260718T062127Z-inventory.tsv
    Relative path, byte size, nanosecond modification time, and SHA-256 identity
    for every file in the closed coordinated capture.

docs/HOME_ASSISTANT_INTEROPERABILITY_PLAN.md
    Future reciprocal read-only HA telemetry, local EG4 candidate assessment,
    lineage protection, security boundaries, and RS-485 topology review.

docs/EG4_HOME_ASSISTANT_TELEMETRY.md
    Validated GET-only Home Assistant telemetry-bridge method, EG4 Web Monitor
    hybrid-mode provenance, exact entity allowlist, source-cadence semantics,
    control prohibition, and recommended retained metadata.

docs/EG4_LOCAL_DONGLE_INVESTIGATION.md
    Pinned public-source protocol research, read/write boundary, provenance,
    coexistence risks, and separately gated one-shot plan for the existing EG4
    Wi-Fi dongle.

docs/IRRADIANCE_MEASUREMENT_PLAN.md
    Future on-site plane-of-array irradiance and temperature measurement,
    calibration, safety, provenance, and expanded-capture plan.

docs/TELEMETRY_SOURCE_ROLES.md
    Agreed authority, comparison, forensic, and display roles for telemetry sources.

docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md
    Authoritative semantics, source boundaries, research defaults, episode
    hierarchy, recovery observations, and phased implementation plan for
    abrupt daytime solar-production collapse investigation.

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
    Hardened read-only ESPHome SSE evidence collector with fixed destination,
    proxy/redirect rejection, bounded input, response validation, restrictive
    output modes, default current retention, and explicit canary support.

scripts/install_esp32_runtime.sh
    Credentialless whole-application runtime installer with side-effect-free
    check, explicit install, metadata-only verification, shared-runtime refusal,
    archival rollback, and dormant-unit safeguards.

scripts/run_esp32_forensic_collector.sh
    Fixed-path, installed-commit-aware, finite foreground ESP32 launcher.

systemd/esp32-forensic-collector.service
    Dormant hardened ESP32 service definition with no timer or activation target.

tests/test_esp32_runtime.py
    Offline installer, launcher, and systemd semantic regression tests.

src/solar_digital_twin/collectors/esp32_retention.py
    Versioned current and conservative ESP32 retention policies, canonical
    deadbands, and entity-local availability normalization.

src/solar_digital_twin/telemetry/esp32_adapter.py
    Synthetic-only, I/O-free exact ESP32 generator-frequency root adapter with
    strict registry identity, lossless source fields, and copy provenance.

tests/fixtures/telemetry/esp32_generator_frequency.json
    Synthetic ESP32 SSE-shaped frequency values, states, occurrences, and
    raw/current/conservative copy references.

tests/test_esp32_adapter.py
    Focused finite-value, identity, state, provenance, rejection, immutability,
    and I/O-boundary tests for the synthetic ESP32 adapter.

scripts/coordinated_capture.py
    Three-source isolated capture supervisor, synthetic rehearsal, compact
    status, duration control, and prior-unit restoration.

scripts/analyze_esp32_retention.py
    Streaming offline raw/retained ESP32 assessment and deterministic candidate
    replay utility.

scripts/analyze_coordinated_capture.py
    Explicit-path, identity-gated, bounded-memory real coordinated-capture
    runner with deterministic controls, sensitivity sets, and derived outputs.

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
