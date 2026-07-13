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

## Session Lifecycle

Every session follows the same lifecycle:

1. Beginning of session: Follow `START_HERE.md`.
2. Review repository status and documentation.
3. Complete one small, tested engineering step.
4. Update documentation as needed.
5. End of session: Follow `SESSION_END.md`.

When conversation length begins reducing response quality:

1. Finish the current small task.
2. Follow `SESSION_END.md`.
3. Recommend beginning a new session.

## Engineering Philosophy

The repository remembers the project.

The chat is today's workspace.

Improve the repository instead of relying on
conversation memory.

If something would help future sessions,
document it.

## Communication Workflow

- Avoid using code/copyable blocks for examples, quoted text, filenames, future ideas, or prompts unless explicitly requested.
- Avoid discussing future actions before reviewing requested command output.
- When requesting command execution, stop after the request and wait for results before discussing subsequent steps.
- Do not assume commands succeeded until their output has been reviewed.
- Avoid discussing expected future repository state until command results have been reviewed.

## Development Workflow

Always work using small engineering iterations.

- One terminal command at a time.
- One tested change at a time.
- One commit at a time.
- Test before committing.
- Push completed work to GitHub.
- A local-only commit is not complete; GitHub must contain the committed work before the task is declared complete.

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
- Introduce executable terminal commands with exactly: **Please run the following command:**
- Only use shell command blocks when the user is expected to execute them.
- Do not use shell command blocks for examples, filenames, future ideas, or possible utilities.
- When discussing possible future files, scripts, directories, or utilities, describe them in plain text.
- Example: **Possible future utilities:** `check_repo.sh`, `tools/check_repository.py`
- Clearly distinguish shell commands from file content intended for review.
- When practical, automate repository edits using heredocs or scripts instead of requiring manual editing.
- If text is provided for review rather than execution, explicitly state that it is **for review only**.
- Unless the user requests otherwise, provide only one actionable step at a time.
- End responses with a clear status or decision point when practical.
- Use phrases such as: **Ready to execute**, **Waiting for results**, **Discussion only**, **For review only**, or **A natural checkpoint has been reached**.
- When appropriate, ask whether the user wants to proceed with the suggested changes.
- If a natural checkpoint has been reached, ask whether the user would like to stop and follow `SESSION_END.md`.

These guidelines improve reproducibility, reduce confusion, and allow future sessions to continue the project consistently.

## Repository Location Guidance

GitHub repository: `1clickit/solar-digital-twin`

The assistant should not assume the local checkout location.

The user should run `./status.sh` from the repository root.

If the user is not already in the repository root, the assistant should ask the user to navigate to the local checkout of `1clickit/solar-digital-twin` first, then run `./status.sh`.

Do not invent local paths such as `~/solar-digital-twin` or `/home/chris/solar-digital-twin` unless the user has provided or confirmed that path in the current session.

## Development Environment

The user has Visual Studio Code with Remote SSH configured and may edit repository files directly.

For larger changes, prefer:

- direct file edits,
- small patches,
- line replacements,

instead of large heredocs.

Continue providing copyable shell commands for:

- testing,
- Git operations,
- repository inspection,
- and small file creation tasks.

## Response Checklist

Before sending a response, verify:

- Am I only discussing observed results?
- Am I assuming command success before seeing output?
- Am I placing non-executable text into code/copyable blocks?
- Could any example be mistaken for something the user should type?
- Am I proposing more than one action?
- Am I creating a new rule when an existing rule already covers the issue?

If any answer is yes, revise the response before sending.

## Startup Requirement

Before proposing work, review:

1. Communication Workflow
2. Response Checklist
3. Startup Decision Process

Treat these as mandatory operating instructions.



## Local Change Check Optimization

At session start, the assistant may ask whether there have been any local changes since the last committed and pushed state.

If the user confirms there have been no local changes, the assistant may proceed using the public GitHub repository documentation as the current project state.

The assistant should still request `./status.sh` when:

- the user reports local changes,
- the user is unsure whether local changes exist,
- generated local files need to be inspected,
- repository state appears inconsistent,
- or local verification is needed before making changes.

## Startup Decision Process

After reviewing the output of `./status.sh`:

1. If the working tree is not clean, inspect the uncommitted changes before proposing new work.
2. Treat `PROJECT_STATE.md` as the authoritative description of the current engineering state.
3. If project documents disagree about the next task, resolve the documentation first so there is a single source of truth.
4. Review the latest repository state before proposing changes.
5. Propose one small, testable engineering step at a time.
6. Prefer updating project documentation when improvements to the workflow are identified.


## EG4 Refresh Report Command

To refresh EG4 data and regenerate the engineering report, run:

`./eg4_refresh_report.sh`

This uses the existing EG4 collector and report generator.

## Generated Artifacts

Generated output is not considered source code.

Examples include:

- reports/
- evidence/
- cache/
- temporary analysis output

Unless the project documentation explicitly states otherwise, generated artifacts should not be committed to Git.

When working on generators:

1. Modify the source code.
2. Generate the artifacts locally.
3. Verify the generated output.
4. Commit the source code unless the generated artifact is intentionally version-controlled.

## Terminal Paste Guidance

When providing shell commands for this project:

- Prefer small, pasteable command blocks.
- Keep heredocs short when practical, usually about 30-40 lines or less.
- Prefer appending or patching existing files over replacing large files in one paste.
- If a heredoc appears to fail, first suspect an incomplete paste or browser issue before suspecting Bash, the terminal, or the VM.
- Do not recommend rebooting the VM unless the shell or system itself is clearly malfunctioning.

## Low-Output Chat Workflow

To reduce chat bloat and avoid tmux/browser paste issues:

- Avoid full diffs in chat after files exceed about 40 lines.
- Prefer compact checks such as `git status --short`, `wc -l`, `grep`, `tail`, and targeted file snippets.
- Redirect large logs to `/tmp` and paste only the relevant summary or last 20 to 40 lines.
- For larger documentation edits, write in small chunks or use file patches instead of one large heredoc.
- Commit and push completed work, then verify important file contents from the public GitHub repository when practical.
- Do not request large pasted output when a compact local check or public GitHub verification is sufficient.
