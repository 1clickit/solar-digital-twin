# Next Task

## Objective

Add EG4 local portal systemd service.

## Context

The EG4 collector/report MVP is complete.

The current standard refresh command is:

./eg4_refresh_report.sh

The EG4 local portal MVP exists and passed a LAN browser smoke test.

## Data Source

Use existing CSV/report output under reports/.

Generated portal output should go under reports/ and should not be committed.

## Completed Portal MVP

Currently shows:

- system status
- battery SOC gauge
- AC-couple power gauge
- load gauge
- data freshness/latest source time
- latest engineering findings

## Rules

Do not modify collector behavior yet.
Do not add Home Assistant, SolarAssistant, ESP32, or control functions yet.
Do not add dependencies unless necessary.

## Success

A systemd service keeps the read-only EG4 local portal available without an open SSH terminal.
