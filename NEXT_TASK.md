# Next Task

## Objective

Establish and verify time synchronization for future EG4 and ESP32 forensic correlation.

## Scope

- confirm the solardt VM IPv4 address
- confirm the solardt timezone
- inspect the current solardt time-synchronization service
- configure solardt to serve time on the LAN if appropriate
- verify solardt remains synchronized to reliable upstream time sources
- document the verified configuration and test results

## Exclusions

- do not modify the ESP32 configuration yet
- do not implement event-correlation code
- do not change EG4 collection frequency
- do not modify EG4 collector behavior or SQLite schema
- do not change equipment settings

## Success

The solardt VM has a verified IPv4 address, uses America/Chicago, remains synchronized to upstream time, and is ready to provide reliable LAN time for the ESP32.
