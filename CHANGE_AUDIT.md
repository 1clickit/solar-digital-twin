# Solar Digital Twin Change Audit

This is the authoritative append-only record of persistent project changes.
Do not silently edit, rewrite, or remove existing entries. Correct an entry by
appending a later correction that identifies it. Git history supplements this
record but does not capture every host, permission, service, device, database,
or runtime change.

## 2026-07-18T03:21:01Z — Governance recalibration

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Reconcile project roles, mission, workflow, risk, approval,
  preservation, audit, commit, and push policy.
- **Affected:** Authoritative governance and project-state documentation only;
  created this audit file.
- **Change:** Defined Chris as project owner/system operator, ChatGPT as
  proactive project lead/technical engineering partner, and Codex as bounded
  local implementation agent. Consolidated approval classes, established
  archive-first preservation and append-only auditing, clarified milestone
  commits/pushes, synchronized the forensic next task, and corrected stale
  protected-evidence access assumptions.
- **Reason:** Replace contradictory relay-era rules and duplicate approval
  ceremonies with one practical risk-calibrated operating model while
  preserving meaningful safeguards.
- **Untouched:** Source code, tests, prototypes, evidence, reports, databases,
  credentials, tokens, ACLs, permissions, users, groups, services, collectors,
  monitors, devices, tmux sessions, and runtime state.
- **Validation:** Documentation consistency searches, `git diff --check`,
  repository health check, index review, and final working-tree review.
- **Recovery:** Revert the related normal Git commit; prior tracked contents
  remain recoverable in Git history. No external archive was needed.
- **Related commit:** The commit containing this entry, titled `Recalibrate
  project leadership and risk policy`; not pushed at entry creation.
- **Limitations:** This entry establishes the audit from this checkpoint
  forward; it does not reconstruct every historical off-Git change.

## 2026-07-18T03:44:52Z — Archive, audit, and VM-health clarification

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Complete requirements omitted from the malformed governance-reset
  request without rewriting the governance commit or its audit entry.
- **Affected:** `CONTRIBUTING.md`, `START_HERE.md`, `PROJECT_INDEX.md`,
  `PROJECT_STATE.md`, `NEXT_TASK.md`, `CHANGE_AUDIT.md`, and new
  `docs/operations/VM_HEALTH_LOG.md`.
- **Change and reason:** Clarified archive handling under storage pressure,
  audit exclusions and secret safety, and created the required 30-day plus
  event-driven read-only VM health procedure, thresholds, and entry template.
- **Untouched:** Source, tests, prototypes, evidence, credentials, permissions,
  ACLs, users, groups, services, collectors, monitors, databases, devices,
  tmux sessions, and runtime state. No VM health measurement was performed.
- **Validation:** Documentation requirement searches, index/reference review,
  `git diff --check`, repository health check, and documentation-only scope
  review.
- **Recovery:** Revert the normal commit containing this entry; commit
  `a1e7c2d3` remains intact and prior tracked content remains in Git history.
- **Archive or backup:** Git history is sufficient for these documentation-only
  changes; no unique operational artifact was replaced.
- **Related commit and push:** The commit containing this entry, titled `Add
  archive audit and VM health policy`; not pushed at entry creation.
- **Follow-up:** Perform the first real read-only VM health review and append its
  result to the health log. No baseline measurements exist yet.

## 2026-07-18T04:01:42Z — Conservative ESP32 retention replay

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Reproduce the documented conservative retention candidate and
  test its forensic equivalence against validated real event/control windows.
- **Affected:** Offline analysis utility and focused tests; ESP32 retention,
  project-state, index, next-task, replay-report, and audit documentation.
- **Change and reason:** Added deterministic candidate-stream output and tests,
  replayed the immutable 12-hour capture under `/tmp`, and documented an Adopt
  decision after all classifications and complete-capture binary/text changes
  were preserved with material storage reduction.
- **Evidence identity:** Raw SHA-256
  `c48d647f97175261e7e015886001acc5bb06207e5336b3677e949ef9fe447059`;
  current-retained SHA-256
  `f2f78957078ed50cd9162f54e669e00e1a23a5e9149c67092d8c11b38e06d6ca`.
- **Untouched:** Evidence contents, production retention and collector defaults,
  services, devices, databases, portal, permissions, credentials, and runtime.
- **Validation:** Focused and full tests, deterministic replay, event/control
  comparison, pre/post evidence metadata and hashes, Python compilation,
  documentation checks, `git diff --check`, and repository health check.
- **Recovery:** Revert the related Git commit. Candidate output is reproducible
  derived material under `/tmp`; source evidence remains authoritative.
- **Related commit and push:** The commit containing this entry, titled
  `Validate conservative ESP32 retention replay`; normal milestone push planned
  after validation.
- **Limitations:** No real availability transition occurred in the capture;
  synthetic tests preserve that policy path. Cloud cover remains an alternative
  explanation, and implementation/deployment remain separate work units.

## 2026-07-18T04:16:44Z — Production ESP32 retention rollout plan

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Convert the adopted replay decision into a safe, reversible
  production implementation and canary plan without activating it.
- **Affected:** ESP32 production-retention plan, telemetry and replay documents,
  project index, project state, next task, and this audit record.
- **Change and reason:** Defined `esp32-conservative-v1`, one-process independent
  dual-policy writers, versioned output/manifest provenance, a 12-hour daytime
  three-output canary, bounded monitoring, non-destructive rollback,
  deterministic verification, 14 acceptance gates, and separate implementation,
  activation, analysis, and retirement milestones.
- **Untouched:** Source, tests, collectors, production retention, evidence,
  devices, services, databases, portal, credentials, permissions, captures,
  firmware, network, and runtime state.
- **Validation:** Policy/replay consistency and scope searches, documentation
  and index review, `git diff --check`, repository health check, and final
  documentation-only diff review.
- **Recovery:** Revert the related normal Git commit. Prior documentation remains
  recoverable in Git; no operational artifact was replaced or archived.
- **Related commit and push:** The commit containing this entry, titled `Plan
  production ESP32 retention rollout`; normal milestone push planned after
  validation.
- **Limitations:** Real availability transitions remain unobserved. The plan
  requires synthetic coverage and treats absent real transitions or events as a
  canary qualification rather than proof of full forensic validation.

## 2026-07-18T04:57:24Z — ESP32 conservative-retention canary implementation

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Implement the adopted conservative retained policy and dormant
  dual-output canary path using synthetic data only.
- **Affected:** ESP32 retention and SSE collector source, offline replay script,
  focused synthetic tests, production/telemetry documentation, project state,
  next task, index, and this audit record.
- **Change and reason:** Added versioned independent policies, exact candidate
  deadbands and availability normalization, exclusive output creation,
  isolated retained writers, explicit canary selection, versioned candidate
  naming, and a separate append-only capture manifest so a later live canary is
  reversible and does not replace the current default.
- **Untouched:** Existing evidence, production deployment and defaults, devices,
  endpoints, captures, services, collectors in operation, databases, portal,
  credentials, permissions, firmware, network, and physical system.
- **Validation:** Focused retention/collector/replay tests, full suite, Python
  compilation, documentation/index checks, `git diff --check`, repository
  health check, and synthetic-only/offline scope review.
- **Recovery:** Revert the related normal Git commit. Existing evidence and
  production behavior require no conversion or cleanup.
- **Archive or backup:** Git history preserves prior tracked implementation; no
  unique operational artifact was replaced.
- **Related commit and push:** The commit containing this entry, titled
  `Implement ESP32 retention canary support`; normal milestone push planned
  after validation.
- **Limitations:** Real availability transitions remain unobserved. The new
  path remains dormant pending a separately authorized live canary and its
  independent analysis; `esp32-frequency-v1` remains the production default.

## 2026-07-18T05:11:50Z — Custom diagnostic equipment guidance

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Record Chris's custom diagnostic equipment capability within the
  project's existing financial, practical, evidence, and safety constraints.
- **Affected:** Engineering Bible, ChatGPT project-lead instructions, project
  index, and this audit record.
- **Change and reason:** Added the ordered diagnostic-option decision path,
  criteria for choosing a certified commercial instrument or professional
  test, required explanation before purchase, and safety, isolation,
  calibration, timestamp, evidence, installation, and non-interference design
  boundaries. Added concise discovery references without duplicating policy.
- **Untouched:** Active technical next task, source, tests, firmware, hardware,
  equipment purchasing, evidence, devices, endpoints, captures, services,
  runtime, databases, portal, credentials, permissions, and physical system.
- **Validation:** Context and cross-reference review, fixed-income and safety
  consistency searches, documentation/index checks, `git diff --check`,
  repository health check, and documentation-only scope review.
- **Recovery:** Revert the related normal Git commit. Prior tracked content
  remains recoverable through Git history.
- **Archive or backup:** Git history is sufficient for these documentation-only
  additions; no unique operational artifact was replaced.
- **Related commit and push:** The commit containing this entry, titled
  `Document custom diagnostic equipment capability`; normal milestone push
  planned after validation.
- **Limitations:** This guidance authorizes no hardware design, purchase,
  installation, live measurement, or electrical work. Each future action
  remains separately risk-classified and bounded.

## 2026-07-18T05:44:11Z — Coordinated 24-hour capture preparation

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Prepare and launch one isolated read-only 24-hour ESP32, EG4,
  and SolarAssistant forensic capture on a common UTC interval.
- **Affected:** Coordinated supervisor and synthetic tests, ESP32 output-path
  selection and tests, capture runbook, ESP32 plans, project state, next task,
  index, and this audit record. The later live supervisor creates isolated
  evidence and runtime provenance outside Git and temporarily stops/restores
  only recorded competing EG4 units.
- **Change and reason:** Added exclusive common capture identity and manifest,
  independent source outputs, isolated EG4 database/evidence, automatic
  duration and process cleanup, compact status, disk stop threshold, exact
  prior-unit restoration, synthetic rehearsal, and a 24-hour operational
  runbook covering nighttime through post-sunset context.
- **Untouched:** Existing evidence and databases, device/firmware/configuration,
  production retention defaults, credentials and permissions, portal behavior,
  physical operation, and unrelated services. No control endpoint is used.
- **Validation:** Focused synthetic collector/coordinator tests, shortened
  temporary-directory rehearsal, full test suite, Python compilation,
  documentation/index checks, `git diff --check`, repository health check, and
  pre/post Git scope review.
- **Recovery:** Stop the capture-specific transient unit; its `SIGTERM` cleanup
  preserves partial evidence and restores only units recorded active before
  launch. Revert the related normal Git commit for repository rollback; never
  delete capture artifacts.
- **Archive or backup:** Git preserves prior tracked code. Isolated live
  evidence and append-only manifests remain under the coordinated capture root.
- **Related commit and push:** The commit containing this entry, titled
  `Prepare coordinated 24-hour forensic capture`; normal milestone push planned
  before live launch.
- **Limitations:** Cloud cover and other alternatives remain unresolved. Live
  availability transitions or forensic events are not guaranteed, and capture
  completion/analysis is a separate next work unit. Runtime identifiers,
  actual times, source starts, warnings, and restoration are recorded in the
  append-only coordinated manifest.

## 2026-07-18T06:12:39Z — Coordinated SolarAssistant identity correction

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Correct the confirmed SolarAssistant identity defect that caused
  the first coordinated-capture startup to abort.
- **Affected:** `scripts/coordinated_capture.py`, focused coordinated-capture
  tests, the coordinated runbook, project state, next task, and this audit
  record.
- **Change and reason:** Removed the forced `chris` group from the
  SolarAssistant child command so `runuser` preserves the normal `solardt-sa`
  account identity and its protected credential access. Added regression tests
  for default and explicit-group command construction and for the live
  SolarAssistant command. Recorded the failed startup and required unique-ID
  relaunch.
- **Untouched:** Credential contents, ownership, mode, and location; devices,
  services, collectors at runtime, existing evidence, databases, permissions,
  production defaults, and physical operation. No live capture was launched.
- **Validation:** Focused and full synthetic tests, Python compilation,
  documentation/index checks, `git diff --check`, repository health check, and
  a non-secret service-identity readability/nonempty metadata check.
- **Recovery:** Revert the related normal Git commit. The failed capture and
  append-only manifest remain preserved at their unique coordinated-capture
  location; no evidence rollback or deletion applies.
- **Archive or backup:** Git preserves the prior tracked implementation. The
  failed run remains preserved outside Git.
- **Related commit and push:** The commit containing this entry, titled
  `Fix coordinated SolarAssistant identity`; normal milestone push planned
  after validation.
- **Limitations:** No device endpoint, live collector, or new capture was used.
  A new uniquely identified coordinated capture still requires launch and
  startup verification.

## 2026-07-18T06:38:42Z — Active coordinated capture documentation

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Record the verified startup and current state of the active
  coordinated 24-hour three-source forensic capture.
- **Affected:** `PROJECT_STATE.md`, `NEXT_TASK.md`, and this audit record.
- **Change and reason:** Recorded active capture
  `solar-forensic-20260718T062127Z`, its live implementation checkpoint
  `6b734306c6f414c6413f7c6e86e9d443e3fe49e2`, successful three-source
  `startup_verified` state, isolated growing outputs, no recent errors,
  approximately 65.5 GB initial free space, and the planned automatic end at
  `2026-07-19T06:21:27.571Z`. The next task now protects the active run and
  defines completion, restoration, preservation, and analysis preparation.
- **Untouched:** Source and tests, collector processes and configuration,
  devices, credentials, services, timers, tmux sessions, permissions,
  databases, existing evidence, and production retention defaults. This was a
  documentation-only work unit with no device-control action or evidence
  rewrite.
- **Validation:** Privileged operator verification established that the
  supervisor and all three collectors were running with growing outputs and no
  recent errors. Documentation/index checks, `git diff --check`, repository
  health check, and documentation-only scope review were performed.
- **Recovery:** Revert the related normal Git documentation commit. The active
  capture continues from its recorded implementation commit independently of
  the repository documentation checkpoint.
- **Archive or backup:** Git history preserves prior documentation; active
  evidence and append-only runtime provenance remain isolated outside Git.
- **Related commit and push:** The commit containing this entry, titled
  `Document active coordinated capture`; normal milestone push planned after
  validation.
- **Limitations:** Capture completion, terminal manifest state, and automatic
  prior-service restoration are expected but not yet verified. Unprivileged
  process inspection can falsely report coordinated children as not running;
  operator-privileged verification controls process-state conclusions.
