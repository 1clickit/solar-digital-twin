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

After an approved persistent host or runtime change, perform proportionate
read-only health checks within the work-unit scope: relevant service state,
expected endpoint or process health, available storage, time synchronization
when timing matters, and repository cleanliness. Record the checks in
`CHANGE_AUDIT.md`. Do not broaden a health check into invasive inspection of
unrelated services, credentials, evidence, or private runtime state.
