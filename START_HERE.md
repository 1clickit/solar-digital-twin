# Start Here

The repository is the Solar Digital Twin project's authoritative memory. Use
the current local working copy when available; GitHub is the shared record of
pushed milestones. Do not rely on old chat history or a stale external copy.

## Startup order

Read:

1. `TEAM.md` — roles and working relationship
2. `CONTRIBUTING.md` — risk, approval, preservation, audit, and Git policy
3. `PROJECT_STATE.md` — verified current state and restrictions
4. `NEXT_TASK.md` — next proposed milestone
5. `AI_PROMPT.md` — ChatGPT project-lead behavior
6. `AGENTS.md` — Codex local-agent behavior
7. `PROJECT_INDEX.md` — navigation when more context is needed
8. `BACKLOG.md` and `docs/chat_ideas/README.md` only when deferred ideas matter

Persistent changes follow the archive-first and append-only audit policy in
`CONTRIBUTING.md`. Periodic and event-driven read-only VM health reviews are
recorded in `docs/operations/VM_HEALTH_LOG.md`.

Every Codex milestone declares exactly one canonical publication mode defined
in `CONTRIBUTING.md`; the mode controls staging, commit, and push authority
without expanding milestone scope. Milestone authorization and standing
authenticated read-only project authority are also defined there.

At fresh-session startup, ChatGPT identifies the persistent conversation mode
defined in `CONTRIBUTING.md`. If neither a mode nor a valid accepted Work Mode
handoff is present, begin in Discussion Mode. Conversation mode and Git
publication mode are separate controls.

Inspect the current branch, HEAD, and working tree before changing anything.
Resolve authoritative-document contradictions before new implementation.

## Continuation behavior

ChatGPT leads proactively from the verified state: maintain the complete
project picture, define the next coherent bounded milestone, direct Codex,
review the consolidated result, and keep work aligned with the diagnostic
mission. Chris is not expected to invent routine software steps. Chris remains
final authority for the physical system, consequential project direction, and
major cost.

Codex completes an authorized milestone as described in `AGENTS.md`; manual
one-command relay is used only when Chris must operate a host or system
directly.

## Session and milestone lifecycle

1. Read the authoritative state and restrictions.
2. Verify repository and relevant input state.
3. Complete one coherent, risk-calibrated, tested milestone.
4. Update authoritative documentation and `CHANGE_AUDIT.md` for persistent
   changes.
5. Complete any authorized commit, normal fast-forward publication, and
   synchronization verification under the canonical safeguards in
   `CONTRIBUTING.md`.
6. Leave enough documentation for a fresh session to continue safely.

## Engineering philosophy

- Evidence over opinion; hypotheses remain distinct from facts.
- Preserve raw evidence, provenance, recovery options, and decision history.
- Prefer simple, reversible, low-cost steps until complexity is justified.
- Verify before concluding and state uncertainty plainly.
- Keep the portal, collectors, analyzers, and automation subordinate to the
  physical solar-system diagnostic mission.
- Capture unrelated ideas without expanding the active milestone.

## Communication

Use concise summaries rather than full diffs or logs. When Chris must execute a
command, label the host and shell, show executable commands only, state whether
results should be pasted, and wait for observed results before concluding that
the action succeeded.

`FOCUS` means reread current state, return to the active objective, verify what
has already happened, and avoid scope drift. `RECALIBRATE` invokes the fuller
procedure in `AI_PROMPT.md`.
