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

## 2026-07-20T20:11:46Z — Harden ESP32 collector runtime

- **Actor:** ChatGPT-directed Codex, authorized by Chris.
- **Purpose:** Implement the reviewed repository-only ESP32 collector, runtime
  installer, provenance launcher, and dormant-unit safeguards without
  installation, service action, device contact, capture, or evidence changes.
- **Collector:** Replaced the ambient Requests call with a dedicated
  proxy-independent session; rejects redirects; accepts only HTTP `200`;
  retries only `429`, `500`, `502`, `503`, `504`, and transport failures;
  validates compatible `text/event-stream`; limits each raw SSE line to 1 MiB
  through bounded 8 KiB chunk assembly; closes every response; and emits only
  fixed payload-free failure categories. Existing deadline/backoff, record,
  allowlist, timestamp, manifest, raw-first, retention-isolation, and policy
  semantics remain unchanged.
- **Evidence safety:** Exclusive output creation now applies file mode `0640`;
  newly created output directories use `0750`. Collision refusal, partial-run
  preservation, terminal manifests, and no-deletion behavior remain intact.
- **Runtime artifacts:** Added `scripts/install_esp32_runtime.sh` with
  side-effect-free `--check`, explicit `--install`, metadata-only `--verify`,
  unknown/shared-runtime refusal, whole-application archival rollback, optional
  explicit reporter selection, and no credential or device path. Added a
  finite installed-commit launcher and dormant
  `systemd/esp32-forensic-collector.service` with `Restart=no`, no timer, and no
  `[Install]` activation target.
- **Affected:** `src/solar_digital_twin/collectors/esp32_sse.py`,
  `tests/test_esp32_sse.py`, new `tests/test_esp32_runtime.py`, the two new
  scripts and unit above, the ESP32 hardening/telemetry/retention and security
  documents, `PROJECT_INDEX.md`, `PROJECT_STATE.md`, `NEXT_TASK.md`, and this
  append-only audit entry.
- **Validation:** 66 focused offline ESP32 tests and all 218 repository tests
  passed; installer `--check` was reviewed then run side-effect-free; shell
  syntax and Python compilation passed; complete diff, diagnostic, network,
  unit, credential, artifact, and exact-scope searches passed; `git diff
  --check` and repository health passed; publication safeguards and independent
  remote verification are required before completion.
- **Untouched:** Installed runtime and protected paths; users, groups,
  ownership, modes, ACLs, services, systemd state, timers, processes, packages,
  credentials, devices, Home Assistant, firmware, networks, evidence, reports,
  databases, generated artifacts, other collectors, portal behavior, and
  retention policy/defaults. No live network request or capture occurred.
- **Recovery:** Revert the single normal repository commit. No host or evidence
  rollback applies because installer installation/verification modes and the
  unit were not executed. Future installation has its own archive-first
  rollback and remains separately gated.
- **Related commit and push:** The commit containing this entry is titled
  `Harden ESP32 collector runtime`; one normal fast-forward push to
  `origin/main` is authorized after every canonical safeguard passes.
- **Limitations:** Actual device `Content-Type`, installed identity/path state,
  compatibility with the existing shared `/opt` runtime, reporter selection,
  and host resource headroom remain installation or passive-verification facts.
  The unit remains repository-only and dormant.

## 2026-07-20T21:09:23Z — Install dormant ESP32 runtime

- **Actor:** Chris operated the `solardt` terminal under a ChatGPT-directed,
  owner-authorized bounded installation; Codex synchronized this durable record.
- **Purpose:** Install the published credentialless ESP32 runtime and perform
  metadata-only verification while leaving device contact and persistent
  operation separately gated.
- **Installed source and runtime:** Commit
  `7f2274b9011c4bb85f3099eb80c8bb86a21f0e04` was installed as a tracked whole-
  application deployment at `/opt/solar-digital-twin`; its exact commit marker
  passed. The previous shared runtime is preserved at
  `/opt/solar-digital-twin.backup.20260720T205254Z`. Rollback was not invoked.
- **Identity and access:** Created system user/group `solardt-telemetry` with
  observed UID/GID `996/989`, `/nonexistent` home, `/usr/sbin/nologin`, and only
  its same-named primary group. Added trusted reporter `chris` to that group;
  reporter read/traverse passed and write was denied. Existing
  `solardt-telemetry-readers` was not modified or repurposed.
- **Paths and unit:** Created `/var/lib/solar-digital-twin/esp32` and its
  `evidence` directory as `solardt-telemetry:solardt-telemetry` mode `0750`.
  Installed `/etc/systemd/system/esp32-forensic-collector.service` as
  `root:root 0644`, performed the required daemon reload, and verified the unit
  exactly matched the repository artifact and remained static/inactive/dead.
  No timer, trigger, activation symlink, automatic-start path, or collector
  process existed.
- **Credential and evidence boundary:** No credential was created;
  `/etc/solar-digital-twin/esp32` was independently absent. Service evidence
  write access passed; reporter read passed and write was denied. Post-install
  evidence-file count was zero; no raw or retained evidence was created or
  modified.
- **Shared-runtime compatibility:** SolarAssistant collector and monitor local
  import/help validation passed. The temporary SolarAssistant monitor was
  already stopped by the VM reboot associated with the memory upgrade; it has
  no systemd service, was not restarted or modified, and its outage is unrelated
  to this installation. Completed capture evidence remains preserved.
- **Validation:** Repository preflight and installer `--check` passed; existing
  legacy runtime, archives, identity, unit, path, reporter, space, and inode
  state were reviewed; installer `--verify` passed; independent installed-
  commit, ownership/mode, access, unit-artifact, static/inactive, no-timer,
  no-process, no-evidence, no-credential-path, local import, repository HEAD,
  origin, divergence, and clean-tree checks passed.
- **Untouched:** ESP32 and all solar devices; services and tmux processes beyond
  the required unit registration; credentials and protected directories; raw
  evidence; firmware; networking; Home Assistant; databases; portal; collector
  and retention behavior. The ESP32 unit was not started or enabled, and no
  device was contacted.
- **Dependency observation:** The fresh virtual environment installed
  successfully, but pip warned that pinned `charset-normalizer==3.4.8` was a
  yanked version without a stated reason. This is unresolved dependency
  maintenance, not an installation failure.
- **Recovery:** The preserved timestamped shared-runtime archive is the rollback
  source. Any rollback, monitor restart, passive ESP32 verification, or
  persistent operation requires its own authorization; do not delete the
  archive or evidence.
- **Related commit and push:** The documentation commit containing this entry is
  titled `Record dormant ESP32 runtime installation`; one normal fast-forward
  push to `origin/main` is authorized after canonical safeguards pass.
- **Next gate:** Separately authorize one short, finite passive ESP32 live
  verification to record actual `Content-Type`, credentialless connectivity,
  output/provenance behavior, manifest closure, and clean stop. Persistent or
  long-duration operation remains a later owner decision.

## 2026-07-20T22:59:04Z — Verify installed ESP32 runtime passively

- **Actor:** Chris operated the `solardt` terminal under a ChatGPT-directed,
  owner-authorized bounded passive verification; Codex synchronized this
  durable record.
- **Purpose:** Verify the installed credentialless ESP32 runtime against the
  project-controlled passive SSE endpoint through one exact finite service run,
  without persistent activation or device/configuration change.
- **Compatibility probe:** A body-free Requests probe as `solardt-telemetry`
  contacted only `http://192.168.3.13/events`. It returned HTTP `200`, exact
  `Content-Type: text/event-stream`, the unchanged final URL, and zero redirects.
  No body, SSE payload, alternate destination, proxy, or credential was printed
  or retained.
- **Finite run:** The installed static
  `esp32-forensic-collector.service` started exactly once at 2026-07-20 16:42:07
  America/Chicago using the unchanged 3,600-second launcher, `current` mode,
  installed commit `7f2274b9011c4bb85f3099eb80c8bb86a21f0e04`, fixed evidence
  path, and `solardt-telemetry` identity. It completed at 17:42:08 with
  `Result=success`, main exit code/status 0/0, `NRestarts=0`, 9.599 seconds CPU,
  40.9 MiB peak memory, and zero swap.
- **Evidence:** Created exactly
  `esp32_sse_20260720_214207Z.ndjson` (12,983,085 bytes),
  `esp32_sse_20260720_214207Z_retained.ndjson` (12,550,203 bytes), and
  `esp32_sse_20260720_214207Z_manifest.ndjson` (748 bytes), all
  `solardt-telemetry:solardt-telemetry` mode `0640`. State/evidence directories
  remained mode `0750`; reporter `chris` could read but not write, and the
  service could not write installed code.
- **Content validation:** The manifest had exactly one start and one clean
  completion record with stop reason `duration`, installed collector version,
  current mode, and matching counts of 35,968 raw and 33,515 retained records.
  Every complete line parsed as JSON; expected schema, fixed source URL,
  17-entity allowlist, valid nondecreasing UTC receipt time, and ordered byte-
  identical retained subsequence checks passed. Policy remained
  `esp32-frequency-v1`; no conservative/canary output appeared; journal
  diagnostics remained payload-free.
- **Post-run state:** Service returned static/inactive/dead with zero restarts,
  processes, timers, triggers, activation paths, or credential paths. Installed
  commit and `/opt/solar-digital-twin.backup.20260720T205254Z` remained intact;
  repository `HEAD` and `origin/main` remained synchronized at
  `049d1ecc721c9460b73d10549ba58e01a8b72a3a` with a clean tree.
- **Operator observations:** The original shell retained stale supplementary-
  group state after adding `chris`; a fresh plain SSH login inherited the group
  and reporter checks passed without `newgrp`, permission, ACL, or group-design
  changes. Some oversized pasted blocks were duplicated or malformed, and one
  incomplete continuation was canceled with Ctrl+C. The systemd-supervised
  collector was unaffected. These observations motivated the canonical compact
  ChatGPT-authored command workflow now recorded in `CONTRIBUTING.md`.
- **Device ownership boundary:** The ESPHome forensic probe is project-
  controlled, but passive verification did not change it. Any coordinated
  firmware, entity, SSE, authentication, or network change requires a separate
  authorized and versioned ESPHome work unit.
- **Untouched:** Device configuration and firmware; credentials; identities,
  memberships, permissions, and ACLs; installed runtime and unit files; timers
  and persistent activation; SolarAssistant monitor; Home Assistant; network;
  databases; portal; retention code/default; and pre-existing evidence. No
  duplicate collector or tmux supervisor was created.
- **Recovery:** Preserve all three verification files as evidence. No runtime
  rollback is required. Any evidence change, persistent ESP32 operation, device
  change, or archive removal remains separately authorized.
- **Related commit and push:** The documentation commit containing this entry is
  titled `Record passive ESP32 runtime verification`; one normal fast-forward
  push to `origin/main` is authorized after canonical safeguards pass.
- **Next milestone:** Define the common telemetry observation, provenance,
  source-lineage, timestamp, freshness, availability, and normalization contract
  before production multi-source portal binding or reciprocal Home Assistant
  integration. Persistent ESP32 operation remains an unmade owner decision.

## 2026-07-20T23:30:43Z — Define telemetry observation contract

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  architecture and contract-design authorization.
- **Purpose:** Define one source-preserving common observation and provenance
  contract before adapters, normalized storage, portal binding, Home Assistant
  export, or any persistent ESP32 decision.
- **Affected:** New `docs/TELEMETRY_OBSERVATION_CONTRACT.md`; directly related
  project state, next task, index, Engineering Bible, source-role, Home
  Assistant interoperability, portal-design, and this append-only audit record.
- **Contract decisions:** Established stable metric versus observation identity;
  preserved root source, device, native metric, transport, evidence, and raw
  value/unit; separated source, receipt, observation, change, and derivation
  times; separated availability, validity, capability, and evaluated freshness;
  required non-destructive versioned normalization; required acyclic bounded
  parent lineage; prevented reflected Home Assistant exports from re-entering
  as independent evidence; and defined source-adapter acceptance gates.
- **Current semantics:** Inventoried distinct EG4 runtime/energy/day timestamp
  behavior, SolarAssistant response-level receipt time and battery scopes,
  ESP32 receipt-time SSE and policy-selected stream provenance, HA polling
  versus source-update cadence and unresolved hybrid lineage, current portal
  freshness, and offline `TimedRecord` limitations.
- **Untouched:** Source and test code; collectors and retention; schemas and
  databases; portal implementation/output; Home Assistant; runtime, installed
  paths, services, timers, processes, identities, permissions, credentials,
  evidence, reports, devices, ESPHome/firmware, packages, networking, and
  deployment. Persistent ESP32 operation remains undecided.
- **Validation:** Documentation/reference/terminology review, exact scope and
  artifact review, `git diff --check`, repository health check, shell syntax,
  Python compilation, and all 218 offline tests passed before publication.
- **Recovery:** Revert the single normal Git commit containing this entry;
  prior documents remain in normal Git history and no operational rollback is
  applicable.
- **Related commit and push:** The commit containing this entry is planned as
  `Define telemetry observation contract`; one normal fast-forward push to the
  expected `origin/main` is authorized after safeguards pass.
- **Limitations and review:** The contract is a published design proposal
  pending independent ChatGPT review and owner acceptance. Observation-ID
  generation, lineage digest format, storage layout, HA transport/attribute
  limits, historical backfill, adapter implementation order, and persistent
  ESP32 operation remain deferred.

## 2026-07-20T23:45:25Z — Clarify telemetry observation contract

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  correction authorization following independent ChatGPT review.
- **Purpose:** Resolve six narrow internal inconsistencies without changing the
  accepted architecture or authorizing implementation.
- **Affected:** `docs/TELEMETRY_OBSERVATION_CONTRACT.md`, `PROJECT_STATE.md`,
  `NEXT_TASK.md`, and this append-only audit entry.
- **Corrections:** Added record-profile applicability and scoped status;
  explicit derivation, window, and anchor times; a root-source metric-ID rule
  plus minimal machine-readable lineage hops; independent source-nature and
  result-nature classification; explicit raw-unit basis and versioned mapping;
  and fail-safe enum/version evolution rules. Synthetic examples now exercise
  point and window derivations, an anchored AC-couple event, source-supplied and
  adapter-specified units, corrected HA hybrid identity, and structured export
  lineage.
- **Review state:** The six findings are resolved, but the revised contract
  remains pending final independent ChatGPT review and explicit owner
  acceptance. No implementation is authorized by publication.
- **Untouched:** Source/test/schema/collector/retention/reporting/portal code;
  runtime, services, devices, Home Assistant, databases, evidence, credentials,
  firmware/ESPHome, networking, packages, installation, deployment, identities,
  permissions, and the parked `solardt` reboot/recovery procedure.
- **Validation:** Contract consistency searches, JSON parsing of all 12 worked
  examples, exact documentation scope, `git diff --check`, repository health,
  shell syntax, Python compilation, and all 218 offline tests passed.
- **Recovery:** Revert the single normal documentation commit. No operational
  rollback applies.
- **Related commit and push:** Planned subject `Clarify telemetry observation
  contract`; one normal fast-forward push to expected `origin/main` is
  authorized after safeguards pass.
- **Deferred:** Observation-ID generation, storage schema, lineage digest,
  adapter order, HA transport/attribute limits, backfill, portal/export work,
  persistent ESP32 operation, and reboot/recovery remain separate decisions.

## 2026-07-21T00:03:45Z — Record contract acceptance and Git publication modes

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  synchronization authorization with declared publication mode
  `commit-and-push`.
- **Owner decision:** Final independent ChatGPT review passed, after which Chris
  explicitly accepted `solar-digital-twin.telemetry-observation.v1` as the
  project's authoritative telemetry observation and provenance contract. No
  repository or runtime action occurred during the acceptance chat turn.
- **Purpose and change:** Changed the contract from proposed/pending to owner-
  accepted authority, advanced current work to source-adapter planning, and
  established three explicit Git publication modes plus missing-mode behavior
  in canonical workflow policy. Added concise ChatGPT, Codex, and startup-chain
  duties so fresh sessions select and enforce one mode.
- **Affected:** `docs/TELEMETRY_OBSERVATION_CONTRACT.md`, `PROJECT_STATE.md`,
  `NEXT_TASK.md`, `CONTRIBUTING.md`, `AI_PROMPT.md`, `AGENTS.md`,
  `START_HERE.md`, `PROJECT_INDEX.md`, concise acceptance-status references in
  `docs/Engineering_Bible.md`, `docs/TELEMETRY_SOURCE_ROLES.md`, and
  `docs/HOME_ASSISTANT_INTEROPERABILITY_PLAN.md`, and this append-only audit
  entry.
- **Publication policy:** `commit-and-push` permits validated exact staging, one
  normal commit, one fast-forward push, fetch/synchronization, and publication
  verification; `commit-only` stops after one validated local commit;
  `no-commit-or-push` prohibits staging, commit, and push. A missing declaration
  permits only clearly authorized read-only inspection and no write work.
- **Boundary:** A publication mode controls Git completion only and never
  expands substantive or operational authority. Destructive/exceptional Git
  remains gated, and platform confirmation does not change mode or scope.
- **Untouched:** Source, tests, adapters, schemas, collectors, retention,
  reporting/portal implementation, Home Assistant, runtime, services, timers,
  processes, VM state, databases, evidence, credentials, devices, firmware,
  ESPHome, networking, identities, permissions, installation, and deployment.
- **Validation:** Owner-acceptance and pending-wording searches, state/task
  consistency, publication-mode and missing-mode checks, startup-chain review,
  exact scope/artifact review, `git diff --check`, repository health, shell
  syntax, Python compilation, and all 218 offline tests passed.
- **Recovery:** Revert the single normal documentation commit. No operational
  rollback applies.
- **Related commit and push:** Planned subject `Record telemetry contract
  acceptance and Git modes`; selected mode authorizes one normal fast-forward
  push to expected `origin/main` after safeguards pass.
- **Deferred:** The HA-import `source.metric_id` fallback when only an HA entity
  ID is known remains an adapter-planning detail. The unscheduled `solardt` VM
  reboot/recovery procedure remains a separate future task covering service,
  collector, timer, dormant-unit, evidence-integrity, and recovery behavior.

## 2026-07-21T00:28:56Z — Plan telemetry source adapters

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  source-adapter planning authorization with publication mode `commit-only`.
- **Purpose:** Create the proposed authoritative implementation plan mapping
  current and planned telemetry sources into the owner-accepted
  `solar-digital-twin.telemetry-observation.v1` contract, compare candidate
  first implementation slices, and select one later offline-fixture slice.
- **Affected:** New `docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md`, `PROJECT_STATE.md`,
  `NEXT_TASK.md`, `PROJECT_INDEX.md`, concise authority references in
  `docs/Engineering_Bible.md` and `docs/TELEMETRY_SOURCE_ROLES.md`, and this
  append-only audit entry.
- **Proposed architecture:** Caller-supplied native records pass through
  source-specific parsing and validation into canonical observation, scoped
  status, or rejection envelopes. The plan keeps collection, evidence,
  adaptation, normalization, derivation, retention, storage, freshness,
  presentation, and Home Assistant transport separate. It proposes a small
  standard-library-first adapter protocol, immutable internal models,
  versioned metric/unit registries, structured source mappings, and concrete
  coverage for all sixteen contract acceptance gates.
- **Selected later slice:** A minimal shared envelope model/validator plus a
  SolarAssistant trusted combined-SOC adapter using synthetic poll fixtures.
  Production IDs remain injectable and unselected; implementation requires a
  separate authorization after review and acceptance.
- **Reuse findings:** Existing collectors and retention modules remain evidence
  producers and semantic references rather than canonical adapters. Parsing and
  timestamp helpers may be wrapped where stricter contract semantics are added.
  `TimedRecord` and forensic correlation adapters remain specialized
  compatibility consumers; later canonical integration requires equivalence
  tests and does not replace them in this milestone.
- **Untouched:** The accepted telemetry contract; source and test code;
  fixtures, schemas, collectors, retention, reports, portal and Home Assistant
  implementation; runtime, services, VM state, databases, evidence,
  credentials, devices, firmware, networking, identities, permissions,
  packages, installation, deployment, and persistent ESP32 operation.
- **Validation:** Exact plan/state/task/reference review, contract-unchanged and
  documentation-scope checks, all mapping/gate/candidate/selection checks,
  `git diff --check`, repository health, shell syntax, Python compilation, and
  all 218 canonical offline tests passed. The first sandboxed test invocation
  denied five loopback test-server binds; the unchanged suite passed when
  rerun with the already approved loopback-test capability.
- **Recovery:** Revert the single normal local documentation commit before any
  later publication, or use a later normal revert commit if separately
  published. No operational rollback applies.
- **Commit and publication:** Planned subject `Plan telemetry source adapters`.
  `commit-only` authorizes exact staging and one local commit; no push is
  authorized. The result remains available locally for independent ChatGPT
  review and a later separately authorized publication decision.
- **Review and deferred matters:** The plan and selected slice remain pending
  independent ChatGPT review and owner acceptance. Final HA-import
  `source.metric_id` fallback semantics and the unscheduled `solardt` VM
  reboot/recovery procedure remain explicit separate decisions, as do storage,
  migration, portal binding, HA export, and persistent ESP32 operation.

## 2026-07-21T00:55:11Z — Correct telemetry source adapter plan

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  correction authorization following independent ChatGPT review, with
  publication mode `commit-only`.
- **Review result:** Independent review found four narrow corrections. The
  overall adapter architecture and selected minimal shared validator plus
  synthetic SolarAssistant combined-SOC slice remain supported.
- **Review publication context:** The first planning commit was published only
  to temporary branch `review/telemetry-source-adapter-plan` for review;
  `origin/main` remained unchanged.
- **Corrections:** Separated SolarAssistant `jk_bms` acquisition identity from
  `solarassistant_rest_v1` transport; separated semantic `observation_id` from
  persisted-instance `record_id` algorithms and inputs; removed a redundant
  normalized SOC observation from the selected slice; separated future gate
  coverage from current Deferred production readiness; and reconciled project-
  state milestone wording.
- **Identity/copy semantics:** The selected valid record uses canonical metric
  `solarassistant.jk_bms.combined.state_of_charge`, system
  `solarassistant`, device `jk_bms_bank`, native metric
  `total/battery_state_of_charge`, authority role, and REST v1 transport. Raw
  and retained copies share one observation ID, use distinct record IDs, and
  differ only through copy-specific retention/evidence provenance.
- **Scope:** `docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md`, `PROJECT_STATE.md`, and
  this append-only audit entry only. The accepted contract, source, tests,
  fixtures, schemas, collectors, retention, reports, portal, Home Assistant,
  runtime, services, databases, evidence, credentials, devices, networking,
  permissions, and persistent ESP32 state remain untouched.
- **Validation:** Exact identity/transport, ID-boundary, copy semantics,
  root-only valid SOC, gate coverage/readiness, milestone, contract-unchanged,
  scope, artifact, documentation/reference, repository health, shell syntax,
  Python compilation, and all 218 canonical offline tests passed before the
  local correction commit.
- **Commit/publication:** Planned subject `Correct telemetry source adapter
  plan`. One normal local correction commit is authorized; no push or review-
  branch update is authorized. Re-review and separate publication authority
  remain required.
- **Recovery and deferred matters:** Revert the local correction commit before
  later publication, or use a later normal revert if separately published. HA
  fallback semantics, production ID encoding, adapter implementation, storage,
  portal/HA binding, reboot/recovery, and persistent ESP32 operation remain
  deferred.

## 2026-07-21T01:05:38Z — Clarify SolarAssistant JK telemetry namespace

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  clarification authorization with publication mode `commit-only`.
- **Purpose:** Clarify that `jk_bms` in canonical SolarAssistant metric IDs is
  a stable namespace for JK BMS telemetry reported by SolarAssistant, not a
  direct acquisition path or hardware connection.
- **Mapping preserved:** Canonical metric
  `solarassistant.jk_bms.combined.state_of_charge`, source system
  `solarassistant`, device `jk_bms_bank`, native metric
  `total/battery_state_of_charge`, authority role, and exclusive transport
  `solarassistant_rest_v1` remain unchanged.
- **Boundary:** Solar Digital Twin never polls or connects to either JK BMS
  directly. No direct JK protocol, address, credential, collector, polling,
  connection, or control path is planned or authorized.
- **Affected:** `docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md` and this append-only
  audit entry only. The accepted contract, source/tests, runtime, evidence,
  databases, credentials, services, devices, and all operational state remain
  untouched.
- **Validation/publication:** Exact namespace, mapping, direct-access
  prohibition, contract-unchanged, scope, `git diff --check`, and repository
  health checks passed before one local commit named `Clarify SolarAssistant JK
  telemetry namespace`. No push is authorized; independent re-review remains
  required.
- **Recovery:** Revert the local clarification commit before later publication,
  or use a later normal revert if separately published. No operational rollback
  applies.

## 2026-07-21T01:33:05Z — Record telemetry adapter plan acceptance

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  acceptance synchronization with publication mode `commit-and-push`.
- **Owner decision:** Independent ChatGPT review passed after the planning
  commit and two correction commits. Chris explicitly accepted the Telemetry
  Source Adapter Plan and its selected first synthetic-only implementation
  slice as the project's authoritative implementation plan. Acceptance does
  not authorize implementation automatically.
- **Purpose:** Change the plan from pending review to owner-accepted authority,
  synchronize project state and references, and advance the next task to
  preparing a bounded repository-only implementation request for the accepted
  SolarAssistant combined-SOC slice.
- **Affected:** `docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md`, `PROJECT_STATE.md`,
  `NEXT_TASK.md`, `PROJECT_INDEX.md`, `docs/Engineering_Bible.md`,
  `docs/TELEMETRY_SOURCE_ROLES.md`, and this append-only audit entry.
- **Boundary:** No adapter, source, tests, fixtures, contract, schema, storage,
  collector, retention, report, portal, Home Assistant, runtime, service,
  database, evidence, credential, device, firmware, network, permission, or
  persistent ESP32 change is authorized or performed. Preparing the next work
  request is distinct from authorizing its implementation.
- **Validation:** Acceptance/status consistency, stale pending-wording,
  state/task/reference, accepted-contract-unchanged, exact documentation scope,
  artifact exclusion, `git diff --check`, repository health, and documentation
  checks passed before staging. Exact staged scope and pre-push fast-forward
  safeguards remain required before publication.
- **Publication/recovery:** Planned subject `Record telemetry adapter plan
  acceptance`; one normal fast-forward push of local `main` to expected
  `origin/main` is authorized. Recovery is a later normal revert of this
  acceptance commit and, if needed, the preceding three plan commits; no
  operational rollback applies. The temporary review branch remains intact.
- **Deferred:** Production ID encoding, HA `source.metric_id` fallback, other
  adapters, storage/migration, portal/HA binding, reboot/recovery, and
  persistent ESP32 operation remain separate future decisions.

## 2026-07-21T02:59:47Z — Implement synthetic SolarAssistant SOC adapter

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  implementation authorization with publication mode `commit-and-push`.
- **Purpose:** Implement only the owner-accepted first synthetic slice: a
  minimal canonical telemetry model/validator, version-1 single-metric
  registry, small adapter/ID-provider protocols, SolarAssistant combined-SOC
  adapter, synthetic fixture, and focused offline tests.
- **Affected:** New `src/solar_digital_twin/telemetry/__init__.py`, `model.py`,
  `registry.py`, `adapters.py`, and `solarassistant_adapter.py`; new synthetic
  fixture `tests/fixtures/telemetry/solarassistant_combined_soc.json`; new
  `tests/test_telemetry_model.py` and `tests/test_solarassistant_adapter.py`;
  implementation-status updates in `PROJECT_STATE.md`, `NEXT_TASK.md`, and
  `docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md`; and this append-only audit entry.
- **Implementation:** Registry version 1 contains only
  `solarassistant.jk_bms.combined.state_of_charge`. One valid 0–100 numeric
  input produces one root source-value observation with equal raw/normalized
  percent values and no transformation or normalized product. Separate
  required injected providers distinguish semantic observation IDs from
  persisted record IDs; raw/retained copies share observation identity and
  have distinct record and evidence/retention provenance.
- **Safety and provenance:** SolarAssistant REST is the sole represented
  interface. No direct JK lineage/source/transport, production ID default,
  collector import, credential, network, file, database, evidence, storage, or
  runtime I/O exists. Distinct bounded rejection reasons cover missing, null,
  unknown, unavailable, malformed, numeric, unit, receipt-time, registry,
  provenance, retention, sequence, and injected-ID failures. One transport
  outage produces one source-scoped status.
- **Validation:** Synthetic fixture JSON parsing, Python compilation,
  `git diff --check`, repository health and exact scope/artifact checks passed;
  all 17 focused model/adapter tests and all 235 offline repository tests
  passed. Tests assert JSON compatibility, immutability, deterministic output,
  prohibited-profile fields, safe enum failure, no operational I/O, and exact
  source/identity behavior.
- **Boundary:** The accepted observation contract is unchanged. Other adapters,
  production ID encoding, storage/schema/migration, historical evidence,
  collectors/retention, portal, Home Assistant, runtime/services, credentials,
  devices, networking, deployment, and persistent ESP32 operation remain
  untouched and unauthorized.
- **Review/publication:** The implementation remains pending independent review
  and Deferred for production binding. Planned subject `Implement synthetic
  SolarAssistant SOC adapter`; one normal fast-forward push to expected
  `origin/main` is authorized after final staging and remote safeguards pass.
- **Recovery:** Revert the single normal implementation commit. No operational
  rollback applies because no operational state changed.

## 2026-07-21T03:15:59Z — Correct SolarAssistant SOC state handling

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  correction authorization with publication mode `commit-and-push`.
- **Purpose:** Resolve independent-review findings in the synthetic
  SolarAssistant combined-SOC slice: explicit null, `unknown`, and
  `unavailable` are valid source-state observations rather than rejections;
  missing and invalid inputs remain bounded rejections.
- **Affected:** `src/solar_digital_twin/telemetry/model.py`,
  `src/solar_digital_twin/telemetry/solarassistant_adapter.py`,
  `tests/test_telemetry_model.py`, `tests/test_solarassistant_adapter.py`,
  `PROJECT_STATE.md`, `NEXT_TASK.md`,
  `docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md`, and this append-only audit entry.
- **Correction:** State observations preserve raw null or raw source strings,
  source-supplied percent-unit provenance, state nature, valid/supported axes,
  explicit availability, null normalized values and transformations, and
  stable payload-free reasons. Raw/retained state copies retain one semantic
  observation ID with separate record/evidence/retention provenance. The
  minimal validator now distinguishes absent required-null fields from present
  nulls and rejects observation/value/state/retention fields prohibited on the
  implemented source-status profile.
- **Validation:** The accepted contract blob remained
  `9be6fd270d23d9ebea27f5d38bcbca7e0f37408f`; 21 focused tests and all 239
  offline repository tests passed, along with Python compilation. The first
  full-suite attempt was blocked only by sandbox denial of five loopback test
  sockets; the identical authorized suite passed when permitted to bind its
  localhost-only ephemeral test server. Final repository health, diff, scope,
  artifact, staging, remote, and publication safeguards remain required.
- **Boundary:** No live collector, direct JK path, runtime, service, evidence,
  database, credential, storage/migration, portal, Home Assistant, device,
  network, deployment, or persistent ESP32 action was introduced or performed.
  The corrected synthetic slice remains Deferred for production binding and
  pending independent review.
- **Publication/recovery:** Planned subject `Correct SolarAssistant SOC state
  handling`; one normal fast-forward push to expected `origin/main` is
  authorized after final safeguards pass. Recovery is a later normal revert of
  this correction commit followed, only if necessary, by a normal revert of
  the original implementation commit. No operational rollback applies.

## 2026-07-21T03:46:29Z — Reject mixed root/status profiles

- **Actor and authorization:** Codex, under Chris's bounded repository-only
  correction authorization with publication mode `commit-and-push`.
- **Finding and correction:** Independent review found that the root validator
  accepted a mixed profile containing a top-level `status` field even though
  the source-status validator already rejects observation-profile fields. The
  root path now rejects top-level `status` with bounded reason
  `invalid_root_profile`, covered within an existing focused test method.
- **Affected:** `src/solar_digital_twin/telemetry/model.py`,
  `tests/test_telemetry_model.py`, and this append-only audit entry.
- **Validation and boundary:** The 21 focused tests, all 239 offline repository
  tests, `git diff --check`, repository health, exact three-file scope, and the
  unchanged telemetry-contract blob are required before publication. Numeric
  and explicit-state behavior, the adapter, fixtures, registry, identity,
  documentation status, and next task remain unchanged. No production binding,
  runtime, service, evidence, database, credential, portal, network, device, or
  operational action occurred.
- **Publication and recovery:** Planned subject `Reject mixed root status
  profiles`; publish once by normal fast-forward to expected `origin/main`
  after all safeguards pass. Recovery is a later normal revert of this
  correction commit. No operational rollback applies.

## 2026-07-21T03:52:47Z — Accept synthetic SolarAssistant SOC adapter

- **Decision:** Independent ChatGPT review passed, and Chris explicitly
  accepted the corrected synthetic SolarAssistant combined-SOC implementation
  as a completed offline source-adapter slice.
- **Accepted commits:** `fa225d58a4108fa08955210276480127ff442869`
  (initial implementation), `d5868054d0582c5cffa9fae42b03e57bc3e10bb8`
  (explicit-state and validator correction), and
  `54df732adb854f0de9a971bdf21ae56f0750c46e` (mixed root/status correction).
- **Documentation-only scope:** Updated `PROJECT_STATE.md`, `NEXT_TASK.md`,
  `docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md`, and this append-only audit entry to
  record acceptance and make selection and planning of the next
  telemetry-contract milestone the active task.
- **Boundary:** Acceptance does not authorize production IDs or binding,
  storage/schema or historical adaptation, live SolarAssistant or JK access,
  collectors, retention, evidence, runtime, services, deployment, portal, Home
  Assistant, devices, or network action. No code, test, fixture, contract,
  dependency, generated, database, credential, or operational state changed.
- **Publication and recovery:** Publish this documentation-only acceptance as
  one normal fast-forward commit with subject `Accept synthetic SolarAssistant
  SOC adapter`. Recovery is a later normal revert of this documentation commit
  only; no operational rollback applies.

## 2026-07-22T02:04:15Z — ESP32 endurance capture integrity closure

- **Actor and authorization:** Chris authorized the finite passive endurance
  capture separately; ChatGPT-directed Codex performed bounded read-only
  integrity review and this documentation-only closure with publication mode
  `commit-and-push`.
- **Operational record:** Transient unit
  `esp32-forensic-overnight-20260721.service` created immutable capture
  `esp32_sse_20260721_041439Z` from `2026-07-21T04:14:39.139Z` through
  `2026-07-21T16:00:01.177Z` using collector
  `7f2274b9011c4bb85f3099eb80c8bb86a21f0e04`, current retention mode, and
  `esp32-frequency-v1`. It wrote 422,744 raw records, 391,241 retained records,
  and a two-record manifest, then stopped normally for duration.
- **Integrity and decision:** JSON, counts, canonical nondecreasing UTC,
  final-newline state, fixed source, all 17 approved IDs, byte-identical ordered
  retention, complete manifest, stable pre/post SHA-256 identities, restrictive
  ownership/modes, and deterministic retention replay passed. Chris accepted
  the result as **PASS WITH ONE QUALIFICATION** and suitable for later forensic
  analysis. The complete record is
  `docs/capture_analyses/esp32_sse_20260721_041439Z-integrity.md`.
- **Qualification and reconciliation:** Systemd ignored `RuntimeMaxSec` because
  the transient unit used `Type=oneshot`; the collector's finite `--duration`
  nevertheless completed normally. Host ownership is correctly
  `solardt-telemetry:solardt-telemetry` mode `0640`; the earlier
  `nobody:nogroup` view was only Bubblewrap overflow-ID mapping, not a file or
  permission anomaly.
- **Documentation-only scope:** Created the integrity report and updated
  `docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md`, `PROJECT_STATE.md`,
  `PROJECT_INDEX.md`, and this append-only audit entry. No evidence content,
  source, tests, dependencies, runtime, services, timers, permissions,
  credentials, devices, networking, or selected telemetry-contract next task
  changed. No persistent service or timer was created or authorized.
- **Publication and recovery:** Publish one normal fast-forward commit titled
  `Record ESP32 endurance capture integrity`. Recovery is a later normal revert
  of this documentation commit only; preserve the evidence unchanged. No
  operational rollback applies.

## 2026-07-22T02:22:13Z — Conversation modes and telemetry interpretation

- **Actor and authorization:** ChatGPT-directed Codex, under Chris's bounded
  documentation-only authorization with publication mode `commit-and-push`.
- **Workflow:** Defined persistent Discussion Mode and Work Mode for
  Chris–ChatGPT conversation, their explicit transitions and safe default, the
  complete Codex request-and-review cycle, and the Owner/Admin Step format.
  Kept conversation modes distinct from the existing Git publication modes and
  preserved all risk and protected-action controls.
- **Source interpretation:** Recorded the qualified operator/developer-reported
  explanation that SolarAssistant's EG4 aggregate AC-use display may include
  AC-coupled solar contribution. The native metric retains provenance and an
  explicit source-semantic label; candidate household-load subtraction is not
  approved or implemented. Deferred log analysis must establish applicability,
  timing, provenance, and labels first.
- **Operating context:** Preserved Chris's July 21 cloudless-condition,
  no-export, overnight grid-use, battery-charging, and solar-dip observations
  for future synchronized correlation, separately identifying his comparison
  with prior 6000XP behavior as a hypothesis. No causal conclusion, component
  failure finding, or warranty determination was made.
- **Affected and untouched:** Documentation only: `CONTRIBUTING.md`,
  `AI_PROMPT.md`, `START_HERE.md`,
  `docs/SOLARASSISTANT_TELEMETRY_PLAN.md`, `BACKLOG.md`,
  `docs/EG4_FORENSIC_CORRELATION.md`, `PROJECT_STATE.md`, and this audit. The
  existing Engineering Bible mission was adequate and unchanged. `NEXT_TASK.md`,
  source, tests, evidence, telemetry behavior, databases, credentials,
  permissions, runtime, services, devices, and networking remained unchanged.
- **Validation, publication, and recovery:** Documentation consistency, exact
  scope, unchanged `NEXT_TASK.md`, `git diff --check`, and repository health
  must pass before one normal fast-forward commit titled `Document work modes
  and telemetry interpretation`. Recovery is a later normal revert of this
  documentation commit; no operational rollback applies.

## 2026-07-22T04:05:10Z — Accept solar-collapse forensic investigation direction

- **Actor and authorization:** ChatGPT-directed Codex under Chris's bounded
  documentation-only authorization with publication mode
  `no-commit-or-push`.
- **Decision:** Centralized the accepted abrupt daytime solar-collapse
  investigation semantics in `docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md`:
  SolarAssistant-triggered collapse/recovery after exact metric review,
  configurable 2-minute/250 W/90%/50 W/30-second research defaults,
  solar-day/case/episode/relapse behavior, extendable 20-minute recovery
  windows, multi-source electrical and environmental context, recovery
  descriptions, competing hypotheses, and future Forensics controls.
- **ESP32 correction:** Recorded that the synthetic generator-frequency root
  adapter must retain every finite approved-source value, including reported
  multiples/harmonics and 5,000/30,000 Hz extremes. Firmware frequency
  thresholds are analysis thresholds, not validity limits; surprising values
  do not automatically prove the AC fundamental.
- **Milestones:** Made the synthetic ESP32 generator-frequency root adapter the
  next bounded implementation, followed by final source-neutral event
  specification, synthetic detector, separately approved historical analysis,
  and only later live detection, portal controls, nighttime characterization,
  and weather integrations.
- **Boundary:** Documentation only. No source, tests, adapter, detector,
  collector, evidence, database, credential, runtime, service, timer, portal,
  Home Assistant, Volcast, weather, device, firmware, permission, or network
  state changed or was accessed. No causal, safety, code, or warranty finding
  was made. Recovery is a normal revert of the eventual documentation commit;
  no operational rollback applies.

## 2026-07-23T16:45:30Z — Implement synthetic ESP32 frequency adapter

- **Actor and authorization:** ChatGPT-directed Codex under Chris's bounded
  repository-only authorization with publication mode `commit-and-push`.
- **Implementation:** Added one I/O-free adapter for exact ESPHome entity
  `sensor-01_gen_frequency`, canonical metric
  `esp32.esphome.forensic_probe.generator_frequency`, ESP32
  `forensic_probe`/forensic/HTTP-SSE identity, receipt-only time, and exact root
  lineage. Registry version `1` now has exactly the accepted SolarAssistant SOC
  and ESP32 frequency entries; the minimal validator dispatches strict exact
  profiles and rejects cross-source substitutions.
- **Value and provenance:** Every finite integer or float remains valid without
  electrical plausibility limits, clipping, correction, or suppression.
  Adapter-specified `Hz` uses mapping
  `esp32.esphome.sensor-01_gen_frequency.unit` version `1`.
  `value.raw` remains the original collector `value`, while validated
  `evidence.source_fields` losslessly preserves the separate raw `value` and
  `state`. Caller-supplied semantic occurrence identity distinguishes equal
  timestamps and remains independent of copy-local retention/evidence.
- **Tests and files:** Added the adapter, one synthetic fixture, and focused
  tests; narrowly generalized the model, registry, exports, model tests, and
  registry expectation in the accepted SolarAssistant tests. Updated
  `PROJECT_STATE.md`, `NEXT_TASK.md`,
  `docs/TELEMETRY_SOURCE_ADAPTER_PLAN.md`, `PROJECT_INDEX.md`, and this audit.
  All 33 focused telemetry tests and all 251 offline repository tests passed.
- **Status and boundary:** Implementation is pending independent ChatGPT/owner
  review and is not owner-accepted. Production gate 16 remains Deferred.
  Production IDs, storage, migration/backfill, historical/operational evidence,
  collectors, retention, firmware, devices, runtime, services, credentials,
  databases, portal, Home Assistant, weather, and collapse detection were not
  accessed or changed.
- **Publication and recovery:** Planned subject `Add synthetic ESP32 frequency
  adapter`; one normal fast-forward push to `origin/main` is authorized after
  final safeguards. Recovery is a normal revert of this one repository commit;
  no operational rollback applies.

## 2026-07-23T16:55:48Z — Correct ESP32 frequency adapter semantics

- **Actor and authorization:** ChatGPT-directed Codex under Chris's bounded
  repository-only correction authorization with publication mode
  `commit-and-push`.
- **Identity correction:** Removed stream-local `ingest_sequence` from the
  observation-ID descriptor. Raw, current-retained, and
  conservative-retained copies with one source occurrence and receipt time now
  pass identical semantic descriptors despite different per-record ingest
  positions; record IDs and copy provenance remain distinct.
- **Normalization correction:** Changed only the ESP32 generator-frequency
  registry profile to `result_nature=normalized_source_value`. Its exact
  adapter-specified Hz mapping remains version `1`, numeric raw and normalized
  values remain equal, and quality now includes `normalized` in accepted order.
  SolarAssistant remains `source_value` with source-supplied percent and its
  unchanged quality categories.
- **Validation and status:** All 33 focused telemetry tests and all 251 offline
  repository tests passed. The implementation remains pending independent
  ChatGPT/owner review and is not owner-accepted. Production gate 16 remains
  Deferred.
- **Boundary and recovery:** No production IDs, storage, evidence, collectors,
  retention implementation, runtime, devices, credentials, database, portal,
  Home Assistant, weather, or collapse detection changed or was accessed.
  Recovery is a normal revert of the correction commit with no operational
  rollback.
- **Publication:** Planned subject `Correct ESP32 frequency adapter semantics`;
  one normal fast-forward push to `origin/main` is authorized after final
  safeguards.

## 2026-07-23T17:03:21Z — Accept synthetic ESP32 frequency adapter

- **Owner acceptance:** After independent ChatGPT review, Chris explicitly
  owner-accepted the corrected synthetic ESP32 generator-frequency adapter
  sequence: `64949db0ec5b65443679fa3a05c744d820274e81` (`Add synthetic
  ESP32 frequency adapter`) and
  `efa6fe453bc2b0184aba7f235bf830f89bb85aa0` (`Correct ESP32 frequency
  adapter semantics`).
- **Review and validation:** Review confirmed exact registry/source/lineage,
  lossless raw `value` and `state`, unrestricted finite values, versioned
  adapter-specified Hz normalization, source-occurrence/copy identity,
  strict cross-source validation, unchanged SolarAssistant behavior, and no
  operational I/O. All 33 focused telemetry tests and all 251 offline tests,
  compilation, diff checks, and repository health passed for the accepted
  implementation sequence.
- **Scope and boundary:** Documentation only. Acceptance closes the synthetic
  offline adapter milestone and does not grant production IDs or binding,
  storage, historical adaptation, collector/retention, runtime, service,
  device, firmware, network, evidence, database, portal, Home Assistant,
  weather, or collapse-detection authority. Production gate 16 remains
  Deferred.
- **Next milestone:** Advance to source-neutral solar-collapse event
  specification and the unresolved prerequisite for exact SolarAssistant
  solar-production trigger identity; do not substitute the ambiguous aggregate
  AC-use/load field or contact live sources in this work unit.
- **Publication and recovery:** Planned subject `Accept synthetic ESP32
  frequency adapter`; one normal fast-forward push to `origin/main` is
  authorized after documentation checks. Recovery is a normal revert of this
  acceptance documentation commit or the applicable implementation/correction
  commit; no operational rollback applies.

## 2026-07-23T17:23:46Z — Finalize source-neutral solar-collapse event plan

- **Actor and authorization:** ChatGPT-directed Codex under Chris's bounded
  documentation/planning-only authorization with publication mode
  `no-commit-or-push`; all changes remain unstaged for review.
- **Repository conclusion:** Tracked approved SolarAssistant material
  establishes the battery-only `GET /api/v1/metrics` family and combined-SOC
  slice but not an exact AC-coupled solar-production topic, scope, unit, sign,
  quantity, exclusions, state behavior, or provenance. Trigger binding remains
  `solar_production_trigger_metric`; no ambiguous aggregate field was
  substituted. One later read-only inventory and narrowly sanitized candidate
  fixture are proposed but not authorized.
- **Specification:** Refined
  `docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md` as the single detailed
  authority. Before this planning work, Chris replaced the earlier
  approximately 250 W research default with a 1,500 W immediate two-minute
  median requirement for creating a new primary episode. Valid lower-baseline
  declines remain subthreshold observations, while lower-power recovery and
  relapse remain evidence inside an already qualified episode. The threshold
  is not a physical, safety, equipment, manufacturer, or regulatory limit.
- **Scope and status:** Updated `PROJECT_STATE.md`, `NEXT_TASK.md`,
  `docs/SOLARASSISTANT_TELEMETRY_PLAN.md`, and
  `docs/PORTAL_UI_DESIGN.md` for the unresolved prerequisite, independent
  review task, and versioned 1,500 W portal default. No source, test, fixture,
  collector, retention, evidence, storage, runtime, service, device,
  credential, network, detector, or portal implementation changed or was
  accessed. Production gate 16 remains Deferred.
- **Validation and recovery:** Repository-local documentation checks include
  diff whitespace, repository health/reference checks, credential-pattern and
  exact-file review, and searches for obsolete active threshold defaults and
  low-output qualifying examples. Recovery is a normal revert of a future
  documentation commit; no operational rollback applies.

## 2026-07-23T20:15:32Z — Adopt milestone authorization governance draft

- **Decision:** Chris adopted coherent milestone authorization in place of
  routine small-step approval. One bounded milestone approval covers every
  explicitly included design, implementation, validation, correction,
  documentation, analysis, operational, and publication activity through
  completion, while consequential owner decisions and protected boundaries
  remain gated.
- **Read-only and credential policy:** Added task-local standing authenticated
  read-only authority using existing approved credentials/runtime identities,
  including behaviorally read-only use of a broader-capability credential when
  necessary. Non-disruption, least exposure, limited authentication attempts,
  protected temporary handling, sanitized access records, and strict
  public/accidental-disclosure prevention remain mandatory.
- **Boundaries and workflow:** Preserved immediate owner gates for public/WAN
  exposure, physical/safety control, inverter/battery configuration,
  destructive evidence/database/Git activity, credential disclosure/movement/
  permission weakening, major cost, and consequential architecture. Added
  exact known-dirty-tree handling, milestone-level review, and either one final
  commit or an explicitly authorized bounded logical series followed by one
  normal push.
- **Files and transitional state:** Governance edits changed
  `CONTRIBUTING.md`, `AGENTS.md`, `AI_PROMPT.md`, `TEAM.md`, and
  `START_HERE.md`, plus this append-only entry. The six-file solar-collapse
  planning draft was preserved as the known pre-existing unstaged state; its
  five other files were not edited during governance work.
- **Operational/publication boundary and recovery:** No credential, live
  source, protected runtime, device, service, database, evidence, or other
  operational access occurred. Nothing was staged, committed, or pushed.
  After eventual publication, recovery is a normal Git revert of the
  governance commit; no operational rollback applies.

## 2026-07-24T04:05:24Z — Plan reusable solar-collapse calibration

- **Owner decisions and architecture:** Chris retained the owner-selected
  1,500 W immediate two-minute median for a new primary episode and required a
  reusable production-shaped calibration path. Canonical append-only
  collection is separate from non-mutating rerunnable analysis; pilot,
  calibration, reanalysis, shadow validation, and production forensics reuse
  the same source adapters, evidence, lifecycle, checkpoint, weather,
  reporting, prompt, and portal foundations.
- **Intervals and learning:** Analysis supports one through 30 days with
  convenient one-, three-, seven-, 14-, and 30-day selections; the initial
  pilot is approximately three days and must not silently overrun. Calibration
  seeks clear and variable-weather conditions, uses robust distributions, and
  excludes suspected failures from normal-envelope training without deleting
  them from forensic evidence.
- **Context and checkpoints:** KVBT begins with the pilot as nearby ambient
  context approximately 0.5 to 1 kilometre away, never an electrical veto or
  panel irradiance sensor. Volcast is optional and non-blocking. Durable
  checkpoints occur at least every five minutes and on pause/stop/completion,
  preserving run state, per-source success, counts, gaps, freshness, storage,
  configuration, candidates, and interruption history.
- **Recovery, portal, and prompts:** Defined explicit run lifecycle,
  pause/resume/stop, incomplete-run and partial-report behavior, and honest
  unavailable interruption gaps. The planned LAN-only unprivileged portal
  reuses existing architecture for narrow lifecycle, checkpoint, reporting,
  interval, threshold-comparison, and sanitized prompt controls without shell,
  credential, raw authenticated response, device control, or WAN access.
- **Trigger and threshold status:** Exact SolarAssistant AC-coupled production
  remains **Conclusion B — Unresolved**; no friendly name, Home Assistant
  entity, or ambiguous AC-use/load field was substituted. Standing
  authenticated read-only authority may support the next separately
  owner-authorized inventory. Threshold recommendations remain versioned and
  require owner acceptance; lower-power in-episode recovery/relapse and
  subthreshold preservation remain unchanged.
- **Files, validation, boundary, and recovery:** Refined
  `docs/SOLAR_COLLAPSE_FORENSIC_EVENT_PLAN.md`,
  `docs/SOLARASSISTANT_TELEMETRY_PLAN.md`,
  `docs/PORTAL_UI_DESIGN.md`, `PROJECT_STATE.md`, `NEXT_TASK.md`,
  `SESSION_END.md`, `docs/operations/VM_HEALTH_LOG.md`, and this audit.
  Repository-local documentation, reference, disclosure, threshold, role, and
  diff checks apply before publication. No credential, live source, protected
  runtime, device, service, timer, evidence, database, collector, retention,
  deployment, capture, network, or portal operation occurred. Publication uses
  the authorized normal commit plan and one fast-forward push; repository
  recovery is a normal Git revert with no operational rollback.
