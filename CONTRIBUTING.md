# Solar Digital Twin Development and Risk Policy

`TEAM.md` defines project roles. This document is authoritative for workflow,
risk classification, approvals, preservation, audit, commits, and pushes.

## Working method

- Use coherent, bounded, reviewable milestones and evidence over opinion.
- Inspect repository state before editing and preserve working behavior.
- Test before committing and keep `main` clean at completed checkpoints.
- Update directly related authoritative documentation with validated work.
- Keep logs and diffs concise; do not ask Chris to review raw code as the main
  quality gate.
- Put deferred ideas in `BACKLOG.md` or the applicable non-authoritative ideas
  document only when the milestone authorizes that edit.
- Stop scope drift and return to the authorized milestone.

## Milestone authorization

A milestone is one coherent, reviewable capability or outcome that may contain
multiple internal tasks. It is bounded by purpose and protected systems, not
artificially divided into repeated approvals. An authorized milestone states:

- objective and expected deliverables;
- accepted semantic requirements;
- applicable source and system scope;
- protected boundaries;
- validation requirements;
- publication mode and permitted commit plan;
- recovery expectations; and
- explicit stop conditions.

Once Chris approves a milestone proposed and bounded by ChatGPT, that one
authorization covers every activity explicitly included through completion.
Codex may proceed without repeated confirmation through relevant repository
and authenticated read-only inspection, design refinement, implementation,
tests and fixtures, internal refactoring, in-scope defect correction and
revalidation, documentation, repository health checks, bounded analysis,
sanitized reports, explicitly included operational work, and the authorized
publication cycle.

Codex may make routine reversible engineering decisions consistent with the
accepted architecture and milestone: module organization, internal API shape,
naming, test structure, bounded retry/timeout mechanics, portal layout, report
formatting, checkpoints, temporary working-file organization, and low-risk
refactoring. A milestone may use a reversible, versioned, clearly provisional
default when raw evidence is unchanged and the completion report identifies it
for later owner review.

Codex does not silently decide physical electrical operation, inverter or
battery configuration, public exposure, destructive evidence handling, major
expenditure, permanent architecture replacement, safety policy, or event
meaning whose alternatives materially change conclusions. Prefer configurable
placeholders or deferred bindings when unresolved semantics can be represented
honestly.

## Chris–ChatGPT conversation modes

Conversation modes govern whether Chris and ChatGPT are discussing possible
work or advancing an agreed milestone. They are distinct from the Git
publication modes below, which govern staging, commit, and push authority for
an already authorized Codex request.

### Discussion Mode

Discussion Mode is for questions, explanation, brainstorming, project
direction, alternatives, and general conversation. Discussion may describe
tentative future work, but it does not authorize Codex work, repository edits,
commands, implementation, publication, runtime action, or a change to
`NEXT_TASK.md`. A discussion conclusion is not silently promoted into project
work. Moving a topic into Work Mode requires explicit agreement between Chris
and ChatGPT about one coherent bounded milestone.

### Work Mode

Work Mode advances one authorized milestone, normally through Codex. A
milestone may be substantial and contain many related internal tasks. ChatGPT
identifies its complete objective, deliverables, boundaries, validation,
recovery, stop conditions, and publication plan in one self-contained Codex
request and declares exactly one Git publication mode: `commit-and-push`,
`commit-only`, or `no-commit-or-push`. Chris returns the completed milestone
result to ChatGPT for independent consolidated review. Corrections are bundled
into the smallest useful follow-up milestone rather than creating routine
micro-approvals.

When Chris must personally perform an operation, ChatGPT labels it an
**Owner/Admin Step**, identifies the exact host and shell, provides one
manageable executable step, and waits for its result when later action depends
on it. Work Mode itself grants no protected operational authority: the bounded
request and the risk rules in this document continue to control every action.

### Selecting and changing modes

- The literal labels `Discussion Mode` and `Work Mode` explicitly select the
  conversation mode, which persists until explicitly changed.
- At the beginning of a fresh session, ChatGPT identifies the mode.
- If no mode is stated and there is no accepted active-milestone handoff, the
  conversation starts in Discussion Mode; implementation authority is not
  inferred.
- A valid handoff that explicitly states Work Mode and the accepted next work
  milestone may resume in Work Mode.
- Moving from Discussion Mode to Work Mode requires ChatGPT to state the
  proposed milestone and Chris to agree.
- Either participant may return to Discussion Mode when a consequential
  decision, ambiguity, risk, or architectural question needs conversation.

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

Credential values must also remain out of fixtures, generated prompts, Codex
completion reports, console/debug output, exception traces, process listings,
portal output, public URLs, screenshots, copied evidence, and test failures.
Use existing protected credential files, runtime identities, or approved secret
mechanisms; never echo secrets or place them in environment dumps or process
arguments. Disable or sanitize verbose authentication logging. Necessary
unsanitized responses stay only in an appropriately protected temporary or
runtime location, and repository artifacts are narrowly sanitized. Perform a
credential and sensitive-content review before staging/publication and stop if
disclosure risk cannot be confidently excluded.

Read-only use never authorizes disclosure; repository copying; relocation to a
less protected place; ownership/permission weakening; password/token creation,
change, reset, rotation, or deletion; portal exposure; or sending credentials
to ChatGPT. Authentication failure never authorizes account, permission, or
device changes.

## Authority and approval classes

ChatGPT classifies actions by actual risk and explains material risk plainly.

### Standing milestone authority

After Chris authorizes a milestone, ChatGPT may direct Codex through its
complete cycle without repeated approval. The milestone controls substantive
and operational scope; its publication mode separately controls staging,
commit, and push authority.

### Git publication modes

Every Codex milestone request must declare exactly one of the following modes.
Codex must identify it before write work and enforce it exactly.

#### Publication mode: commit-and-push

After validation and every normal safeguard passes, Codex may stage only
validated in-scope files, create the permitted normal commit plan, push once
normally by fast-forward to the expected `origin/main`, fetch and verify
synchronization, and verify the published result. The milestone may authorize
one final commit or a bounded series of logical commits; one final commit is
the default when no series is stated.

For an authorized series, every commit remains within milestone scope, no
partial commit may contain secrets or unexpected artifacts, the series is
validated as a whole before one final push, and amend, reset, rebase,
force-push, and history rewriting remain prohibited.

This is normally appropriate for routine, bounded, reversible repository work:
documentation synchronization, narrow tested corrections, focused tests,
focused implementation milestones with settled requirements, and low-risk
maintenance. A discovered mistake is corrected with a later normal commit;
never amend, reset, force-push, or rewrite history merely to conceal it.

#### Publication mode: commit-only

After validation, Codex may stage only validated in-scope files, create one
normal local commit, and must stop before every push. Its report includes the
local commit hash and subject, files, validation, working-tree state, and an
explicit statement that no push occurred.

ChatGPT may select this mode when pre-publication review is materially
justified, including authoritative architecture/contracts, security or
credential policy, evidence or retention semantics, storage schemas or
migrations, substantial deletions/reorganization, unusually public or
sensitive material, unresolved technical uncertainty, or any request that
requires review before publication. A later push needs a separately authorized
milestone with its own publication mode.

#### Publication mode: no-commit-or-push

Codex must not stage, commit, or push. Use this for read-only review,
repository inspection, exploratory analysis, unapproved planning, or drafts
intended to remain uncommitted. Codex reports every resulting working-tree
change clearly.

#### Missing publication mode

Codex must not infer publication authority. If a milestone request declares no
mode, Codex may perform only clearly authorized read-only inspection; it
must not begin write work, stage, commit, or push, and must report that the
publication mode is missing.

A publication mode never expands the substantive milestone scope or grants
runtime, service, credential, evidence, database, network, deployment,
device-control, or destructive-Git authority. Normal pushes are fast-forward
only. Destructive and exceptional Git operations remain always gated. A
platform confirmation neither changes the selected mode nor expands scope.

### Standing authenticated read-only project authority

During an active project-relevant task directed by ChatGPT or explicitly
requested by Chris, Codex may use existing project credentials and runtime
identities for relevant authenticated read-only work without a new approval
each time. This includes authenticated `GET`, `HEAD`, or equivalent documented
read-only API queries; approved health/status endpoints; source and metric
inventories; telemetry, device, service, and protected runtime metadata;
strict read-only database queries; completed-evidence inspection; and narrowly
sanitized fixtures or reports.

This authority applies only while the active milestone or bounded
investigation needs the access. It does not authorize spontaneous inspection,
continued access after the task, unattended recurrence, or persistence.
Collectors, schedules, background monitoring, automatic reboot resume, and
long-duration capture require explicit milestone duration, source scope,
checkpointing, stop behavior, recovery, and storage limits.

Prefer an established least-privileged or technically read-only credential
when readily available and suitable. Its absence does not block relevant
read-only work: an existing credential with broader technical capability may
be used when the task is relevant, the invoked operation is demonstrably
read-only, no control/write endpoint is used, secrets remain protected,
operation is non-disruptive, and authentication failure causes no account or
permission change. Broader credential capability never expands behavioral
authority.

Exact access to a known approved credential file, secret mechanism, or runtime
identity is permitted for this read-only work. An execution-platform
confirmation may be accepted only when it grants that exact access. Stop if it
would grant unrestricted root-filesystem inspection, unrelated home or
credential stores, broad recursive access, credential export/relocation,
permission weakening, or unrelated protected-runtime access.

Read-only access must be operationally non-disruptive: use the minimum query
rate and response volume needed; avoid rapid polling, unnecessary full
responses, expensive unbounded queries, locks, and long transactions; stop
repeated authentication after a small number of failures; and avoid lockout,
rate limiting, device load, storage exhaustion, or service instability. A
technically non-writing request that may materially degrade availability is
not permitted.

Read-only means inspection without changing configuration, control state,
stored evidence, firmware, accounts, permissions, or operating behavior.
`POST`, `PUT`, `PATCH`, and `DELETE` are excluded unless independently proven
non-mutating and explicitly allowed by the milestone. Control endpoints,
configuration or database writes, service restart/reload, firmware/device
commands, evidence/retention/permission changes, deployment, and public
exposure are not standing read-only operations. If endpoint semantics cannot
be proven non-mutating, stop.

Authenticated-access completion reports and applicable audit entries record,
without secrets: source/service identity, general endpoint/query family,
read-only method, approximate request count, relevant start/end time, whether
protected temporary unsanitized material existed, its protected location,
sanitization method, and authentication/rate/availability/completeness
problems. Never record passwords, tokens, authorization headers, cookies,
credential-bearing URLs/commands, sensitive full responses, or secret-bearing
errors.

### Milestone operational authority

A milestone may explicitly include one-approval operational work such as
package installation; service/timer creation; runtime deployment; narrow
user/group/ACL or permission setup; a new read-only collection; controlled
evidence copying; database migration; portal startup; or runtime validation.
One milestone approval then covers the complete implementation, validation,
in-scope correction, restart, and rollback sequence. Ask again only if scope or
risk materially expands. This creates no standing operational authority
outside that milestone.

### Always-gated operations

Chris's explicit approval is required immediately before force-push; reset,
rebase, history rewriting, or destructive Git operations; permanent evidence
deletion or rewriting; credential/token disclosure, movement to a less
protected location, or permission weakening; broad recursive permission
changes; firewall changes affecting public reachability or other public/WAN
exposure; power/safety device control; inverter or battery configuration;
firmware flashing without an accepted recovery path; destructive database
operations; physical electrical changes; major purchases or architecture
replacement with major cost/recovery implications; or an action materially
riskier than the authorized milestone.

Proceed when work is routine, bounded, reversible, and authorized. Stop and ask
Chris when uncertainty could materially affect physical safety, evidence
integrity, credentials, availability, recovery, major cost, or project
direction.

## Manual operation and milestone Codex workflow

This section is canonical for the distinction between actions Chris performs
and work Codex performs locally.

### Manual operation by Chris

When Chris personally performs commands, give one manageable actionable step
at a time, immediately name the exact host and shell, and use a compact
executable command block. Pause for the observed result when the next action
depends on it. Avoid oversized logs, diffs, and heredocs. ChatGPT remains
responsible for routine software-engineering judgment; do not transfer that
burden to Chris.

ChatGPT is the primary author and reviewer of commands Chris personally runs.
Chris returns each observed result to ChatGPT and receives the next dependent
step there. Codex may analyze or propose operational commands to ChatGPT, but
does not maintain a parallel command-relay conversation with Chris unless
ChatGPT explicitly delegates that role for a milestone. Prefer compact
commands because line wrapping, duplicated paste content, and surrounding
prompt text can corrupt oversized terminal input. This presentation rule is
separate from authorization: it does not divide one approved milestone
into repeated approval gates or reduce repository-only Codex autonomy.

### Authorized milestone execution

Codex reads the complete milestone request and proceeds uninterrupted until all
deliverables are complete or a material stop condition occurs. Authorization
covers every explicitly included repository, read-only inspection,
implementation, validation, documentation, analysis, operational, and
publication activity. Self-correction and repeated validation inside the
milestone need no new approval.

Codex must not request repeated permission for an already-authorized activity.
Chris should not be placed in a routine “press Y” role after ChatGPT has already
classified the action, scope, and safeguards. This autonomy never expands the
approved purpose or files, transfers routine engineering decisions to Chris,
or bypasses execution-environment security controls.

### Repository and operational authority

Repository authorization alone does not grant deployment, persistent runtime,
configuration, control, or other operational authority. Standing
authenticated read-only authority applies during active relevant tasks.
Installation; service/timer/process changes; user/group/ACL/permission changes;
firmware/control actions; migrations; evidence copying; deployment; and other
mutating operational work must be explicitly included in the milestone.
Always-gated actions still require immediate owner approval.

Known pre-existing changes do not automatically block a milestone when the
request identifies them exactly, says whether each is adopted, preserved, or
excluded, requires actual-state verification, and prevents accidental editing
or staging of excluded work. Unexpected changes remain a stop condition.

### Publication safeguards

Before any authorized staging, commit, or push, Codex must confirm the
applicable safeguards for the selected publication mode:

- the work remains entirely within the approved purpose and file scope;
- the starting working tree and every resulting change are understood;
- all required validation passes;
- only intended files are staged;
- no credential, token, authorization header, protected path, or other
  sensitive material is present;
- no raw evidence, generated report or portal output, database, cache, backup,
  or other unexpected artifact is included;
- the expected remote remains `origin`, the target remains `origin/main`, and
  the configured remote URL is unchanged and expected;
- local and remote history have not unexpectedly diverged and the push is a
  normal fast-forward; and
- no protected operational action occurred.

All listed safeguards apply to `commit-and-push`; all staging/commit and scope
safeguards apply to `commit-only`; `no-commit-or-push` prohibits staging,
commit, and push. If any applicable safeguard fails, Codex stops before the
prohibited or unsafe action and reports the exact condition.

### Escalation boundary

Codex stops and returns the exact condition when:

- continuing materially exceeds or conflicts with the milestone;
- a protected always-gated action is required;
- public or accidental credential disclosure cannot be prevented;
- a supposedly read-only operation may mutate or materially disrupt its target;
- physical safety could be affected;
- raw evidence would be destroyed, overwritten, or normalized in place;
- validation cannot be completed or in-scope defects cannot be corrected;
- repository/environment state invalidates the milestone, including unexpected
  changes, divergence, checkpoint, files, or behavior;
- a major unresolved semantic decision cannot be represented safely as
  configurable or deferred;
- recovery is unavailable for a consequential operation;
- major cost or architecture direction would change;
- an applicable publication safeguard fails, or any amend, reset, rebase,
  merge, force-push, destructive Git action, or history rewrite is required; or
- continuing would otherwise become unsafe or materially ambiguous.

Codex does not stop merely because a relevant read-only query needs an existing
credential or approved credential file, a correctable routine test fails, an
internal engineering choice is needed, multiple related files must change, the
milestone is lengthy, an exact platform confirmation appears, or one internal
task finishes while other deliverables remain.

### Interface-enforced confirmations

The Codex execution environment may display a mandatory platform confirmation
even when the milestone already authorizes the exact action. Such a
prompt is an interface control, not a request for Chris to make a new technical
decision. Codex may use it only when the displayed action exactly matches the
authorized activity and may not broaden the action because confirmation is
available.

A confirmation may cover exact authorized credential/runtime access or other
milestone activity. Broader filesystem, unrelated credential/runtime access,
credential export/relocation, permission weakening, destructive Git activity,
or another unapproved boundary requires stopping. Project policy does not
bypass platform controls.

### Reviewability and durable records

Review occurs primarily at the completed milestone boundary and uses the
original milestone request, Codex's compact completion report, representative
implementation and critical interfaces, Git status/diff/history and remote
synchronization, tests and repository-health results, credential/source
boundaries, evidence preservation, disclosure checks, the Codex session or
activity record, and append-only audit entries. ChatGPT need not inspect every
routine internal edit before Codex finishes.

Owner acceptance remains required when a milestone establishes consequential
project semantics, activates production behavior, changes physical operation,
or crosses another owner-controlled gate.

Interface and session history may be transient. It is not durable project
evidence unless a documented retention mechanism preserves it. Git and the
repository audit are the durable project records; evidence-specific provenance
remains governed by its own immutable records.

### Required completion report

Codex reports the milestone outcome, declared publication mode and commit plan,
every changed/included file, tests and validation, working-tree state, and
protected-boundary confirmation. It also includes the sanitized authenticated
access record above when applicable. For `commit-only`, report every local
commit hash/subject and confirm no push. For `commit-and-push`, report every
commit hash/subject, local `HEAD`, `origin/main`, ahead/behind, normal
fast-forward publication, and independent published-repository verification
when practical. For `no-commit-or-push`, report remaining changes and confirm
no staging, commit, or push.

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
change. Temporary milestone-working files belong under `/tmp` and may expire
through normal operating-system cleanup; do not label unique artifacts as
temporary to delete them.

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

Every persistent-change milestone appends an entry before completion. Never
silently edit or remove an existing entry; correct it with a later entry that
references the original. Include, where applicable: UTC time, actor, purpose,
affected files or components, change and reason, explicitly untouched scope,
validation/tests, recovery or rollback, archive/backup location, related commit
and push state, and unresolved risks or limitations.

Routine read-only inspection needs no audit entry unless it produces a
significant engineering finding or persistent report. Creating the audit entry
for a milestone does not recursively require another entry. Audit entries must
never contain passwords, tokens, API keys, authorization headers, credential
contents, secret arguments, or sensitive runtime output.

## Git and milestone synchronization

The declared publication mode determines whether staging, a local commit, and
publication are authorized. Codex stages only validated in-scope files. The
milestone permits either one final commit or an explicit bounded logical
series, which is validated as a whole before one normal fast-forward push.
Fetch-based synchronization and published-result verification follow. Pushes
are never forceful under routine authority. Destructive or exceptional Git
operations remain always gated.

## Recovery

Back up or archive before significant changes, preserve known-good versions,
and define rollback in the milestone. Direct device access and recovery must
not depend on a collector. Prefer reversible steps and verify replacements
before retiring prior versions.

## VM and operational health

Follow the read-only schedule, observations, thresholds, and append-only entry
format in `docs/operations/VM_HEALTH_LOG.md`. A normal health review is recorded
there, not duplicated in `CHANGE_AUDIT.md`. Any persistent corrective action
resulting from it receives a change-audit entry. Do not broaden a health review
into invasive inspection or automatic remediation.
