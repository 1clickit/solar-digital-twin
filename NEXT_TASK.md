# Next Task

## Objective

Implement the first small local automation checks from the AI engineering framework MVP design.

## Context

The reusable AI engineering framework MVP boundary design is documented in:

`docs/AI_ENGINEERING_FRAMEWORK_MVP.md`

The design identifies candidate first automation checks that should be small, local, and easy to trust.

## Scope

Create or extend a lightweight local check script for Solar Digital Twin repository health.

Initial checks should focus on:

- required project memory files exist
- `PROJECT_STATE.md` has a current milestone and next task
- `NEXT_TASK.md` has objective, scope, and success sections
- docs referenced from `PROJECT_INDEX.md` exist
- generated directories such as `reports/` and `evidence/` remain ignored by Git
- obvious credential filenames are not staged

## Exclusions

- Do not create a separate framework repository.
- Do not generate a full project template yet.
- Do not modify EG4 collector or portal behavior.

## Success

A local check command reports clear pass/fail results without changing files.

## Consider Later

Improve portal browser freshness without changing data collection:

- discourage browser caching so newly opened windows show the latest generated HTML
- optionally reload an open portal tab automatically
- preserve generated time, source time, and stale-data warnings
- keep browser reloads separate from the 15-minute EG4 collection timer
