# Next Task

## Objective

Review and standardize time synchronization across all deployed solar equipment using solardt at 192.168.3.11 as the preferred LAN NTP server.

## Scope

- inventory all deployed solar equipment and supporting monitoring devices
- confirm each device's IPv4 address and network reachability
- identify each device's current time source, timezone, and NTP configuration
- determine which devices support configurable NTP servers
- include the ESP32 forensic logger, EG4 equipment, CP-100, BMS interfaces, and other relevant solar devices
- verify each supported device can reach solardt UDP port 123
- prepare the minimum configuration change needed to prefer 192.168.3.11
- retain reliable public NTP servers as fallbacks where supported
- document equipment that lacks configurable NTP or requires further interface research
- verify clock alignment after each future configuration change

## Exclusions

- do not upload firmware or deploy device configuration changes yet
- do not alter ESP32 thresholds or forensic-event logic
- do not change inverter, battery, charger, or protection settings
- do not implement EG4 and ESP32 correlation code
- do not change EG4 collection behavior

## Success

Every relevant solar device is inventoried and classified as synchronized, ready for configuration, unsupported, or requiring further research. A reviewed plan exists for making solardt the preferred NTP server wherever the equipment supports it.
