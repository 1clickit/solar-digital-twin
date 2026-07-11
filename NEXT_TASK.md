# Next Task

## Objective

Extend repository health checks with shell and Python syntax validation.

## Context

The first local repository health check script is operational:

`scripts/repo_health_check.sh`

`status.sh` now runs this check during normal session startup.

The next small improvement is to add safe syntax checks that do not change files.

## Scope

Extend the repository health check to verify:

- tracked shell scripts parse with `bash -n`
- Python source files compile with `python -m compileall`
- checks report clear pass/fail results
- checks do not modify files

## Exclusions

- Do not create a separate framework repository.
- Do not generate a full project template yet.
- Do not modify EG4 collector or portal behavior.
- Do not run commands that require EG4 credentials.

## Success

`./scripts/repo_health_check.sh` and `./status.sh` both report passing health checks.

## Consider Later

Improve portal browser freshness without changing data collection:

- discourage browser caching so newly opened windows show the latest generated HTML
- optionally reload an open portal tab automatically
- preserve generated time, source time, and stale-data warnings
- keep browser reloads separate from the 15-minute EG4 collection timer

Improve tmux scrollback/copy behavior:

- consider raising VM-side tmux history limit beyond 50000 lines
- document the preferred Debian WSL -> SSH -> VM-side tmux setup
