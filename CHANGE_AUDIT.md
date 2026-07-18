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
