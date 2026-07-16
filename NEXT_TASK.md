# Next Task

## Objective

Perform an offline-only investigation and tested correction of the
SolarAssistant live monitor's fresh-data `Unknown` status badge.

## Context

The dedicated runtime is installed under `/opt/solar-digital-twin`; its
administrator-controlled credential remains protected outside Git. A capture
begun at approximately `2026-07-16 02:00 America/Chicago` is running as
`solardt-sa` in root-owned detached tmux session `solarassistant-24h`, with a
configured duration of 86,400 seconds and automatic completion expected. The
read-only monitor runs as `solardt-sa` in root-owned detached tmux session
`solarassistant-monitor` at `http://192.168.3.11:8792`; its health endpoint
returned `{"status":"ok"}`.

Fresh capture data is visible, but the status badge displays `Unknown`. This is
a minor deferred correction, not a capture blocker. Collector PID 92638 and
monitor PID 92674 were observed historically; these transient PIDs are not
stable runtime configuration.

## Scope

1. Reproduce the fresh-data `Unknown` badge using repository-local fixtures or
   tests without reading or changing live evidence.
2. Identify and document the cause before changing behavior.
3. Implement the smallest offline correction and add focused tests that cover
   fresh, stale, and relevant process/countdown states.
4. Preserve the monitor's read-only evidence operation and collector isolation.

## Boundaries

- Do not stop, restart, signal, attach to, inspect interactively, redeploy, or
  modify the active collector or monitor without Chris's explicit approval.
- Do not deploy the correction during the active capture.
- Do not alter `/opt/solar-digital-twin`, the installed collector, credentials,
  retained-output behavior, evidence, tmux sessions, or runtime state.
- Safe development may continue only when it cannot alter the installed
  collector or retained-output behavior.
- Preserve monitor read-only operation: no device requests, credential access,
  or evidence writes.
- Require Chris's explicit approval before any later deployment.

## Success

The badge cause is reproduced and explained offline, the smallest correction is
covered by focused tests, and read-only monitor behavior and collector
isolation remain intact. No deployment or live-runtime action occurs.
