# Next Task

## Objective

Enhance `status.sh` into a lightweight repository health check.

## Context

The EG4 portal service and automated 15-minute refresh timer are operational.

The current `status.sh` already reports:

- current branch
- Git status
- latest commit
- GitHub synchronization
- `PROJECT_STATE.md`
- `NEXT_TASK.md`

## Scope

Add concise checks for:

- required project files
- duplicate Markdown headings
- documentation drift between `PROJECT_STATE.md` and `NEXT_TASK.md`

Preserve the existing startup status output.

## Rules

Keep the script dependency-free.
Do not modify EG4 collector or portal behavior.
Report problems clearly without making automatic changes.

## Success

`./status.sh` continues to show normal session status and also reports repository health-check results.
