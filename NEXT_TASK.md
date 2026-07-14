# Next Task

## Objective

Plan read-only ESP32 forensic telemetry collection for EG4 AC-couple event correlation.

## Context

The ESPHome forensic logger config has been saved in the repository and OTA-deployed to the live ESP32.

Current deployed ESP32 forensic logger:

- hostname: `eg4-forensic-logger.local`
- static IPv4: `192.168.3.13`
- preferred LAN NTP server: `192.168.3.11`
- web portal reachable on port 80 from solardt

## Scope

- inspect the ESPHome device's read-only telemetry access options
- identify which 1-second values are available from the ESP32
- determine whether ESPHome native API, web endpoint, logs, or another read-only method is best for collection
- document fields useful for EG4 AC-couple correlation
- define the smallest safe collector/reporting step
- keep timestamp alignment with Central time and LAN NTP in mind

## Exclusions

- do not change ESP32 thresholds or forensic-event logic
- do not change inverter, battery, charger, or protection settings
- do not implement full EG4 and ESP32 correlation code yet
- do not change EG4 collection behavior
- do not add database schema changes yet
- do not commit or display Wi-Fi secrets

## Success

A reviewed plan exists for collecting ESP32 1-second telemetry read-only from solardt and using it later for EG4 AC-couple event correlation.
