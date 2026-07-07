# Solar Digital Twin – Project Status

**Last Updated:** 2026-07-07

## Current Repository

`/home/chris/solar-digital-twin`

## Current Branch

`main`

## Last Verified Commit

`1d91f1e` — Configure EG4 collector with YAML

## Completed

- Proxmox installed and configured.
- Home Assistant restored and operational.
- Ubuntu VM `solardt` created.
- Python virtual environment configured.
- Git repository initialized.
- Engineering Bible established.
- EG4 collector imported and working.
- Added `config/eg4.yaml`.
- EG4 collector now reads serial/database/evidence/reports paths from YAML.
- EG4 username/password are prompted interactively and are not stored.
- Collector successfully tested on 2026-07-07.

## Current Development Rules

- One small tested commit at a time.
- Test before every commit.
- Engineering Bible is the design authority.
- Git is the source of truth for code.
- Preserve working functionality.

## Next Milestone

Standardize project configuration:

```text
config/
    eg4.yaml
    system.yaml
    logging.yaml
