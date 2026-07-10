# Next Task

## Objective

Verify and normalize EG4 month energy units in the generated daily report.

## Existing Implementation

src/solar_digital_twin/reporting/eg4_daily_report.py

## Primary Output

reports/engineering_daily_report.md

## Completed Previous Work

The EG4 daily report now includes:

- Source file summary.
- Latest runtime snapshot.
- Latest energy snapshot.
- Day telemetry summary.
- Month energy summary using the latest non-empty day.
- Remote setting names read from raw JSON records.
- Plain-English engineering findings.

## Reason

The month energy CSV appears to report values such as `121.0`, while the daily energy snapshot reports values such as `12.7 kWh`.

The report should avoid misleading unit labels until the month-column scale is confirmed.

## Data Source

Read existing collector CSV output.

Do not modify the collector.

## Success

The month energy section clearly reports correct units or explicitly labels unconfirmed raw values.

## Notes

Keep this as a reporting-only change.