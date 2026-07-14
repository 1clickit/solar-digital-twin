# ESPHome Firmware

## EG4 Forensic Probe v3

Device name: `eg4-forensic-logger`

Friendly name: `EG4 Forensic Probe v3`

Source file:

- `firmware/esphome/eg4_forensic_probe_v3.yaml`

## Purpose

This ESP32 device is a forensic telemetry logger for Solar Digital Twin event correlation.

It is intended to support review of EG4 AC-couple events by providing local, higher-frequency electrical observations near the inverter/AC-couple measurement point.

## Secrets

Wi-Fi credentials must not be committed.

The ESPHome YAML must use:

- `ssid: !secret wifi_ssid`
- `password: !secret wifi_password`

Local ESPHome secrets belong in `firmware/esphome/secrets.yaml`.

That file is ignored by Git and must remain local only.

## Limitations

The ESP32 telemetry is supporting evidence for correlation.

It should not be treated as final proof of an individual microinverter failure or dropout by itself.

EG4 aggregate data, ESP32 telemetry, timestamps, weather/cloud context, and reviewed event windows should be considered together.

## Planned LAN configuration

Planned next steps:

- Configure a static IPv4 address for the ESP32.
- Configure LAN NTP with the `solardt` VM as the preferred time source.
- Keep public NTP fallback only if needed.
- Collect 1-second telemetry for correlation with EG4 AC-couple events.
