# AGENTS.md

This file is the OpenAI Codex CLI entry point for the Solar Digital Twin
repository.

## Startup

Before proposing or making changes, read:

1. `START_HERE.md`
2. `TEAM.md`
3. `CONTRIBUTING.md`
4. `PROJECT_STATE.md`
5. `NEXT_TASK.md`
6. `AI_PROMPT.md`

Treat repository documentation as authoritative project memory.

## Codex Operating Mode

The manual ChatGPT relay rules and Codex local-agent rules are different.

Manual ChatGPT relay rules apply when Chris is running commands and pasting
results back into a chat.

Codex CLI runs locally in the repository, so Codex may work in one bounded,
reviewable local work unit at a time instead of one pasted terminal command at
a time.

If Codex-specific guidance in this file conflicts with manual relay wording in
other project documents, follow this file for Codex CLI operation while
preserving the safety intent of the other documents.

A bounded work unit may include local inspection, related file edits, targeted
tests, repository health checks, and a concise summary.

## Communication

Chris is the project owner and system operator, not a software developer. Use
clear, plain language, and do not assume he can independently review source
code, full diffs, stack traces, or architecture decisions.

- Clearly distinguish informational output from decisions or actions that need
  Chris's approval.
- Prefer focused tests and code review over asking Chris to judge raw code.
- An external ChatGPT project-management session may provide bounded work
  instructions and review final summaries, but Codex cannot access that
  separate conversation.
- Repository documentation and the current Codex task remain authoritative.
- Preserve all existing approval requirements and safety guardrails.
- Codex may freely identify and propose ideas, risks, architecture improvements,
  and future work, but must label proposals separately from authorized work.
- Codex must not implement a proposal, expand the active task, or edit
  `BACKLOG.md` without explicit approval.

## Guardrails

- Prefer direct local inspection over asking the user to paste file contents.
- Inspect `git status --short` before changing files.
- Keep changes small, related, and reviewable.
- Do not read, display, paste, commit, or request secret values.
- It is acceptable to create or edit secret-handling templates, ignored files,
  documentation, and checks that verify required secrets exist without printing
  their values.
- Do not run `sudo`, destructive commands, package installs, or broad network
  actions without explicit approval.
- Do not commit without explicit user approval.
- Do not push without explicit user approval.
- Do not upload generated evidence, reports, databases, logs, credentials, or
  temporary repository snapshots unless project documentation explicitly says
  to do so.

## Credential-Blocked Work

When authorized work requires a credential that is not available through an
approved external mechanism, report the requirement without requesting its
value and stop the affected live action. Never read, display, return, or ask
Chris to paste the secret. No new credential installer, credential storage
layout, or authenticated consumer may be implemented until the project-wide
security decisions in `docs/SECURITY_MODEL.md` are approved. Existing approval,
network, service, and change-control requirements remain in force.

## Verification

After changing files, run the relevant checks. Usually this means:

- `./scripts/repo_health_check.sh`
- targeted tests for the files changed
- `git status --short`

Summarize changed files, checks run, and results before asking for approval to
commit or push.
