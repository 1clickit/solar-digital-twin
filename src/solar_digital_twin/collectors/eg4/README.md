# EG4 Portal Connector v4

This version turns the EG4 portal reverse-engineering work into a local Digital Twin connector.

## What it does

`eg4_sync.py` logs into the EG4 portal, downloads known API datasets, saves raw JSON evidence, updates SQLite, and exports CSV reports.

Current endpoints:

- `/WManage/api/inverter/getInverterRuntime`
- `/WManage/api/inverter/getInverterEnergyInfo`
- `/WManage/api/analyze/chart/dayMultiLine`
- `/WManage/api/inverterChart/monthColumn`
- `/WManage/web/maintain/remoteSetRecord/list`

## Install

From PowerShell inside this folder:

```powershell
python -m pip install requests
```

## Credentials

Set these in PowerShell:

```powershell
$env:EG4_USERNAME="your_username"
$env:EG4_PASSWORD="your_password"
```

## Run

```powershell
python .\eg4_sync.py --serial 44830P0125 --date 2026-07-03 --db ".\eg4_digital_twin.sqlite" --verbose
```

For today's date, you can omit `--date`:

```powershell
python .\eg4_sync.py --serial 44830P0125 --db ".\eg4_digital_twin.sqlite"
```

## Output

```text
evidence\YYYYMMDD_HHMMSS\   raw JSON evidence and metadata
reports\                     CSV reports and analysis_summary.txt
eg4_digital_twin.sqlite       local Digital Twin SQLite cache
```

## Notes

- Raw JSON evidence is kept unchanged.
- SQLite tables use `INSERT OR REPLACE`, so rerunning the same day updates existing samples instead of creating duplicates.
- Energy fields that EG4 stores as tenths are converted to kWh in the snapshot table, while raw JSON is still preserved.
