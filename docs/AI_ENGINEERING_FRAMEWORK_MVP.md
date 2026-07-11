# AI Engineering Framework MVP

## Purpose

This document defines the boundary of a reusable AI engineering framework MVP discovered from the Solar Digital Twin workflow.

The goal is to identify what can be reused by unrelated coding projects without extracting, forking, or building the framework yet.

## MVP Boundary

The MVP is a documentation and workflow framework, not a software product yet.

It should define:

- startup rules
- communication rules
- project-state tracking
- task tracking
- local verification expectations
- safety and correctness checks
- session-end audit expectations
- future template or bootstrap structure

It should not yet define:

- a separate repository
- a package or installer
- a generated project scaffold
- a full automation engine
- a replacement for Solar Digital Twin documentation

Solar Digital Twin remains the active project.

## Reusable Components

Reusable across coding projects:

- authoritative project documentation
- startup document review
- explicit current task tracking
- one-action-at-a-time workflow
- clear command/output handoff
- local verification before claims about local state
- post-push public repository audit
- session-end checklist
- backlog and Consider Later separation
- generated artifact policy
- communication correction loop
- stable terminal/session guidance for long work

## Solar Digital Twin-Specific Components

Specific to this project:

- EG4 collector details
- EG4 portal details
- inverter serial numbers
- local VM name and path
- LAN portal address and port
- systemd EG4 refresh service and timer
- SQLite database and report filenames
- preferred terminal path: Debian WSL -> SSH -> VM-side tmux
- avoiding IPv6 for local portal access

## Mandatory Rules

Mandatory rules prevent unsafe, misleading, or destructive behavior.

Initial mandatory rules:

- warn before commands that request credentials or interactive input
- never ask the user to paste credentials
- inspect actual errors before proposing fixes
- do not assume exact file contents when uncertain
- do not assume exact local paths when uncertain
- do not assume installed commands when uncertain
- use local verification for local-only facts
- distinguish successful report generation from fresh underlying source data
- do not promote Consider Later ideas without discussion
- use `--no-pager` for output that must be pasted
- keep generated artifacts out of Git unless explicitly intended

## Judgment-Based Guidance

Guidance helps the assistant make better choices but should not be treated as absolute law.

Initial guidance:

- prefer reviewable, reversible terminal changes sized to the risk of the edit
- allow larger terminal edits when they are easy to inspect and safe to reverse
- use smaller patches for risky, uncertain, or hard-to-inspect changes
- prefer stable reconnectable sessions for long engineering work
- reduce repeated verification when public GitHub already proves a committed fact
- choose inspection depth based on risk
- avoid unnecessary chatter after asking the user to paste command output
- keep browser caching and automatic reload as Consider Later unless the user asks to discuss them

## Automated Local Checks

Possible reusable checks:

- required documentation files exist
- required headings exist
- current milestone and next task are aligned
- generated artifact directories remain ignored
- no secrets or credential files are staged
- Markdown links to local docs resolve
- shell scripts pass syntax checks
- Python files compile
- tests or smoke checks run where available

## Post-Push Public GitHub Audit

After pushing, verify public repository state rather than relying only on local success.

Reusable audit checks:

- intended commit is visible on public GitHub
- changed files match the expected scope
- required docs are visible
- generated artifacts were not pushed
- project state and next task agree
- the next task remains actionable for a fresh session

## Future Template or Bootstrap

A future framework template could include:

- `START_HERE.md`
- `AI_PROMPT.md`
- `PROJECT_STATE.md`
- `NEXT_TASK.md`
- `BACKLOG.md`
- `SESSION_END.md`
- `docs/`
- `scripts/health_check.sh`
- optional project-specific overlay docs

The bootstrap process should ask for project-specific facts instead of assuming them.

## Open Questions

- Which rules belong in every project by default?
- Which checks should be implemented as scripts first?
- Should the framework live inside each project or become a separate template repository later?
- How much project-specific terminal guidance should a reusable template allow?
