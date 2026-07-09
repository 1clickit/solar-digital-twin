# START HERE

Welcome to the Solar Digital Twin project.

## Purpose

This repository is the authoritative memory of the project.

Do not rely on previous chat history to determine the
current state of the project.

Every new engineering session begins by reviewing this
repository.

## Read in this order

1. TEAM.md
2. CONTRIBUTING.md
3. PROJECT_STATE.md
4. NEXT_TASK.md
5. BACKLOG.md (if needed)

6. SESSION_END.md

These documents contain everything required to resume
development.

## Engineering Philosophy

The repository remembers the project.

The chat is today's workspace.

Improve the repository instead of relying on
conversation memory.

If something would help future sessions,
document it.

## Development Workflow

Always work using small engineering iterations.

- One terminal command at a time.
- One tested change at a time.
- One commit at a time.
- Test before committing.
- Push completed work to GitHub.

Never leave important project knowledge
only in a conversation.

## Local VM

The Ubuntu VM is the working environment.

Use it for:

- running code
- testing
- generated artifacts
- local configuration
- uncommitted work

GitHub remains the authoritative record
of committed work.

## Session Goal

At the end of every session,
another engineer should be able to continue
using only this repository.

## What "FOCUS" Means

**FOCUS** is not an instruction to stop thinking critically or to avoid making engineering suggestions.

Instead, it is a quality-control principle for this project. It originated as a signal from the user during long development sessions, but every future session should treat it as a reminder to verify context before proceeding.

When the user says **FOCUS**, it means the assistant should:

- Re-center on the current task and the documented project state.
- Avoid introducing unrelated ideas or expanding the scope of the current commit.
- Verify what has already been completed before proposing additional work.
- Reduce the chance of repeated work, forgotten decisions, or incorrect assumptions that can occur late in long conversations.
- Continue offering engineering improvements when they materially improve the project, but clearly separate them from the task currently being executed.
- If the assistant recognizes it is losing project context, repeating work, or making unnecessary assumptions, it should pause, review the repository documentation, and re-establish the current project state before continuing rather than waiting for the user to say "FOCUS."

The preferred workflow is to minimize the need for **FOCUS** by using the repository as the source of truth:

1. Read `START_HERE.md`.
2. Have the user run `./status.sh`.
3. Review the output and referenced project documentation.
4. Determine the next smallest tested task.
5. Complete one small, tested commit.
6. Repeat.

The goal is disciplined execution without sacrificing engineering judgment. The assistant should continue looking for opportunities to improve the architecture, workflow, reliability, and maintainability of the project, while keeping those recommendations separate from the immediate task unless they are required to complete it correctly.

## Repository Editing Guidelines

To keep development reproducible and reduce mistakes, follow these communication rules during every session:

- Provide complete, paste-ready shell commands for anything the user should run.
- Clearly distinguish shell commands from file content intended for review.
- When practical, automate repository edits using heredocs or scripts instead of requiring manual editing.
- If text is provided for review rather than execution, explicitly state that it is **for review only**.
- Unless the user requests otherwise, provide only one actionable step at a time.

These guidelines improve reproducibility, reduce confusion, and allow future sessions to continue the project consistently.
