# Credential Installation

## Purpose

The credential installer creates approved integration credential files without
placing secret values in the repository, command history, Codex output, or
ChatGPT. Chris runs it manually from the normal `solardt` VM terminal.

Only the `solarassistant` service profile is currently approved. It writes the
`SOLARASSISTANT_PASSWORD` setting atomically to
`/etc/solar-digital-twin/solarassistant.env` as `root:root` with mode `0600`.
It creates `/etc/solar-digital-twin` securely when needed and does not read or
alter `/etc/solar-digital-twin/eg4.env`.

## Manual Installation

From the repository root, Chris runs:

`sudo .venv/bin/python -m solar_digital_twin.credentials solarassistant`

The installer accepts only a registered service identifier. It never accepts a
secret, destination, setting name, owner, or permissions as command-line
arguments. It prompts twice using hidden terminal input and refuses empty,
mismatched, or control-character input. Replacing an existing credential file
requires typing `REPLACE` before secret entry.

Successful output contains only the service identifier, destination, owner,
and permissions. The credential file must never be committed, copied into this
repository, included in reports, or exposed in Codex or ChatGPT output.

This work unit installs secure credential storage only. The current
SolarAssistant collector does not load this file, and no approved service or
launcher consumes it yet. Installing the file therefore does not currently
unblock a Codex-run live request. A separately reviewed and explicitly approved
consumer is required before unattended use.

Do not source the credential file with a shell. Its environment-file encoding
is intended for a future defined consumer, and shell interpretation could alter
some valid secret characters.

Future integrations require a separately reviewed and explicitly approved
profile. Profiles may later use different credential types or storage formats;
do not assume Home Assistant, ESPHome, or another integration uses a password
or environment file.

## Credential-Blocked Workflow

1. Codex reports that a credential is required without requesting its value.
2. Codex stops the affected live action.
3. Chris runs the approved installer or approved one-time hidden-input helper
   from the normal VM terminal.
4. Chris reports only success or a non-secret error.
5. Codex resumes only when an approved external consumer exists and can use the
   credential without reading, displaying, or returning the secret. Until then,
   the affected live action remains stopped.

Installation does not itself authorize a live request or service change. All
normal network, service, change-control, commit, and push approvals remain in
force.
