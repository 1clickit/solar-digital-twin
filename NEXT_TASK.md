# Next Task

## Objective

Prepare the repository and `solardt` VM for safe OpenAI Codex CLI use before
resuming collector implementation.

## Context

Repomix evaluation has stopped as the active workflow task. Repomix may be
considered later as an occasional architecture-audit snapshot tool, but it is
not current project workflow, authoritative memory, or a recovery backup.

The current engineering implementation goal remains persistent multi-rate
telemetry collection. Codex preparation is a workflow improvement intended to
reduce manual copy/paste load and preserve project momentum.

## Scope

- Add `AGENTS.md` as the Codex CLI entry point.
- Distinguish manual ChatGPT relay rules from Codex local-agent rules.
- Allow Codex to perform bounded, reviewable local work units rather than one
  pasted terminal command at a time.
- Preserve repository documentation as authoritative project memory.
- Keep commits and pushes under explicit user approval.
- Keep actual secret values out of chat, logs, commits, and generated output.
- Install and evaluate Codex CLI only after this documentation is committed and
  pushed.

## Initial Codex Evaluation Boundary

The first Codex evaluation should be read-only or documentation-only.

Codex should read the repository guidance, inspect status, run safe local
checks, and summarize what it would do next before making code changes.

## Resume Afterward

After Codex is safely evaluated, resume hardening the standalone collectors for
configurable observation, selective retention, evidence rotation, freshness
tracking, and controlled recovery before portal, SQLite, or systemd integration.

## Success

The repository clearly tells Codex how to operate safely, Repomix is no longer
an active task, and the project is ready for a conservative Codex CLI install
and evaluation on `solardt`.
