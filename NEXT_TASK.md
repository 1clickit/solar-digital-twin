# Next Task

## Objective

Perform the reviewed installation of the dedicated `solardt-sa` runtime
identity, administrator-owned runtime, and writable evidence boundary, then
verify the resulting metadata and permissions without installing a
SolarAssistant credential or contacting the device.

## Context

Commit `39548b1` completed the repository-side collector support, runtime and
credential installer scripts, offline tests, and operating documentation. The
scripts have not been run in privileged mode. No account, system path,
credential, service, or live collection has been created.

## Scope

1. Confirm the repository is clean and synchronized at the approved commit.
2. Run `scripts/install_solarassistant_runtime.sh --check` without privilege and review its fixed identity, paths, and planned actions.
3. Run the committed runtime installer in its administrator installation mode.
4. Permit only the installer to create or verify `solardt-sa`, create the approved directories, deploy tracked content into `/opt/solar-digital-twin`, build the administrator-owned virtual environment, install pinned requirements and the local package, and apply documented metadata.
5. Run the committed metadata-only `--verify` mode.
6. Confirm the account is non-login, the runtime is not writable by `solardt-sa`, the evidence directory is writable by it, the credential directory has approved metadata, the collector import or executable path works, and the repository remains clean.

## Boundaries

- `sudo` is authorized only for the reviewed committed runtime installer and its documented verification mode during that separately approved work unit.
- Stop before installing or entering the SolarAssistant password.
- Stop before device contact, authentication, collector execution against the device, evidence capture, or systemd work.
- Do not improvise unrelated privileged commands. If the installer reports a defect, stop and return to repository-side correction instead of bypassing it manually.
- Credential installation, manual authenticated verification, the longer capture, deadband work, persistent service operation, SQLite, and portal integration remain separate later stages.

## Success

The dedicated account, administrator-owned runtime, credential-directory
boundary, and writable evidence directory are installed and pass the committed
metadata-only verification without creating a password file, contacting
SolarAssistant, starting collection, or enabling a service.
