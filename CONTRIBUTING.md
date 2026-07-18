# Solar Digital Twin Development and Risk Policy

`TEAM.md` defines project roles. This document is authoritative for workflow,
risk classification, approvals, preservation, audit, commits, and pushes.

## Working method

- Use small, bounded, reviewable work units and evidence over opinion.
- Inspect repository state before editing and preserve working behavior.
- Test before committing and keep `main` clean at completed checkpoints.
- Update directly related authoritative documentation with validated work.
- Keep logs and diffs concise; do not ask Chris to review raw code as the main
  quality gate.
- Put deferred ideas in `BACKLOG.md` or the applicable non-authoritative ideas
  document only when the work unit authorizes that edit.
- Stop scope drift and return to the current objective.

## Practical risk and security

Risk is managed, not eliminated. Security protects credentials, evidence,
recovery options, and the physical system without unnecessarily blocking
ordinary reporting and analysis. Read-only telemetry is lower risk than
credentials, configuration, control, or destructive actions. Reversible
actions require less friction than irreversible ones. Delay, manual burden,
and excess complexity are also project risks.

Use strong home-lab and engineering basics proportional to plausible harm, not
bank, military, intelligence, classified-system, or large-enterprise process
unless a specific threat justifies it. Preserve strong controls for credentials,
tokens, authorization headers, device control, evidence integrity, public
network exposure, destructive Git operations, major physical changes,
expensive purchases, recovery, and rollback.

Secrets must remain outside Git, repository documentation, chat, logs, reports,
command arguments, shell history, and ordinary backups.

## Authority and approval classes

ChatGPT classifies actions by actual risk and explains material risk plainly.

### Standing bounded-work authority

After Chris authorizes a bounded objective, ChatGPT may direct Codex through
the complete work cycle without repeated approval: authorized reads and
telemetry inspection, in-scope edits, tests, corrections, validation, related
documentation, exact staging, and the validated local commit.

### Standing read-only authority

Ordinary read-only repository inspection, non-secret telemetry, completed
evidence, generated reports, metadata and hashes, strict read-only database
queries, approved local health endpoints, bounded offline analysis, and public
technical documentation generally require no separate prompt. Limit access to
what is relevant; avoid secrets, tokens, unrelated private files,
authorization headers, process memory, and huge unnecessary dumps.

### One-approval operations

One plain-language explanation and one approval covers the complete bounded
implementation, correction, validation, and rollback sequence for package
installation; user/group/ACL or narrow permission changes; operational service
configuration or restart; deployment; a new live capture; controlled evidence
copying; firmware installation; database migration; or approved live device
configuration. Ask again only if scope or risk materially expands.

### Always-gated operations

Chris's explicit approval is required immediately before force-push; reset,
rebase, history rewriting, or destructive Git operations; permanent evidence
deletion or rewriting; credential/token disclosure, movement, or permission
weakening; broad recursive permission changes; firewall or public-exposure
changes; power/safety device control; inverter or battery configuration;
firmware flashing without an approved recovery path; physical electrical
changes; major purchases or architecture replacement; or an action materially
riskier than the authorized work unit.

Proceed when work is routine, bounded, reversible, and authorized. Stop and ask
Chris when uncertainty could materially affect physical safety, evidence
integrity, credentials, availability, recovery, major cost, or project
direction.

## Manual operation and bounded Codex workflow

This section is canonical for the distinction between actions Chris performs
and work Codex performs locally.

### Manual operation by Chris

“One actionable step at a time” primarily governs commands or consequential
actions Chris must personally perform. Give one clear actionable step, name the
exact host and shell, and pause for the observed result when the next action
depends on it. ChatGPT remains responsible for routine software-engineering
judgment; do not transfer that burden to Chris.

### Complete bounded Codex work units

Codex operates under one complete bounded work unit at a time. Once Chris
authorizes it, Codex proceeds uninterrupted through every activity explicitly
included in that unit. This may include authorized repository reads and
inspection, in-scope edits, temporary non-evidence working files, tests,
linters, repository health checks, validation, directly related documentation,
staging only the approved files, a specifically authorized local commit, and a
normal push when the work unit expressly authorizes it.

Codex must not request repeated permission for an already-authorized activity.
Chris should not be placed in a routine “press Y” role after ChatGPT has already
classified the action, scope, and safeguards. This autonomy never expands the
work unit or bypasses execution-environment security controls.

### Escalation boundary

Codex stops and returns the exact condition when:

- an action exceeds or conflicts with the work unit, or material ambiguity or
  scope expansion invalidates the plan;
- the repository is unexpectedly dirty, divergent, on the wrong checkpoint,
  or contains unexpected files or behavior;
- software installation is required;
- an unapproved service, timer, process, runtime, network, VM, deployment,
  collector, or production-retention change is required;
- credentials, tokens, authorization headers, or protected secrets would need
  handling;
- raw evidence would be modified, deleted, normalized in place, or overwritten;
- a database migration or destructive database operation is required;
- an unapproved commit or push, or any amend, reset, rebase, merge, force-push,
  destructive Git action, or history rewrite is required; or
- continuing would otherwise become unsafe or materially ambiguous.

Chris returns the exact stopped request and surrounding context to ChatGPT.
ChatGPT decides whether proceeding is appropriate and, when needed, prepares a
revised bounded authorization. Codex does not improvise beyond the boundary.

### Interface-enforced confirmations

The Codex execution environment may display a mandatory platform confirmation
even when the bounded work unit already authorizes the exact action. Such a
prompt is an interface control, not a request for Chris to make a new technical
decision. Codex may use it only when the displayed action exactly matches the
authorized activity and may not broaden the action because confirmation is
available.

A confirmation involving broader filesystem access, installation, credentials,
services, runtime changes, destructive Git activity, or another protected
boundary requires stopping and escalation unless that exact activity is
explicitly authorized. Project policy does not bypass platform controls.

### Reviewability and durable records

Review uses the available combination of the original bounded request, Codex's
compact completion report, Git status/diff/history and remote synchronization,
test and repository-health results, the Codex session or activity record, and
append-only `CHANGE_AUDIT.md` entries for persistent changes. Together these
show whether Codex remained within authorization.

Interface and session history may be transient. It is not durable project
evidence unless a documented retention mechanism preserves it. Git and the
repository audit are the durable project records; evidence-specific provenance
remains governed by its own immutable records.

## Preservation: archive instead of delete

Preserve project information rather than permanently deleting it as routine
work. This includes source, documentation, configuration, evidence, databases,
reports, operational logs, analysis results, firmware, scripts, service and
device configuration, backups, and governance records.

When active material is obsolete or superseded, verify its replacement, then
archive it with its original name where practical, a UTC timestamp or unique
identifier when useful, the reason, replacement, ownership/permissions, and
enough context to restore or compare it. Never silently discard information
needed for troubleshooting, rollback, evidence, audit, warranty escalation,
recovery, or decision history. When uncertain, archive.

Raw evidence is immutable: never overwrite, normalize in place, rewrite, or
discard it. For Git-tracked material, a reviewed normal commit may remove an
active file when Git history preserves it and `CHANGE_AUDIT.md` records the
change. Temporary bounded-work files belong under `/tmp` and may expire through
normal operating-system cleanup; do not label unique artifacts as temporary to
delete them.

Unique operational artifacts outside Git require an appropriate archive or
backup. Storage pressure is not authorization to delete raw evidence. Address
capacity through safe archiving, approved additional storage, relocation of
reproducible derived products, reviewed retention changes, or another
documented capacity plan. Do not create elaborate duplicate archives for
ordinary tracked material already recoverable through Git history.

## Append-only change audit

`CHANGE_AUDIT.md` is the authoritative append-only record of persistent
changes. Git history supplements but does not replace it because packages,
permissions, services, devices, networks, and runtime can change outside Git.

Every persistent-change work unit appends an entry before completion. Never
silently edit or remove an existing entry; correct it with a later entry that
references the original. Include, where applicable: UTC time, actor, purpose,
affected files or components, change and reason, explicitly untouched scope,
validation/tests, recovery or rollback, archive/backup location, related commit
and push state, and unresolved risks or limitations.

Routine read-only inspection needs no audit entry unless it produces a
significant engineering finding or persistent report. Creating the audit entry
for a work unit does not recursively require another entry. Audit entries must
never contain passwords, tokens, API keys, authorization headers, credential
contents, secret arguments, or sensitive runtime output.

## Git and milestone synchronization

A validated local commit is part of an authorized bounded work unit. Codex
stages only validated in-scope files. Prefer one tested commit per logical
change. Pushes occur at clean milestone boundaries under project-lead direction,
are never forceful under routine authority, and are followed by local/remote
synchronization verification. Destructive or exceptional Git operations remain
always gated.

## Recovery

Back up or archive before significant changes, preserve known-good versions,
and define rollback in the work unit. Direct device access and recovery must
not depend on a collector. Prefer reversible steps and verify replacements
before retiring prior versions.

## VM and operational health

Follow the read-only schedule, observations, thresholds, and append-only entry
format in `docs/operations/VM_HEALTH_LOG.md`. A normal health review is recorded
there, not duplicated in `CHANGE_AUDIT.md`. Any persistent corrective action
resulting from it receives a change-audit entry. Do not broaden a health review
into invasive inspection or automatic remediation.
