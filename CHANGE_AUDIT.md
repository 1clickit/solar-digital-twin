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
