# Next Task

## Objective

Add an engineering findings section to the generated EG4 daily report.

## Existing Implementation

src/solar_digital_twin/reporting/eg4_daily_report.py

## Primary Output

reports/engineering_daily_report.md

## Completed Previous Work

The EG4 daily report now:

- Reads existing collector CSV output.
- Summarizes source files.
- Shows latest runtime data.
- Shows latest energy data.
- Summarizes day telemetry.
- Reads remote setting names from raw JSON records.
- Ignores empty future month energy rows.

## Data Source

Read the existing CSV reports produced by the EG4 collector.

Do not modify the collector.

## Success

The Markdown report includes a plain-English engineering findings section that highlights notable conditions such as AC-couple activity, low/off samples, latest real month-energy day, and recent remote setting changes.

## Notes

Keep this as a reporting-only change.
