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

## 2026-07-18T20:01:33Z — Bounded Codex authorization clarification

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Clarify manual terminal operation, complete bounded Codex
  autonomy, interface confirmations, escalation, and later review without
  changing the existing governance model.
- **Affected:** `CONTRIBUTING.md` as canonical workflow policy, direct Codex
  instructions in `AGENTS.md`, ChatGPT project-lead guidance in `AI_PROMPT.md`,
  and this audit record.
- **Change and reason:** Established that one-step pacing primarily applies to
  actions Chris performs; an authorized Codex work unit proceeds through all
  explicitly included activities without duplicate permission. Consolidated
  exact stop conditions, ChatGPT reauthorization flow, platform-confirmation
  limits, and the distinction between transient session history and durable
  Git/audit records.
- **Untouched:** Project roles, risk and approval classes, active coordinated
  capture state and task, source and tests, evidence, databases, credentials,
  services, processes, timers, permissions, VM/runtime configuration, devices,
  and production behavior.
- **Validation:** Governance contradiction review, protected-boundary review,
  documentation/index checks, `git diff --check`, repository health check, and
  documentation-only scope review.
- **Recovery:** Revert the related normal Git documentation commit. Prior
  tracked governance remains recoverable through Git history.
- **Archive or backup:** Git history is sufficient for these documentation-only
  changes; no unique operational artifact was replaced.
- **Related commit and push:** The commit containing this entry is titled
  `Clarify bounded Codex authorization workflow`; normal push planned after
  validation.
- **Limitations:** This clarification grants no action beyond an explicitly
  authorized bounded work unit and does not bypass platform security controls.
  Session/activity history is not claimed as permanent evidence.

## 2026-07-18T20:53:35Z — Home Assistant and irradiance planning

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Preserve future reciprocal Home Assistant telemetry, local EG4
  assessment, RS-485 topology review, and on-site irradiance/temperature
  measurement plans without displacing the active coordinated capture.
- **Affected:** New Home Assistant interoperability and irradiance measurement
  plans, Engineering Bible principles, project index, backlog cross-references,
  and this audit record.
- **Change and reason:** Defined allowlisted LAN-only read-only exchange in both
  directions, stable schema and lineage/loop protections, practical credential
  boundaries, a controlled `joyfulhouse/eg4_web_monitor` candidate pilot, a
  mandatory bus-ownership review before any second RS-485 master, and safe
  calibrated plane-of-array irradiance/temperature evidence. Recorded operator
  questions and the future sequence after capture completion and first
  analysis.
- **Untouched:** Active capture task/state, source and tests, Home Assistant and
  devices, credentials, networking, RS-485 wiring, services/processes/timers,
  evidence, databases/manifests, collectors/retention, permissions, and runtime.
- **Validation:** Active-task preservation review, no-control and provenance
  boundary searches, documentation/index checks, `git diff --check`, repository
  health check, and documentation-only scope review.
- **Recovery:** Revert the related normal Git documentation commit. Prior
  tracked documentation remains recoverable through Git history.
- **Archive or backup:** Git history preserves prior documentation; no unique
  operational artifact was replaced.
- **Related commit and push:** The commit containing this entry is titled
  `Plan Home Assistant telemetry interoperability`; normal push planned after
  validation.
- **Limitations:** No transport, integration, sensor, topology, or production
  source is selected or validated. The EG4 candidate remains control-capable
  software under a proposed read-only pilot policy, and irradiance remains a
  future diagnostic source rather than an alpha blocker.

## 2026-07-19T04:01:48Z — Capture closure and EG4 dongle investigation

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Reconcile authoritative state after the intentional coordinated
  capture stop and Home Assistant discovery, and prepare a public-source-only,
  strictly read-only future EG4 Wi-Fi-dongle measurement path without
  displacing evidence analysis.
- **Affected:** `PROJECT_STATE.md`, `NEXT_TASK.md`, `PROJECT_INDEX.md`, the
  coordinated-capture and Home Assistant plans, telemetry source roles, new
  `docs/EG4_LOCAL_DONGLE_INVESTIGATION.md`, and this append-only entry.
- **Change and reason:** Recorded controlled terminal state `interruption` /
  `signal`, normal child shutdown, successful unit restoration, immutable
  evidence and outstanding integrity/analysis work; recorded verified HA,
  MQTT, EG4-cloud, ESPHome, and dongle topology. Pinned public research found a
  proprietary LuxPower envelope carrying Modbus functions, an explicit
  read/write boundary, source-code/default polling discrepancy, conservative
  read blocks, and unresolved single-client/cloud coexistence risk.
- **Public checkpoints:** `joyfulhouse/eg4_web_monitor`
  `485bc613448d57917c6e4d01e42f128aa4ecbbb3` and its declared minimum
  `pylxpweb>=0.9.39b3`; `pylxpweb` tag `v0.9.39b3` commit
  `889f1ba2d55d23efe2e5fdaa0dbdc50c4adc35ab` was inspected as that minimum.
- **Untouched:** No LAN solar device, Home Assistant, EG4 cloud endpoint,
  credential, runtime process/service/timer, collector, evidence, manifest,
  operational database, permission, network, MQTT broker, firmware, or
  production retention behavior was accessed or changed. Public clones existed
  only under `/tmp`; no upstream source was vendored.
- **Validation:** Pinned-source file/commit review, provenance and read/write
  boundary review, stale-state/contradiction searches, documentation checks,
  `git diff --check`, and repository health check.
- **Recovery:** Revert the related normal Git documentation commit. Prior
  tracked documentation remains recoverable in Git history; no runtime or
  evidence rollback is applicable.
- **Archive or backup:** Git history preserves prior documentation. Temporary
  public research clones are non-evidence working material under `/tmp`.
- **Related commit and push:** The commit containing this entry is titled
  `Document capture closure and EG4 dongle investigation`; normal push planned
  after validation.
- **Limitations:** No exact live request is authorized or ready. Exact device
  serials, dongle firmware, port-8000 protocol acceptance, and safe coexistence
  with cloud traffic remain unresolved. Capture inventory and three-source
  analysis remain first priority.

## 2026-07-19T04:29:36Z — Coordinated capture integrity verification

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Inventory, hash, and validate the closed coordinated capture
  before three-source offline analysis.
- **Affected:** New integrity report and tracked 444-file identity inventory;
  coordinated runbook, project state, next task, project index, and this
  append-only audit record.
- **Change and reason:** Recorded a qualified integrity pass after bounded
  read-only verification of manifest chronology, file identities, native parse
  and newline integrity, timestamps, cadence/gaps, source coverage, EG4 SQLite
  integrity and stored artifact hashes, approved ESP32 entities, and exact
  retained-stream subsequences. Documented that the ESP32-specific manifest
  lacks a terminal record while the common manifest records its controlled
  SIGTERM and all ESP32 evidence streams end cleanly.
- **Evidence identity:** 444 files / 685,044,693 bytes. Inventory TSV SHA-256
  `4a26541c296957ed1a84dafd0ce95c62d06540802ab9c5876c0adbf50393b529`;
  sorted absolute-path SHA-256 snapshot identity
  `1add9b983da00d9996996ca21848d18965246e6dc34eace61d8ba76133b03a1c`.
- **Untouched:** All evidence and operational databases; devices, credentials,
  permissions, services, processes, timers, collectors, monitors, portal,
  network, firmware, and production retention behavior.
- **Validation:** Stable matching pre/post 444-file SHA-256 inventories; zero
  malformed or backward NDJSON records; complete final newlines; all 425 EG4
  JSON files valid; SQLite immutable read-only integrity `ok`; all 340 stored
  EG4 artifact hashes matched; both ESP32 retained streams were ordered
  exact-byte raw subsequences; documentation checks, focused/full tests,
  `git diff --check`, and repository health check.
- **Recovery:** Revert the related normal Git commit. The generated inventory
  and report are reproducible from immutable sources; no evidence rollback
  applies.
- **Archive or backup:** The isolated evidence remains preserved at its
  original `/var/lib` path. Git preserves the tracked derived inventory and
  report.
- **Related commit and push:** The commit containing this entry is titled
  `Verify coordinated capture integrity`; push is not authorized in this work
  unit.
- **Limitations:** Source-local ESP32 terminal provenance is incomplete.
  Approximately 15-minute EG4 cadence limits event timing. Integrity does not
  establish equipment causation or promote `esp32-conservative-v1`; bounded
  three-source analysis and owner review remain next.

## 2026-07-19T04:33:30Z — Integrity inventory tracked-path correction

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Correct the tracked location of the generated immutable identity
  inventory after the post-commit repository health check rejected a tracked
  file beneath ignored `reports/`.
- **Affected:** Inventory path, its documentation/index references, and this
  append-only correction entry.
- **Change and reason:** Moved the unchanged inventory from `reports/` to
  `docs/capture_inventories/` so generated operational reports and raw evidence
  directories remain wholly ignored while this durable evidence-identity
  record remains tracked. Its content and SHA-256 are unchanged.
- **Untouched:** Capture evidence, inventory contents and identity, analysis
  conclusions, devices, credentials, permissions, runtime, services,
  collectors, databases, and production policy.
- **Validation:** Inventory SHA-256 remains
  `4a26541c296957ed1a84dafd0ce95c62d06540802ab9c5876c0adbf50393b529`;
  focused/full tests from the original verification remain applicable;
  `git diff --check` and repository health check passed after relocation.
- **Recovery:** Revert this normal correction commit and the preceding
  integrity commit together if the entire checkpoint must be removed. Do not
  move the file back beneath ignored `reports/` without changing the health
  policy intentionally.
- **Related commit and push:** The commit containing this entry is titled
  `Correct coordinated inventory path`; no push is authorized.
- **Limitations:** This correction changes only tracked repository placement;
  it adds no new source verification or analysis conclusion.

## 2026-07-19T05:28:42Z — Coordinated three-source correlation analysis

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Complete the first reproducible, bounded offline correlation of
  integrity-verified capture `solar-forensic-20260718T062127Z` using EG4,
  high-resolution ESP32, and trusted SolarAssistant/JK BMS telemetry.
- **Files changed:** Added `scripts/analyze_coordinated_capture.py`, its focused
  tests, `docs/COORDINATED_CAPTURE_CORRELATION.md`, and the compact event TSV;
  strengthened the adapter's SQLite read-only URI; reconciled project state,
  next task, index, and relevant capture/correlation documentation; appended
  this audit entry.
- **Evidence read:** Exactly the six inventory-recorded primary artifacts under
  `/var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z`:
  `eg4/eg4_capture.sqlite`; the raw, `esp32-frequency-v1`, and
  `esp32-conservative-v1` ESP32 NDJSON files; and the raw and retained
  SolarAssistant NDJSON files. No evidence was copied or written.
- **Exact identities:** EG4 SHA-256 `153070c4a8488d9b3c8719be68f2aedbf065ab25b84df7adafb71d3692975fb8`,
  647168 bytes, mtime_ns 1784431424329281543; ESP32 raw
  `a3e720b1027ecf2927f1d98cf6cc113faebfc560cea5e7a6dadbd3b40d90122b`,
  275220446 bytes, 1784432180722722866; current retained
  `9e288bd184154cc6aa90823a5a6075260250fac03e89d3a43ee4b76149e8be5c`,
  266259706 bytes, 1784432180722722866; conservative retained
  `c81a3841291f91c6f32436bc05a88d3155debfb249c7776795c8ae650a9e8aa7`,
  63972840 bytes, 1784432174673015267; SolarAssistant raw
  `e4c1b1bbb3e288f139dc3bb9979f17adf59493851e347b588b950176f3d76e4e`,
  70969608 bytes, 1784432171335176595; SolarAssistant retained
  `aa6e87f22d9d79b2ad9bf29d3367552ac399e956bd2c26acc8d18ec9ffaf2048`,
  1556735 bytes, 1784432171334176643. Every size, mtime, and digest matched
  before and after analysis.
- **Analysis parameters:** Primary documented configuration: 1000 W minimum
  baseline, 500 W absolute drop, 40% fractional drop, two plateau samples,
  80% recovery, 100 W zero-output threshold, 900-second search window,
  600/420-second acceptable runtime/day gaps, and 15/2/600/420-second
  SolarAssistant/ESP32/runtime/day alignment tolerances. Fixed sensitivity used
  strict 1500/750/45%/85% and loose 750/350/25%/75% baseline/drop/fraction/
  recovery values with all other parameters unchanged.
- **Results:** Seven primary candidates were detailed with three deterministic
  controls. The five zero-output candidates were stable across all parameter
  sets; the two partial collapses were threshold-sensitive, and loose settings
  added one candidate. Aggregate loss/rejoin is supported, while cloud/solar
  variability, battery/inverter control, electrical behavior, and aggregate
  microinverter dropout/rejoin cannot be distinguished causally. No unique
  coincident frequency, voltage, availability, temperature, or imbalance
  disturbance was established. Trusted battery telemetry showed context and
  some flow transitions, not a consistent exclusive constraint signature.
- **Retention comparison:** Raw, `esp32-frequency-v1`, and canary
  `esp32-conservative-v1` preserved the event/control classifications and
  critical bounded context. This is supporting evidence only and changes no
  retention-policy status.
- **Validation:** 51 focused runner/analyzer/adapter/coordinated-capture tests
  and all 188 repository tests passed; changed Python compiled; deterministic
  real reruns produced byte-identical JSON and TSV; output hashes were
  `5c92a3bf3a28de985c684728e754f75277d89eac1a2c62b576dc72fbe0f66d7f`
  and `756eb803b6e171f186fd366b50c581cb354ebc77cbba6ef784721ede98b6b9b5`;
  `git diff --check` and repository health passed.
- **Untouched:** Evidence, devices, credentials, operational databases,
  services, processes, collectors, timers, runtime, permissions, users/groups,
  networking, Home Assistant, MQTT, EG4 dongle/cloud, SolarAssistant/ESP32
  endpoints, firmware, and retention production state.
- **Reproducibility and recovery:** The report records the exact explicit-path
  command and UTC bounds. Revert the normal Git commit to recover repository
  state; evidence requires no rollback and remained immutable.
- **Related commit and push:** The commit containing this entry is titled
  `Analyze coordinated three-source evidence`; normal non-force push is
  authorized after final validation.
- **Limitations:** Coarse EG4 cadence and aggregation, receipt-time latency,
  sparse runtime context, calculated rather than independently observed active
  microinverter count, missing irradiance, and incomplete ESP32 source-local
  terminal provenance constrain interpretation. The common manifest records
  controlled SIGTERM and all ESP32 streams end cleanly. Owner review is required
  before any separately gated follow-up measurement.

## 2026-07-19T05:40:01Z — Correlation worktree reconciliation and SVG restoration

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Reconcile the in-progress three-source analysis after a duplicate
  Codex writer was terminated, restore the intended deterministic SVG output,
  and revalidate the complete work unit before commit and push.
- **Affected:** `scripts/analyze_coordinated_capture.py`, its focused tests,
  `docs/COORDINATED_CAPTURE_CORRELATION.md`, new deterministic event overview
  `docs/capture_analyses/solar-forensic-20260718T062127Z-events.svg`, and this
  append-only reconciliation entry.
- **Change and reason:** Re-reviewed all staged and untracked work without
  resetting or discarding it. Confirmed that the concurrent edit had omitted
  the intended required `--svg-output` behavior. Restored distinct-path and
  evidence-boundary validation, dependency-free deterministic SVG generation,
  byte-comparison tests, and an explanation limiting screenshot interpretation
  to observed event magnitude and recovery rather than causation.
- **Real rerun:** Two complete runs again produced seven candidates and three
  controls with matching pre/post identities for all six pinned evidence files.
  JSON, TSV, and SVG were byte-identical between runs. SHA-256 identities were
  JSON `5c92a3bf3a28de985c684728e754f75277d89eac1a2c62b576dc72fbe0f66d7f`,
  TSV `756eb803b6e171f186fd366b50c581cb354ebc77cbba6ef784721ede98b6b9b5`,
  and SVG `a9ced67f7a32612bf2cb196fb3326c1bd8dd6c69cdb186720d3442042df8b167`.
- **Validation:** 51 focused tests passed; all 188 repository tests passed
  (the five localhost HTTP tests used the execution environment's narrowly
  approved unittest permission after sandbox socket denial); changed Python
  compiled; `git diff --check` and repository health passed.
- **Untouched:** All raw evidence and operational databases; devices,
  credentials, services, processes, timers, collectors, runtime, permissions,
  networking, Home Assistant, MQTT, firmware, and retention production state.
- **Recovery:** Revert the normal correlation commit. All derived outputs are
  reproducible from immutable inputs; evidence requires no rollback.
- **Related commit and push:** Included in `Analyze coordinated three-source
  evidence`; normal non-force push authorized after final validation.
- **Limitations:** The SVG is a derived overview of EG4 observations and adds no
  new measurement or causal evidence. The limitations in the preceding work-unit
  entry remain unchanged.

## 2026-07-19T06:34:06Z — Preserve coordinated battery-cell review

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Preserve the completed temporary read-only SolarAssistant
  battery-cell review as durable project evidence and reconcile the owner-review
  state without authorizing a new measurement.
- **Source and destination:** Copied the exact regular file
  `/tmp/solar-forensic-20260718T062127Z-battery-cell-review.md` to
  `docs/capture_analyses/solar-forensic-20260718T062127Z-battery-cell-review.md`.
  Both were 49,471 bytes with SHA-256
  `7572ba7422b9c89bd754b79db9f5507e0152e3bb1ff77efbe619f84a971af289`.
- **Read-only evidence review:** Streamed 305,172 raw SolarAssistant records
  across 42 discovered topics and inspected the 5,951-record, 12-topic retained
  file. The review used actual topic names and captured offsets for before,
  nearest, and after observations at seven event anchors and three controls.
- **Evidence identities:** Raw evidence matched before and after: 70,969,608
  bytes, mtime_ns 1784432171335176595, SHA-256
  `e4c1b1bbb3e288f139dc3bb9979f17adf59493851e347b588b950176f3d76e4e`.
  Retained evidence matched before and after: 1,556,735 bytes, mtime_ns
  1784432171334176643, SHA-256
  `aa6e87f22d9d79b2ad9bf29d3367552ac399e956bd2c26acc8d18ec9ffaf2048`.
- **Findings preserved:** Event-anchor spread was 2–10 mV for Battery 1 and
  1–8 mV for Battery 2; capture maxima were 24/19 mV and highest reported cells
  were 3.501/3.494 V. No positive JK overvoltage-protection evidence was found.
  Missing MOS/protection and related topics limit absolute exclusion, but the
  available evidence does not support JK protection for any event or all seven.
- **Affected:** Permanent detailed report, coordinated correlation report,
  project index, project state, next task, and this append-only audit entry.
- **Untouched:** Raw and retained evidence, operational databases, devices,
  services, runtime, collectors, timers, networking, credentials, firmware,
  permissions, Home Assistant, MQTT, and production retention behavior.
- **Validation:** Exact source/destination byte and SHA-256 comparison; complete
  diff review; documentation/index checks; `git diff --check`; repository
  health check; clean post-commit worktree and exact commit-file review planned.
- **Recovery:** Revert the normal local preservation commit. Source evidence
  requires no rollback; Git will preserve the detailed derived report.
- **Related commit and push:** The commit containing this entry is titled
  `Preserve coordinated battery cell review`. Push is explicitly not authorized
  in this work unit.
- **Limitations:** Missing exported MOS, balancing, protection/alarm,
  individual-cell, and charge-limit topics mean an unobserved transient cannot
  be absolutely excluded. No new measurement is authorized.

## 2026-07-20T18:16:37Z — Preserve cooling analysis and Home Assistant telemetry findings

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Preserve the completed July 19 cooling-control analysis and the
  reusable, validated Home Assistant / EG4 Web Monitor telemetry method without
  promoting fan investigation into the active milestone.
- **Affected:** Added the tracked cooling analysis and
  `docs/EG4_HOME_ASSISTANT_TELEMETRY.md`; updated project state, next-task
  deferral, project navigation, and this append-only audit record.
- **Change and reason:** Preserved the validated temporary report faithfully,
  adding only a tracked-report note that pairs each ignored evidence filename
  with its byte size, hash, and validation status;
  documented the successful GET-only `/api/states` bridge, exact allowlist,
  source-update timestamp semantics, hybrid-mode lineage qualification,
  control prohibition, and retained-metadata requirements; deferred any fan
  instrumentation until after primary project milestones.
- **Evidence identity:** Ignored immutable raw telemetry is 20,227,369 bytes,
  SHA-256 `4c411fbd9e258ffc217da2d52f3690662c4c97f1a73281b00f71174ff687cf0f`;
  its manifest is 3,066 bytes, SHA-256
  `96ed69112d9cfe8e78524557fedbe6afdf2e594f1386ee3b066cae44beac02f0`.
  Both matched the completed read-only analysis identities.
- **Findings preserved:** The two-hour capture completed 7,200/7,200 requests
  with zero errors. Radiator 1/2 ranges were 59–72/47–51 °C with 52/32
  distinct source updates; eight high-temperature episodes were stable under
  5- and 10-minute grouping. Every next Radiator 1 source value was below 68
  °C after about 121 seconds. No fan telemetry existed, and no fan activity or
  causation was inferred.
- **Untouched:** Immutable capture evidence; Home Assistant, EG4 dongle/cloud,
  SolarAssistant, ESP32, credentials, network, firmware, devices, services,
  timers, collectors, databases, permissions, and runtime configuration. No
  installation, device contact, commit, or push occurred.
- **Validation:** Temporary/tracked analysis-body comparison after excluding
  the documented tracked-only preservation note;
  evidence pre/post identity checks; documentation and sensitive-content
  searches; `git diff --check`; repository health check; and final working-tree
  review.
- **Recovery:** Revert the future normal documentation commit containing this
  entry. The ignored immutable capture remains authoritative and requires no
  rollback.
- **Related commit and push:** Not committed or pushed; awaiting separate
  approval.
- **Limitations:** Home Assistant polling cadence is not source cadence;
  per-entity local-dongle/cloud lineage remains unproven; no fan command, RPM,
  PWM/duty, current, or acoustic evidence was captured.

## 2026-07-20T19:24:32Z — Consolidate workflow authority and project direction

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Reduce routine software relay burden by making one coherent
  bounded repository workflow canonical, and record the owner-accepted
  diagnostic baseline and next technical direction.
- **Affected:** `CONTRIBUTING.md`, `START_HERE.md`, `AGENTS.md`, `TEAM.md`,
  `SESSION_END.md`, `PROJECT_STATE.md`, `NEXT_TASK.md`, `PROJECT_CONTEXT.md`,
  `BACKLOG.md`, `PROJECT_STATUS.md`, `PROJECT_INDEX.md`, and this append-only
  audit entry. `AI_PROMPT.md` was reviewed and already provided the required
  concise audience-specific behavior, so it was not changed.
- **Authority change:** Explicit approval of a clearly bounded repository-only
  work unit now authorizes uninterrupted inspection, in-scope edits,
  correction, validation, directly related documentation, exact staging, one
  normal local commit, one normal fast-forward push to expected `origin/main`,
  and published-result verification when all canonical safeguards pass.
  `CONTRIBUTING.md` is the sole detailed current authority.
- **Supersession:** Active requirements for separate routine local-commit or
  normal-push approval are superseded. Historical audit entries recording older
  approval boundaries remain unchanged as historical evidence and are not
  current authority. Destructive or exceptional Git operations remain gated.
- **Repository/runtime separation:** Repository completion authority grants no
  installation, deployment, runtime, service, timer, process, identity,
  permission, credential, network, firmware, device, database-migration,
  evidence, or physical-system authority.
- **Strategic direction:** The coordinated evidence is accepted as sufficient
  to establish repeated real aggregate AC-couple collapse and recovery for the
  initial baseline; no additional causal measurement is selected. The next
  task is planning a separately authorized repository-only ESP32 runtime and
  security hardening work unit, followed later by separately approved runtime
  verification and then a common telemetry/provenance contract.
- **Historical preservation:** Prior audit entries were not edited.
  `PROJECT_STATUS.md` now identifies its July 7 content as superseded and
  points to current authority while preserving full history in Git.
- **Untouched:** Source, tests, helper and runtime scripts, systemd files,
  collectors, analyzers, portal code/prototype/output, firmware, evidence,
  reports, databases, caches, backups, credentials, services, devices,
  networking, users/groups, permissions, and all runtime state.
- **Validation:** Complete diff and active-policy phrase review; current-state
  and next-task consistency checks; exact changed/staged-file review;
  sensitive-content, evidence, generated-artifact, and protected-path checks;
  `git diff --check`; repository health check; remote/upstream/divergence and
  normal-fast-forward verification; fetch-based post-push synchronization and
  independent published-commit verification.
- **Recovery:** Revert the single normal documentation commit. No operational
  or evidence rollback applies because no protected boundary was crossed.
- **Related commit and push:** The commit containing this entry is titled
  `Consolidate workflow authority and project direction`; one normal
  fast-forward push to `origin/main` is authorized after all safeguards pass.
- **Limitations:** This work records static collector observations only as
  candidates. It does not verify or implement ESP32 or SolarAssistant changes,
  automate safeguards in helper scripts, or authorize future implementation or
  runtime work.

## 2026-07-20T19:51:24Z — Plan ESP32 collector runtime hardening

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Convert the accepted ESP32 hardening direction into an
  implementation-ready repository plan while keeping repository implementation,
  installation, passive live verification, and persistent operation as four
  separately authorized phases.
- **Static verification:** Current source and focused tests confirm the fixed
  credentialless LAN HTTP endpoint and the absence of explicit redirect,
  environment-proxy, content-type, input-size, and permanent/transient HTTP
  handling. Allowlisting, exclusive output creation, raw-before-retained
  ordering, retained-writer isolation, and the default `esp32-frequency-v1`
  policy are already mitigated. Reconnect handling and logging are partially
  supported; installed runtime identity remains a runtime-phase fact.
- **Plan:** Added `docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md`, proposing the
  shared credentialless `solardt-telemetry` identity, administrator-owned code
  under `/opt/solar-digital-twin`, narrowly writable evidence under
  `/var/lib/solar-digital-twin/esp32`, explicit HTTP/SSE safeguards, preserved
  evidence semantics, a dormant service, an idempotent installer, acceptance
  gates, and nondestructive recovery.
- **Affected:** The new plan; `docs/ESP32_FORENSIC_TELEMETRY_PLAN.md`,
  `docs/ESP32_RETENTION_PRODUCTION_PLAN.md`, `docs/SECURITY_MODEL.md`,
  `PROJECT_INDEX.md`, `PROJECT_STATE.md`, `NEXT_TASK.md`, and this append-only
  audit entry.
- **Untouched:** Collector and retention source; tests; installers; systemd and
  helper scripts; firmware; ESPHome; runtime files; identities; ownership,
  permissions, ACLs, protected paths, services, processes, credentials,
  networks, devices, Home Assistant, evidence, reports, databases, generated
  artifacts, and retention behavior. No device was contacted and no capture
  was started.
- **Validation:** Complete source/test review and finding classification;
  focused offline ESP32 tests; complete documentation diff and phase-boundary
  review; sensitive-content, evidence, generated-artifact, and exact-file-scope
  checks; `git diff --check`; repository health; exact staged-file review; and
  remote/upstream/normal-fast-forward safeguards.
- **Recovery:** Revert the single normal documentation commit. No runtime or
  evidence rollback applies because this work only records a plan.
- **Related commit and push:** The commit containing this entry is titled
  `Plan ESP32 collector runtime hardening`; one normal fast-forward push to
  `origin/main` is authorized after all safeguards pass.
- **Limitations:** Actual installed identity, device response `Content-Type`,
  an appropriate input ceiling, and production resource limits require later
  focused implementation or separately approved runtime verification. The plan
  does not authorize or perform those phases.
