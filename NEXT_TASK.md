# Next Task

## Objective

Begin a controlled longer SolarAssistant raw and retained evidence capture at
the normal 10-second polling interval, initially targeting approximately 24
hours, without yet enabling a persistent systemd service.

## Context

The dedicated `solardt-sa` runtime, protected credential, and `/var/lib`
evidence boundary are installed. The committed metadata and access-boundary
verification passed. A 25-second authenticated collector run at a 10-second
interval then completed successfully as `solardt-sa`, wrote 126 approved raw
records plus a separate retained NDJSON file, and confirmed the expected
combined, Battery 1, and Battery 2 telemetry. No service or long-running
collector was started.

The earlier deadband assessment remains insufficient for numeric thresholds.
This longer capture is intended to provide representative evidence for renewed
assessment, not to activate a retention policy or persistent service.

## Scope

1. Run the collector as `solardt-sa` using the protected password file, the
   dedicated runtime Python environment, and
   `/var/lib/solar-digital-twin/solarassistant/evidence`.
2. Poll at the normal 10-second interval and initially target approximately 24
   hours without creating or enabling a systemd service.
3. Preserve every approved observation in complete raw NDJSON and preserve the
   existing separate retained NDJSON output.
4. Seek natural coverage of daylight charging, overnight discharge, idle or
   near-zero current and power, ordinary load transitions, temperature
   evolution, and voltage and cell behavior across a wider SOC range.
5. After the capture, inspect evidence integrity, polling coverage, and storage
   growth, then use the resulting raw evidence for renewed deadband assessment.

## Boundaries

- Do not alter device settings or manipulate equipment solely to manufacture
  operating conditions; document naturally absent conditions.
- Stop immediately on HTTP `401` or `403` and require operator correction and
  a later manual verification before resuming automation.
- Retain the existing bounded handling for temporary network failures.
- Do not implement or approve numeric deadbands yet.
- Do not create or enable persistent systemd collection yet.
- Do not add SQLite normalization or portal integration yet.
- Preserve the separate runtime identity and credential boundary required while
  the SolarAssistant `admin` credential's effective authority remains unknown.
- Keep collector and retention mechanics modular for future devices and
  sensors; do not generalize SolarAssistant-specific thresholds prematurely.

## Success

An approximately 24-hour controlled run completes or yields a clearly
documented bounded result, with intact complete raw evidence, separate retained
evidence, understood storage growth, and enough naturally varied operating
coverage to support a renewed deadband assessment. Persistent service,
deadbands, SQLite, and portal work remain deferred.
