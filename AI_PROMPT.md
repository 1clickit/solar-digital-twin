# AI Operating Instructions

## Authority

Repository documentation is authoritative memory.

Read and follow:

1. `START_HERE.md`
2. All documents referenced by `START_HERE.md`
3. `AI_PROMPT.md`

## Startup

Assume there have been no local changes since the last committed and pushed state unless explicitly stated.

Begin by asking:

"Have there been any local changes since the last committed and pushed state?"

If yes, uncertain, or partial, request `./status.sh`.

If no, proceed from the public GitHub repository documentation.

## Communication Rules

- Use one actionable step at a time.
- Use bold labels before copyable blocks:
  - `Please run the following command:`
  - `Proposed file contents:`
  - `Discussion only:`
  - `For review only:`
- Do not place examples, filenames, future ideas, or quoted text into executable-looking blocks.
- When the user corrects communication behavior:
  1. acknowledge,
  2. briefly restate understanding,
  3. stop and wait for feedback.

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
- small file creation tasks.

## RECALIBRATE

If the user says:

`RECALIBRATE`

then:

1. Stop.
2. Re-read repository workflow documents.
3. Identify the deviation.
4. Return to the last known good point.
5. Continue without introducing new ideas.

## Workflow Improvements

Repository workflow improvements are part of the project and may be updated when deficiencies are discovered.