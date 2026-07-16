# SolarAssistant Dedicated Runtime

## Implementation status

Commit `39548b1` completed the repository-side collector interface, installers,
tests, and documentation. The committed runtime installer was subsequently run
manually from the normal `solardt` terminal with private `sudo` authentication.
The dedicated runtime and fixed paths below were installed successfully, and
the committed verification reported: `VERIFY: SolarAssistant runtime metadata
and access boundaries passed`.

The committed credential installer was then run manually. The trusted `solardt`
host administrator entered the password privately through the controlling
terminal, and the credential was installed with the approved metadata. Its
value and derivatives were not placed in Git, repository documentation, chat,
command arguments, or shell history. This follows the approved practical Home
Assistant-style trusted-host security model.

A one-time authenticated collector verification also completed successfully as
`solardt-sa` using the protected password file, dedicated runtime Python
environment, and dedicated `/var/lib` evidence output. No systemd service was
created or enabled, and no persistent collector was started.

## Purpose and boundary

SolarAssistant uses a dedicated unprivileged Linux identity while the effective
authority of its `admin` credential remains unknown. This is a practical Home
Assistant-style boundary: the trusted `solardt` administrator may securely
install or replace the password, while the collector can read it but cannot
change it or access unrelated credentials.

The password must never enter Git, the project tree, chat, logs, reports,
command arguments, shell history, or ordinary project backups. This design does
not use a vault, encryption agent, or custom root secret wrapper.

## Fixed identity and paths

- Service user and primary group: `solardt-sa`
- Account type: unprivileged system account with `/usr/sbin/nologin` and no home
- Credential directory: `/etc/solar-digital-twin/solarassistant`, `root:solardt-sa`, mode `0750`
- Password file: `/etc/solar-digital-twin/solarassistant/password`, `root:solardt-sa`, mode `0640`
- Runtime root: `/opt/solar-digital-twin`, administrator owned and not writable by `solardt-sa`
- State root: `/var/lib/solar-digital-twin/solarassistant`, `solardt-sa:solardt-sa`, mode `0750`
- Evidence directory: `/var/lib/solar-digital-twin/solarassistant/evidence`, `solardt-sa:solardt-sa`, mode `0750`

The password file contains only the password and an optional final newline. It
is not an environment file and must never be shell-sourced.

## Collector authority

The installed collector identity may read its password, execute the approved
runtime, connect outbound to the fixed SolarAssistant metrics endpoint, and
write its raw and retained SolarAssistant evidence. It may not modify, replace,
create, or delete the credential; read other collectors' credentials; modify
the runtime; administer `solardt`; use `sudo`; or change device configuration.

Raw NDJSON remains authoritative. Retained NDJSON remains a separate sibling
stream. Runtime path selection changes storage location only.

## Runtime preparation workflow

The reviewed `scripts/install_solarassistant_runtime.sh` has three modes:

- `--check` performs non-privileged source and design validation without changing the host.
- No argument performs the later administrator-approved installation.
- `--verify` performs metadata-only and access-boundary checks after installation; it never reads the password contents.

Real installation must be run by the trusted administrator only after the
script is committed and reviewed. It refuses a dirty working tree, creates or
verifies the fixed non-login account and directories, deploys only tracked
content from the current Git commit, and creates an administrator-owned virtual
environment from pinned `requirements.txt` plus the local package. It excludes
untracked files and therefore does not deploy `.git`, credentials, evidence,
reports, databases, caches, or temporary files. A previous dedicated runtime is
moved to a timestamped backup rather than silently deleted.

The script installs no credential, contacts no device, starts no collector, and
creates no systemd service. Package installation and all privileged actions
remain separately approved future operations.

Runtime source validation also includes the separate SolarAssistant
live-capture monitor module and foreground launcher documented in
`docs/SOLARASSISTANT_MONITOR.md`. Installed metadata verification confirms that
the monitor module can display `--help`; it does not start the monitor, bind a
port, read evidence or credentials, contact a device, or alter collector
operation. Deployment remains a later separately approved runtime action.

The reviewed installation sequence starts with the non-privileged command
`./scripts/install_solarassistant_runtime.sh --check`. Only with separate
approval, the administrator then runs the same script with no argument and later
with `--verify` under `sudo`. These are future operator actions, not authorization
to run them during repository development.

## Credential installation and replacement

The reviewed `scripts/install_solarassistant_credential.sh --check` validates
the fixed design without privilege or secret input. Its later no-argument mode
must be run by the trusted administrator from a controlling terminal. It
accepts no password argument, disables echo, requires matching entry twice,
rejects empty input, and atomically installs the fixed password file through a
restrictive temporary file. It prints no password and contacts no device.

Replacement uses the same installer. After initial installation or correction
following HTTP `401` or `403`, automated authentication remains stopped until
one separately approved manual collector verification succeeds. The installer
does not start or re-enable collection.

The completed credential action ran `scripts/install_solarassistant_credential.sh`
under `sudo` from Chris's normal terminal. The password was entered through the
controlling terminal and did not appear in the command.

The collector's credential precedence is:

1. `--password-file`, for the protected runtime file.
2. `SOLARASSISTANT_PASSWORD`, for backward-compatible controlled use.
3. A private interactive `getpass` prompt for manual verification.

The password itself is never a command-line option.

## Evidence and backups

The runtime passes `--output-dir` with
`/var/lib/solar-digital-twin/solarassistant/evidence`. The service identity owns
that directory so it can create, append, flush, and manage approved evidence.
Credential storage is separate and read-only to the collector.

Back up source, documentation, and appropriate evidence according to project
policy. Ordinary project backups must exclude plaintext credential files.
Credential recovery normally means secure re-entry, replacement, or rotation.

## Recovery

After VM loss, rebuild or restore the host and reviewed runtime from known-good
source and protected backups, recreate the approved identity and paths, and
securely re-enter the credential. Verify the runtime before resuming collection.

After confirmed `solardt` compromise, isolate or shut down the host, rebuild it
from known-good source and backups, verify it, rotate every potentially exposed
credential, and restore automation only after verification.

Collector failure must not change the device password or management access.
Device-account recovery remains independent of the collector.

## Manual authenticated verification

The collector ran once as `solardt-sa` at a 10-second interval for 25 seconds.
It used the protected password-file input, dedicated runtime Python environment,
and `/var/lib/solar-digital-twin/solarassistant/evidence`. The run stopped
cleanly without authentication rejection, wrote 126 approved raw records, and
created a separate retained NDJSON file. Raw receipt-time coverage was
`2026-07-16T05:41:34.125Z` through `2026-07-16T05:41:55.129Z`, representing
approximately three successful polling responses.

This was a short point-in-time verification, not a long-term operating
characterization. It confirmed combined, Battery 1, and Battery 2 topic families
for SOC, state of health, voltage, current, power, capacity, charge capacity,
cycle count, average/highest/lowest cell voltage, cell imbalance, battery
temperatures, temperature sensor readings, and MOS temperature. Representative
observations were 78% combined SOC, 79% Battery 1 SOC, 77% Battery 2 SOC,
53.3 V combined voltage, 53.4 V Battery 1 voltage, and 53.2 V Battery 2 voltage.
Combined current and power were zero during the short window.

## Deferred stages

Persistent systemd collection, numeric deadbands, SQLite normalization, and
portal integration remain deferred. The next bounded stage is a controlled
longer raw and retained capture at the normal 10-second interval, initially
targeting approximately 24 hours without enabling a persistent service.

The separate LAN-only live-capture monitor is implemented and offline-tested
but is not installed or running. Its later foreground `tmux` launch is distinct
from collector operation and includes no systemd service.
