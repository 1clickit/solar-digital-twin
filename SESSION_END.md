# Session End Checklist

Before ending a work session, confirm:

## Engineering

- The bounded objective is complete or its blocker is documented.
- Relevant tests and repository checks passed, or failures are recorded.
- No unsupported conclusion or hidden scope expansion remains.

## Documentation and audit

- `PROJECT_STATE.md` and `NEXT_TASK.md` reflect validated current reality when
  the work changed it.
- Persistent changes have an appended `CHANGE_AUDIT.md` entry.
- Deferred ideas are recorded only in the appropriate authorized location.

## Repository

- Intended files only were staged and committed.
- `git status --short` was reviewed.
- Clean milestone commits were pushed under project-lead direction and
  local/remote synchronization was verified.
- A local commit that is intentionally awaiting a milestone push is clearly
  documented; it is not mislabeled as lost or incomplete work.

## Knowledge transfer

A new session should be able to continue from the repository without relying
on private conversation history. If it cannot, improve authoritative project
memory before ending.
