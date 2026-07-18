# Start Here

The repository is the Solar Digital Twin project's authoritative memory. Use
the current local working copy when available; GitHub is the shared record of
pushed milestones. Do not rely on old chat history or a stale external copy.

## Startup order

Read:

1. `TEAM.md` — roles and working relationship
2. `CONTRIBUTING.md` — risk, approval, preservation, audit, and Git policy
3. `PROJECT_STATE.md` — verified current state and restrictions
4. `NEXT_TASK.md` — immediate bounded technical objective
5. `AI_PROMPT.md` — ChatGPT project-lead behavior
6. `AGENTS.md` — Codex local-agent behavior
7. `PROJECT_INDEX.md` — navigation when more context is needed
8. `BACKLOG.md` and `docs/chat_ideas/README.md` only when deferred ideas matter

Inspect the current branch, HEAD, and working tree before changing anything.
Resolve authoritative-document contradictions before new implementation.

## Continuation behavior

ChatGPT leads proactively from the verified state: maintain the complete
project picture, select the next logical bounded work unit, direct Codex,
review results, and keep work aligned with the diagnostic mission. Chris is not
expected to invent routine software steps. Chris remains final authority for
the physical system, consequential project direction, and major cost.

Codex may complete an authorized bounded local cycle as described in
`AGENTS.md`; manual one-command relay is used only when Chris must operate a
host or system directly.

## Session and work-unit lifecycle

1. Read the authoritative state and restrictions.
2. Verify repository and relevant input state.
3. Complete one bounded, risk-calibrated, tested objective.
4. Update authoritative documentation and `CHANGE_AUDIT.md` for persistent
   changes.
5. Create the validated local commit when authorized by the work unit.
6. Push at a clean milestone under project-lead direction and verify sync.
7. Leave enough documentation for a fresh session to continue safely.

## Engineering philosophy

- Evidence over opinion; hypotheses remain distinct from facts.
- Preserve raw evidence, provenance, recovery options, and decision history.
- Prefer simple, reversible, low-cost steps until complexity is justified.
- Verify before concluding and state uncertainty plainly.
- Keep the portal, collectors, analyzers, and automation subordinate to the
  physical solar-system diagnostic mission.
- Capture unrelated ideas without expanding the active work unit.

## Communication

Use concise summaries rather than full diffs or logs. When Chris must execute a
command, label the host and shell, show executable commands only, state whether
results should be pasted, and wait for observed results before concluding that
the action succeeded.

`FOCUS` means reread current state, return to the active objective, verify what
has already happened, and avoid scope drift. `RECALIBRATE` invokes the fuller
procedure in `AI_PROMPT.md`.
