# Solar Digital Twin – Project Status

**Last Updated:** 2026-07-07

## Current Repository

`/home/chris/solar-digital-twin`

## Current Branch

`main`

## Last Verified Commit

`25b164e` — Add initial system configuration

## Completed

- Proxmox installed and configured.
- Home Assistant restored and operational.
- Ubuntu VM `solardt` created.
- Python virtual environment configured.
- Git repository initialized.
- Engineering Bible established.
- EG4 collector imported and working.
- Added `config/eg4.yaml`.
- Added `config/system.yaml`.
- Added `config/logging.yaml`.
- Runtime artifacts ignored by Git (`.gitignore`).
- EG4 collector reads configuration from YAML.
- EG4 username/password are prompted interactively and are not stored.
- Collector successfully tested on 2026-07-07.
- Repository verified clean after all commits.

## Current Development Rules

- One small tested commit at a time.
- Test before every commit.
- Engineering Bible is the design authority.
- Git is the source of truth for code.
- Preserve working functionality.
- Verify a clean working tree after every commit.

## Next Milestone

Create a shared configuration loader.

Objectives:

- One module loads all YAML configuration.
- Every collector uses the same configuration API.
- Keep the change to one small tested commit.
- Preserve existing collector behavior.
