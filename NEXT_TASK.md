# Next Task

## Objective

Create a clean read-only local EG4 web portal MVP.

## Context

The EG4 collector/report MVP is complete.

The current standard refresh command is:

./eg4_refresh_report.sh

The next milestone is to see the collected EG4 data as a useful local web portal.

## Data Source

Use existing CSV/report output under reports/.

Generated portal output should go under reports/ and should not be committed.

## First Portal Version

Show:

- system status
- battery SOC gauge
- AC-couple power gauge
- consumption gauge
- data freshness/latest source time
- latest engineering findings

## Rules

Do not modify collector behavior yet.
Do not add Home Assistant, SolarAssistant, ESP32, or control functions yet.
Do not add dependencies unless necessary.

## Success

A local generated HTML dashboard can be opened and viewed as a useful EG4 status portal.
