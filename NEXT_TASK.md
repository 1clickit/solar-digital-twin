# Next Task

## Objective

Discuss and document telemetry-source roles and trust priorities before
selecting any primary source for portal display.

## Context

The standalone ESP32 SSE collector is implemented and manually verified.

ESP32 evidence now has canonical UTC receipt timestamps from the synchronized
`solardt` clock. ESP32 NTP requests to `solardt` have also been verified.

No decision has been made about which available source should be treated as
primary for display or engineering conclusions.

## Scope

- inventory the available telemetry sources
- distinguish authoritative, derived, forensic, and display roles
- compare measurement location, update rate, timestamp quality, and gaps
- compare known failure modes and uncertainty
- identify values that should be shown side by side rather than merged
- document decision criteria before choosing any primary source

## Exclusions

- no portal changes yet
- no database schema changes
- no source-priority decision before discussion
- no EG4-to-ESP32 correlation implementation yet

## Success

A documented source-role comparison and agreed decision criteria exist before
any source is designated primary for portal display.
