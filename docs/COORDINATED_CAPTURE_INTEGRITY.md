# Coordinated Capture Integrity Verification

## Result

Capture `solar-forensic-20260718T062127Z` passes immutable evidence integrity
verification with one provenance qualification. The intentional supervisor
SIGTERM is not a capture failure. The common manifest records all three source
stops with return code `-15`, successful restoration, and terminal state
`interruption` / `signal`. Every native evidence stream ends on a complete
newline-delimited record and remains suitable for bounded three-source offline
analysis.

The qualification is that the ESP32-specific append-only manifest contains its
valid start record but no terminal record. The common coordinated manifest
independently records the ESP32 stop, and the raw/current/conservative ESP32
files have clean endings, consistent coverage, and stable hashes. This limits
source-local terminal provenance but does not invalidate the preserved ESP32
telemetry. Later analysis must retain this qualification.

## Immutable identity

The isolated source is
`/var/lib/solar-digital-twin/coordinated/solar-forensic-20260718T062127Z`.
The tracked inventory is
`reports/solar-forensic-20260718T062127Z-inventory.tsv`; it records the relative
path, byte size, nanosecond modification time, and SHA-256 for every file.

- Inventory: 444 files and 685,044,693 bytes.
- Inventory TSV SHA-256:
  `4a26541c296957ed1a84dafd0ce95c62d06540802ab9c5876c0adbf50393b529`.
- Sorted absolute-path SHA-256 snapshot identity:
  `1add9b983da00d9996996ca21848d18965246e6dc34eace61d8ba76133b03a1c`.
- The complete 444-file SHA-256 snapshot matched before and after parsing and
  SQLite inspection.
- Source totals: EG4 435 files / 7,060,595 bytes; ESP32 5 files /
  605,453,571 bytes; SolarAssistant 3 files / 72,526,392 bytes; common manifest
  1 file / 4,135 bytes.

The common manifest has 11 valid records, begins at
`2026-07-18T06:21:27.574Z`, and ends at `2026-07-19T03:36:24.228Z`.
Its repository implementation identity is
`6b734306c6f414c6413f7c6e86e9d443e3fe49e2`. The actual coordinated interval
was 76,496.657 seconds, approximately 21 hours 14 minutes 57 seconds.

## Native-format integrity and coverage

### EG4

- SQLite immutable read-only `PRAGMA integrity_check` returned `ok`.
- There are 85 sync runs. Their local start times span
  `2026-07-18T01:21:28` through `2026-07-18T22:23:43`; median and maximum start
  gaps are 902 seconds, with no gap over 20 minutes.
- The database contains 85 runtime snapshots, 334 unique day-series samples,
  85 energy snapshots, 31 month-energy rows, and zero set records.
- Runtime server timestamps span `2026-07-18T06:19:34` through
  `2026-07-19T03:22:55` UTC. Median cadence is 845 seconds, maximum gap is 966
  seconds, and no gap exceeds 20 minutes.
- All 425 per-poll JSON files parse. All 340 runtime, energy, day, and month
  artifacts referenced in `evidence_files` exist and match their database
  SHA-256 values. The remaining 85 valid JSON files are per-run login metadata.
- The collector log contains no `error`, `traceback`, or `reconnect` marker and
  ends with the expected supervisor termination message.

### ESP32

- Raw: 764,161 valid records, 275,220,446 bytes, zero malformed records, zero
  backward timestamps, and a final newline. Receipt coverage is
  `2026-07-18T06:21:27.929Z` through `2026-07-19T03:36:20.723Z`.
- The primary frequency series has 76,408 samples over 76,492.655 seconds;
  median cadence is 1.001 seconds, maximum gap is 1.654 seconds, and no gap is
  over two seconds.
- All 17 approved entity IDs are present and no unapproved ID is present.
- Current `esp32-frequency-v1`: 713,435 valid records and 266,259,706 bytes.
  Every record is an ordered exact-byte subsequence of raw.
- Canary-only `esp32-conservative-v1`: 151,815 valid records and 63,972,840
  bytes. Every record is an ordered exact-byte subsequence of raw.
- Neither retained stream has malformed records, backward timestamps, or a
  missing final newline. This verification does not promote the conservative
  policy; `esp32-frequency-v1` remains production.
- The collector log contains only the expected supervisor termination message.

### SolarAssistant

- Raw: 305,172 valid records and 70,969,608 bytes, zero malformed records,
  zero backward timestamps, and a final newline.
- There are 7,266 complete polls, each containing all 42 observed topics.
  Receipt coverage is `2026-07-18T06:21:28.435Z` through
  `2026-07-19T03:36:11.334Z`; median poll cadence is 10.532 seconds, maximum
  gap is 11.377 seconds, and no gap is over 20 seconds.
- Retained: 5,951 valid records, 1,556,735 bytes, 12 retained topics, zero
  malformed records, zero backward timestamps, and a final newline.
- The collector log contains only the expected supervisor termination message.

## Interpretation and next boundary

The three source intervals overlap throughout the controlled run and have no
integrity gap that blocks offline correlation. Source cadence still limits
event timing: EG4 is approximately 15-minute telemetry, while SolarAssistant
is approximately 10 seconds and ESP32 approximately one second. Analysis must
align without interpolation, preserve trusted SolarAssistant battery context,
and keep cloud cover, load, battery constraints, aggregation, source timing,
and electrical/control behavior as explicit alternatives.

No evidence, database, device, credential, permission, collector, service,
monitor, portal, or production retention setting was changed. The next bounded
work unit is three-source offline correlation and raw/current/conservative
ESP32 comparison, followed by owner review before any new capture or local
dongle measurement.
