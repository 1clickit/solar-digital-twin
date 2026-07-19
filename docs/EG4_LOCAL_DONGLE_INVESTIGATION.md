# EG4 Local Wi-Fi Dongle Investigation

## Purpose and status

This is public-source-only preparation for a possible strictly read-only Solar
Digital Twin connection to the existing EG4 Wi-Fi dongle. No LAN request was
sent and no client was implemented. Coordinated-capture integrity review and
three-source analysis remain the active milestone.

The previously observed endpoint is `192.168.3.20:8000`; its ARP-observed MAC
was `d8:3b:da:21:92:c8`. The dongle remains attached to the inverter and may
continue cloud reporting. A local connection is a second transport from the
same inverter, not ownership of its physical RS-485 bus and not an independent
physical measurement.

Preferred later flow is `EG4 inverter -> existing Wi-Fi dongle -> local TCP
8000 -> solardt`, then source-labeled validation and selected read-only exports
from `solardt` to Home Assistant.

## Pinned public sources

Research used temporary `/tmp` clones only:

- [`joyfulhouse/eg4_web_monitor` commit `485bc613448d57917c6e4d01e42f128aa4ecbbb3`](https://github.com/joyfulhouse/eg4_web_monitor/tree/485bc613448d57917c6e4d01e42f128aa4ecbbb3),
  integration version `3.5.1-beta.2`;
- its [manifest](https://github.com/joyfulhouse/eg4_web_monitor/blob/485bc613448d57917c6e4d01e42f128aa4ecbbb3/custom_components/eg4_web_monitor/manifest.json)
  specifies `pylxpweb>=0.9.39b3`, not an exact resolver lock;
- the minimum compatible release studied is `pylxpweb` tag `v0.9.39b3`,
  [commit `889f1ba2d55d23efe2e5fdaa0dbdc50c4adc35ab`](https://github.com/joyfulhouse/pylxpweb/tree/889f1ba2d55d23efe2e5fdaa0dbdc50c4adc35ab).

Both repositories use the MIT License. Copied or substantially derived source
must retain its copyright and license. Findings below distinguish source facts,
upstream claims, engineering inferences, and unresolved questions.

## Protocol and framing

**Source fact:** pinned
[`dongle.py`](https://github.com/joyfulhouse/pylxpweb/blob/889f1ba2d55d23efe2e5fdaa0dbdc50c4adc35ab/src/pylxpweb/transports/dongle.py)
implements a proprietary LuxPower/EG4 TCP envelope carrying translated Modbus
RTU-style operations. It is not ordinary Modbus TCP.

A translated request contains:

- magic `a1 1a`, little-endian protocol version `1`, and frame length;
- address `01` and TCP function `c2` (`c1` heartbeat, `c3` parameter read,
  and `c4` parameter write are also defined);
- ten-byte padded/truncated ASCII dongle serial and data length;
- request action `00`, embedded Modbus function, ten-byte inverter serial,
  little-endian register/count or value fields; and
- little-endian CRC-16/Modbus over the embedded data frame.

There is no Modbus-TCP MBAP transaction identifier in this envelope. Responses
are checked for TCP function, inverter serial, Modbus function, start register,
count/length, and CRC. The parser searches for `a1 1a` because unsolicited or
stale bytes may precede a response.

**Source fact:** both ten-character serials are required and embedded. Factory
documentation calls them an authentication requirement, but the transport has
no separate password, token, login, or challenge-response. Serial possession
may be weak identification/authentication; vendor intent remains unresolved.

## Read/write boundary

Translated `c2` plus embedded function `03` reads holding/configuration
registers; `04` reads input/runtime registers. Proven read calls include
`read_device_type`, `read_serial_number`, `read_firmware_version`,
`read_parallel_config`, `read_runtime`, `read_energy`, `read_battery`,
`read_midbox_runtime`, and `read_parameters`.

Embedded `06` writes one holding register and `10` writes multiple registers;
TCP function `c4` is parameter write. The integration exposes control paths for
quick charge, modes, SOC/voltage/current/power limits, sell-back, peak shaving,
forced discharge, and smart ports. Hiding entities does not make it read-only.

A Solar Digital Twin client must omit `06`, `10`, `c4`, generic named writes,
cloud control fallbacks, and all control objects by construction. It must
allowlist only `03` and `04` and reject any write selection.

## Register/read groups

Pinned
[`_register_data.py`](https://github.com/joyfulhouse/pylxpweb/blob/889f1ba2d55d23efe2e5fdaa0dbdc50c4adc35ab/src/pylxpweb/transports/_register_data.py)
defines:

| Group | Input registers | Source description |
|---|---:|---|
| `power_energy` | 0-31 | power, voltage, SOC/SOH, current |
| `status_energy` | 32-63 | status, energy, fault/warning codes |
| `temperatures` | 64-79 | temperatures, currents, fault history |
| `bms_data` | 80-112 | BMS pass-through |
| `extended_data` | 113-153 | parallel, generator, EPS, per-leg, AC-couple |
| `eps_split_phase` | 140-142 | EPS L1/L2 voltages |
| `output_power` | 170-173 | output power and load energy |
| `split_phase_grid` | 193-204 | split-phase grid voltage/per-leg power |

Other pinned reads include inverter serial at input 115-119, parallel config at
input 113, quick-charge remaining time at input 210, and individual batteries
at input 5000 onward. Device type is holding 19; firmware is holding 7-10;
parameter reads are holding-register chunks of at most 40. GridBOSS/MID groups
are input 0-39, 40-67, 68-107, 108-119, and 128-131, plus holding 20 for smart
port mode.

These cover runtime, energy, battery, temperature, status, faults/warnings,
frequency, generator/EPS, AC-couple, identity, firmware, and configuration.
Actual model support and scaling must be verified from pinned mappings; a
register's presence does not prove its value is valid on Chris's inverter.

## Polling, blocks, validation, and recovery

**Documentation claim:** pinned README/configuration prose describes five-second
local/dongle updates and 60-minute parameter refresh.

**Source fact:** the pinned transport constants instead default wired Modbus to
5 seconds and Wi-Fi dongle to **30 seconds**, noting dongle reads take about
8-10 seconds; the selectable dongle range is 5-300 seconds. The coordinator
uses the transport-specific value. Code controls at this checkpoint, so the
five-second dongle prose is stale or generic. A future first test must be one
shot, not recurring.

The conservative plan uses groups no larger than 40. Fast mode can coalesce up
to 125; 120 is an upstream field claim for some DG firmware. Older firmware may
reject blocks above about 40, triggering fallback. GridBOSS/MID stays at 40 or
less because larger reads failed on upstream hardware.

The transport serializes connections, transactions, and multi-step operations;
drains pending bytes; rejects wrong function/serial/range, short frames, bad
CRC, and Modbus exceptions; and tears down suspect sockets after timeout, EOF,
or socket failure. Reads do not resend after timeout; later polling reconnects.
Other transient failures have bounded retries. Connection setup uses three
attempts with exponential delays; integration re-attachment is floored at 60
seconds.

## Firmware and multiple-client risk

**Upstream claim:** newer firmware may block port 8000. The observed open port
does not prove translated reads are accepted.

**Upstream claim strongly reflected in code:** the dongle has one TCP slot.
Connection creation/closure is serialized, and source warns to disable other
clients. It also handles unsolicited, cloud-proxied, stale, and misrouted
frames, suggesting cloud/local contention is plausible.

The upstream
[`collision_test.py`](https://github.com/joyfulhouse/eg4_web_monitor/blob/485bc613448d57917c6e4d01e42f128aa4ecbbb3/scripts/collision_test.py)
does not establish safe coexistence. It constructs ordinary Modbus-TCP MBAP
frames, uses private hard-coded test endpoints, opens parallel connections, and
commits no results. Its port-8000 request does not match `DongleTransport`'s
envelope. It is only an experimental harness; multiple-client safety remains
unresolved and the single-client warning controls.

## Security and provenance

- LAN-only; no WAN exposure.
- No credential is proven beyond device serial identifiers; keep serials out of
  ordinary logs/chat and preserve them only in protected raw provenance.
- Label source `EG4 local Wi-Fi dongle` and transport `LuxPower/EG4 translated
  Modbus over TCP 8000`.
- Cloud and dongle are two transports from one inverter, never independent
  physical corroboration.
- SolarAssistant/JK BMS remains the independent trusted battery source.
- Exports to Home Assistant retain origin/lineage and cannot be re-ingested as
  independent evidence.

## Proposed strictly read-only client and evidence plan

A future small independent client, not the control-capable HA integration,
must expose only an explicit `03`/`04` register allowlist; contain no write API;
validate complete framing and identity; serialize one connection/request; use
blocks no larger than 40; stop rather than reconnect aggressively; and preserve
exclusive raw request/response frames with UTC receipt time, source/software
identity, interpretation, and SHA-256. Decoding is separate and raw frames are
immutable. Home Assistant must not be a second local poller during the test.

After integrity validation, compare local fields with existing cloud evidence
by UTC and meaning: latency, cadence, scaling, gaps, fault/warning, frequency,
AC-couple power, and state. Agreement validates transport mapping; it is not
independent physical confirmation.

## Candidate initial transaction

Pinned source proves `DongleTransport.read_device_type()` is structurally
read-only: translated `c2`, embedded `03`, holding register 19, count 1:

`await DongleTransport(host, dongle_serial, inverter_serial).read_device_type()`

However, **no exact live transaction is ready for authorization**. Exact bytes
depend on the unrecorded serials and resulting CRC, and single-client/cloud
coexistence is unresolved. A later work unit must obtain identifiers through an
approved external mechanism, confirm no other local poller, select a safe test
window, define an exclusive raw artifact, and review the final frame before one
request.

## Stop conditions, rollback, and next gate

Stop if the frame is not solely `c2` plus `03`/`04`; authentication, a write,
or configuration is requested; another local client exists; cloud/device
operation changes; the TCP slot appears held; framing, identity, CRC, or range
is unexpected; firmware rejects the conservative request; rapid reconnect is
needed; or raw evidence cannot be exclusively preserved.

Rollback is closing the one socket and sending nothing further. Do not restart
the dongle, inverter, HA, collectors, or services automatically.

Unresolved: exact serials, firmware, port-8000 protocol acceptance, single-slot
coexistence with cloud traffic, unsolicited-frame behavior, exact inverter
family, and the smallest useful allowlist. The next gate remains immutable
capture inventory and three-source analysis, followed by owner review and a
separately authorized one-shot transaction with exact bytes and stop criteria.
