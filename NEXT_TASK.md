# Next Task

## Objective

Design a reusable AI engineering framework MVP from the Solar Digital Twin workflow.

## Context

The EG4 portal, automated refresh timer, timezone handling, stale-data protection, and repository health checks are operational.

The repository currently mixes reusable engineering workflow rules with Solar Digital Twin-specific instructions.

## Scope

Design the framework boundary and structure only.

Include:

- reusable workflow components versus Solar Digital Twin-specific components
- mandatory safety and correctness rules versus judgment-based guidance
- automated local checks that can catch common workflow mistakes
- post-push public GitHub audit checks
- future template or bootstrap process ideas
- stable terminal/session workflow guidance for long AI-assisted engineering work
- Solar Digital Twin-specific terminal preference: Debian WSL -> SSH -> VM-side tmux
- paste guidance: larger edits may be allowed only when reviewable, reversible, and appropriate to risk
- guidance that preserves Solar Digital Twin as an active project

Do not extract, fork, or build the full framework yet.

## Success

A reviewed framework MVP design identifies what can be reused by unrelated coding projects without carrying Solar Digital Twin-specific assumptions.

## Consider Later

Improve portal browser freshness without changing data collection:

- discourage browser caching so newly opened windows show the latest generated HTML
- optionally reload an open portal tab automatically
- preserve generated time, source time, and stale-data warnings
- keep browser reloads separate from the 15-minute EG4 collection timer
