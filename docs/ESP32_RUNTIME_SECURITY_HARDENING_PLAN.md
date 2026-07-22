# ESP32 Runtime and Security Hardening Plan

## Status and phase boundary

Repository implementation is complete and offline-tested. The design was based
on the static review at commit
`140f6fd4f9f4d9bc1daa4e9e7c0e59e9e43e658c` and implemented from checkpoint
`b1e821964427f62fa45237a8f915760146e817cc`.

The repository contains the hardened collector, focused tests, a credentialless
runtime installer, a fixed-provenance launcher, and a dormant systemd unit.
Installation and metadata-only verification completed successfully on
`solardt` from commit `7f2274b9011c4bb85f3099eb80c8bb86a21f0e04`.
During installation, no service was started or enabled, no evidence was
created, and no device was contacted.

The future work is separated into four gates:

1. repository-only implementation — **complete**;
2. separately approved installation on `solardt` — **complete**;
3. separately approved short passive live verification — **complete**; and
4. a later owner decision for persistent or long-duration operation.

Approval of one gate does not authorize another.

## Installation result

The tracked whole-application runtime is installed at
`/opt/solar-digital-twin` with an exact commit marker. The prior shared runtime
is preserved at `/opt/solar-digital-twin.backup.20260720T205254Z`; installer
rollback was not invoked. The fresh virtual environment completed successfully,
although pip warned that pinned `charset-normalizer==3.4.8` was yanked without
a stated reason. This remains a dependency-maintenance observation, not an
installation failure.

The new system identity `solardt-telemetry` has observed UID/GID `996/989`,
home `/nonexistent`, shell `/usr/sbin/nologin`, and only its same-named primary
group. Trusted reporter `chris` was added to that group; read/traverse passed
and write access was denied. Existing `solardt-telemetry-readers` was not
modified or repurposed. State and evidence directories are
`solardt-telemetry:solardt-telemetry` mode `0750`; the evidence file count was
zero. No ESP32 credential path exists.

The installed unit exactly matches the repository artifact and is
`root:root 0644`, static, inactive, and dead. It has no timer, trigger,
activation symlink, automatic start path, or collector process.

## Passive live-verification result

On July 20, 2026, a minimal header-only probe to the fixed credentialless URL
returned HTTP `200`, exact `Content-Type: text/event-stream`, the unchanged
final URL, and zero redirects without printing or retaining a body. The
installed static service then ran exactly once through its unchanged 3,600-
second `current` launcher as `solardt-telemetry`.

Capture `esp32_sse_20260720_214207Z` completed successfully with 35,968 raw and
33,515 `esp32-frequency-v1` retained records. Its manifest contained one start
and one clean completion record with stop reason `duration` and installed
collector version `7f2274b9011c4bb85f3099eb80c8bb86a21f0e04`. JSON/schema,
fixed source URL, 17-entity allowlist, nondecreasing UTC receipt time,
raw/retained byte identity and ordering, ownership/modes, and payload-free
journal checks passed. No conservative or canary output was created.

The service finished with result success, exit status 0, 9.599 seconds CPU,
40.9 MiB peak memory, no swap, and zero restarts. It returned static,
inactive, and dead with no timer, trigger, process, credential path, or
automatic activation. No firmware, ESPHome, network, authentication, or device
configuration changed. Evidence is preserved under the installed evidence path.

## Post-hardening endurance-capture result

Finite capture `esp32_sse_20260721_041439Z` ran from
`2026-07-21T04:14:39.139Z` through `2026-07-21T16:00:01.177Z` using installed
collector version `7f2274b9011c4bb85f3099eb80c8bb86a21f0e04` and current policy
`esp32-frequency-v1`. It produced 422,744 raw and 391,241 retained records.
Read-only integrity review and deterministic replay passed, and Chris accepted
the result as **PASS WITH ONE QUALIFICATION**. The complete evidence identities,
checks, ownership reconciliation, and result are recorded in
`docs/capture_analyses/esp32_sse_20260721_041439Z-integrity.md`.

The qualification is that systemd ignored `RuntimeMaxSec` for the transient
`Type=oneshot` unit, leaving the collector's successfully completed finite
`--duration` as the automatic stop mechanism. This does not invalidate the
evidence. A host-enforced ceiling requires separate design review before any
future endurance launch. This finite result creates no timer, enablement, or
persistent service authority; the persistent-operation owner decision remains
unmade.

## Repository implementation result

The implemented client uses a dedicated Requests session with environment
proxy use disabled, rejects redirects, accepts only HTTP `200`, retries only
`429`, `500`, `502`, `503`, and `504` plus transport failures, and treats every
other HTTP status as permanent. `Retry-After` is numeric-only and locally
capped at 30 seconds; malformed values fall back to the existing capped
backoff.

Before stream parsing, the collector requires `text/event-stream`
case-insensitively and permits compatible parameters. A byte-level iterator
reads 8 KiB transport chunks and limits each complete raw SSE line, excluding
its line terminator, to 1 MiB before UTF-8 decoding or JSON parsing. Every
response closes in a `finally` path, and diagnostics use fixed categories,
safe status-derived categories, exception class names, and bounded delay only.

Exclusive output creation now explicitly applies mode `0640`; newly created
output directories are `0750`. Record fields, timestamps, manifests,
allowlist, raw-first ordering, retained-writer isolation, reconnect state,
policy meanings, and the `esp32-frequency-v1` default are unchanged.

Repository artifacts are `scripts/install_esp32_runtime.sh`,
`scripts/run_esp32_forensic_collector.sh`, and
`systemd/esp32-forensic-collector.service`. The installer supports `--check`,
`--install`, and `--verify`; whole-application replacement preserves a prior
runtime and refuses an unmarked legacy shared runtime unless an administrator
explicitly accepts it after inspection. The unit has a fixed one-hour
foreground invocation, `Restart=no`, no timer, and no `[Install]` target.

The actual device `Content-Type`, installed account/path state, shared-runtime
compatibility, and one-hour resource behavior are verified as recorded above.
No production resource limits were invented, and persistent operation remains
an unmade owner decision.

## 1. Objective and non-objectives

The objective is to prepare a safer unattended host runtime for the passive,
read-only ESPHome SSE collector while preserving:

- authoritative raw evidence;
- UTC receipt timestamps and current provenance semantics;
- the exact 17-entity sensor allowlist;
- fixed credentialless LAN collection;
- raw-before-derived ordering;
- independent retained-policy outputs and failure state;
- `esp32-frequency-v1` as the default retention policy; and
- the absence of every device-control or configuration path.

Non-objectives are ESP32/ESPHome firmware changes, enabling device
authentication, VLAN or firewall redesign, Home Assistant integration,
retention-default changes, database normalization, portal work, a long-duration
capture, persistent service activation, and device-control functionality.

## Static findings and evidence

Classification terms are limited to **confirmed by current source**, **already
mitigated**, **partially supported**, **not supported**, and **requires runtime
verification**.

| # | Candidate | Classification | Current evidence and consequence |
|---:|---|---|---|
| 1 | Fixed unauthenticated LAN HTTP SSE URL | **confirmed by current source** | `esp32_sse.py:22` fixes `http://192.168.3.13/events`; lines 301–305 issue a streaming GET without credentials. `docs/ESP32_FORENSIC_TELEMETRY_PLAN.md` records the verified passive endpoint. Preserve the fixed IPv4 destination and credentialless role. |
| 2 | Explicit sensor allowlist | **already mitigated** | `APPROVED_IDS` at lines 28–46 contains 17 IDs; line 341 rejects all others. `test_allowlist_and_receipt_timestamp_are_unchanged` verifies filtering and record shape. Preserve it. |
| 3 | Raw written before retained outputs | **already mitigated** | Lines 353–362 encode, write, and flush raw before invoking each retained writer. `test_raw_is_flushed_before_retained_processing_and_records_match` checks exact order and unchanged retained bytes. |
| 4 | Derived-writer failures do not stop raw collection | **already mitigated** | `RetainedOutput.process` catches processing/write/flush failures independently; open and close failures disable only that writer. Tests cover retained open, processing, write, flush, and two-policy isolation. A raw write/flush failure correctly stops collection and is manifested. Preserve this behavior and add only regression coverage needed by HTTP refactoring. |
| 5 | Output collision and prior-file mixing | **already mitigated** | `_assert_outputs_absent` checks all selected paths before network access; manifest, raw, and retained files use exclusive mode `x` at lines 281, 289, and 292–294. `test_any_existing_canary_path_refuses_before_network_or_truncation` verifies refusal and preservation. |
| 6 | Reconnect is bounded and preserves state | **partially supported** | Backoff starts at 1 second and is capped at 30 seconds (lines 271–272, 377–387); policy instances remain outside the reconnect loop, and two tests prove current/canary state survives reconnect. However, total attempts are unlimited for duration `0`, and every `RequestException` follows the same retry path. Preserve state and capped delay, then add explicit permanent/transient rules and bounded service operation. |
| 7 | Redirects are not explicitly prohibited | **confirmed by current source** | The `requests.get` call supplies no `allow_redirects=False`; Requests follows GET redirects by default. Future code must reject redirects rather than follow a new destination. |
| 8 | Environment proxies are not explicitly bypassed | **confirmed by current source** | The module-level Requests API is used without a `Session` whose `trust_env` is false. Future code must ignore proxy environment configuration for this fixed LAN endpoint. |
| 9 | SSE content type is not validated | **confirmed by current source** | The request sends `Accept: text/event-stream`, but after `raise_for_status()` no response `Content-Type` check occurs. Future code must accept `text/event-stream` case-insensitively with optional compatible parameters such as `charset`, and reject other media types. |
| 10 | Incoming line/event size has no explicit bound | **confirmed by current source** | `response.iter_lines(chunk_size=1, decode_unicode=True)` does not impose an application line limit before JSON parsing. Future code must enforce a documented maximum without logging rejected payloads. |
| 11 | Permanent HTTP rejection and transient failure are not distinct | **confirmed by current source** | `raise_for_status()` and the single `except requests.RequestException` path retry all HTTP/transport failures alike. Future code must stop on redirects, unsupported content, and permanent 4xx responses; retry only bounded transient transport failures, selected 5xx responses, and carefully bounded `429` if supported. |
| 12 | Explicit payload-free and secret-free logging policy | **partially supported** | Retained-writer diagnostics print only output label and exception type, and tests prove private exception text is omitted. JSON failures are silently skipped. The connection path prints the full exception string at lines 382–385, and no explicit policy covers future HTTP validation. Replace it with fixed categories, status/error type, and bounded delay; never log response bodies, SSE lines, headers, environment values, or credentials. |
| 13 | No dedicated installed runtime identity | **requires runtime verification** | Repository history documents the standalone run as user `chris`; `SECURITY_MODEL.md` classifies ESP32 SSE for a shared telemetry identity, but no ESP32 runtime installer/unit or completed installation is documented. Installation-phase metadata checks must confirm actual host state; this planning work does not inspect users or runtime paths. |
| 14 | Retention-policy selection must remain unchanged | **already mitigated** | `RETENTION_MODES` and `parse_args` default to `current`; `_retained_outputs` maps it only to `esp32-frequency-v1`. `test_default_mode_does_not_open_conservative_output` verifies no conservative output in default mode. Hardening must not change these semantics. |
| 15 | Firmware/device security is separate from host runtime hardening | **already mitigated** | The collector contains one GET-only telemetry path and no firmware, OTA, native API, service call, or control function. Security and recovery documents keep ESPHome secrets/management separate. Firmware/authentication/network changes remain separate future decisions. |

## 2. Threat and failure model

Apply the approved practical Home Assistant-style trusted-host model. Protect
against realistic accidental and LAN-origin failures without vaults,
containers, TLS infrastructure, or enterprise identity complexity that does
not reduce plausible risk.

The future design must address:

- malformed or unexpectedly large SSE responses consuming memory or collector
  availability;
- proxy environment variables routing a fixed LAN request elsewhere;
- HTTP redirects changing destination or transport;
- a successful HTTP response carrying HTML, JSON, or another unexpected type;
- unbounded capture duration, file growth, or retry activity;
- timestamp-name collision and evidence mixing;
- retained-output failure affecting authoritative raw evidence;
- payload-rich diagnostics entering the journal;
- accidental service start, enablement, timer activation, or restart loop;
- a collector identity with repository, credential, administrative, or
  unrelated runtime authority;
- evidence permissions that force routine trusted analysis through repeated
  administrator intervention; and
- duplicate collection or unclear provenance when Home Assistant also observes
  the ESP32.

The fixed LAN endpoint is unauthenticated and unencrypted. Host isolation and
future network segmentation limit exposure; this work must not pretend HTTP
provides device identity or confidentiality.

## 3. Proposed runtime identity

Use the shared credentialless read-only telemetry identity
`solardt-telemetry`, with a same-named primary group. This follows
`SECURITY_MODEL.md`: classify identity by maximum effective authority, and
allow sharing only among technically read-only telemetry sources. The ESP32
SSE interface currently exposes passive telemetry without a credential or
control path, so an ESP32-only identity would add administration without
meaningful isolation.

The future account must be a system account with `/usr/sbin/nologin`, no home,
no sudo, no credential directory, no repository write access, no access to
unrelated protected runtimes, and only read/execute access to installed code.
It may write only its narrowly scoped ESP32 state/evidence directory and
contact the fixed IPv4 SSE endpoint.

For practical trusted analysis, the initial reporting operator `chris` may be
a member of the telemetry group. Directory mode `0750` and file mode `0640`
then give group read/traverse without group write. Any future reporting service
identity must be separately reviewed before group membership. The installation
phase must verify the identity has no supplementary group or protected-resource
access beyond the exact approved design.

Do not implement any identity in the repository phase.

## 4. Proposed installed paths and ownership

| Purpose | Proposed path | Owner:group | Mode |
|---|---|---|---:|
| Installed tracked application | `/opt/solar-digital-twin` | `root:root` | directories `0755`; files normally `0644`; executables `0755` |
| Shared state parent | `/var/lib/solar-digital-twin` | administrator-managed | existing verified metadata must be preserved |
| ESP32 state root | `/var/lib/solar-digital-twin/esp32` | `solardt-telemetry:solardt-telemetry` | `0750` |
| ESP32 evidence | `/var/lib/solar-digital-twin/esp32/evidence` | `solardt-telemetry:solardt-telemetry` | `0750` |
| Capture files | beneath evidence directory only | `solardt-telemetry:solardt-telemetry` | `0640` under `UMask=0027` |

No ESP32 secret or credential path is needed. Routine service diagnostics go to
the systemd journal under a payload-free policy; raw telemetry never goes to
the journal. Installed code remains administrator-owned and read-only to the
service identity. The installer must refuse symlinks, unexpected file types,
owners, groups, or modes rather than recursively taking ownership of unknown
material.

## 5. HTTP/SSE client hardening

Future repository implementation must:

1. construct a dedicated Requests session with `trust_env = False`;
2. send GET with `allow_redirects=False`, streaming enabled, fixed connect/read
   timeouts, the existing `Accept` header, and the fixed IPv4 URL;
3. treat every 3xx response as a permanent destination-policy failure without
   following `Location`;
4. stop on permanent 4xx rejection; treat only selected 5xx responses and
   transport timeouts/connection failures as transient; treat `429` as
   transient only with a locally capped delay, never an unbounded server value;
5. validate `Content-Type` as `text/event-stream` case-insensitively, allowing
   documented parameters such as `charset`; runtime verification must confirm
   the device's actual compatible value before persistent operation;
6. enforce an application-level maximum decoded SSE data line/event size. Use
   a conservative initial ceiling of 1 MiB unless focused fixture review
   supports a smaller value; reject over-limit input before JSON parsing and
   record only the fixed failure category;
7. preserve the existing UTC receipt timestamp at acceptance, exact allowlist,
   record fields, raw ordering, policy state across reconnects, and 1-to-30
   second capped exponential reconnect delays;
8. require explicit finite duration in the dormant service invocation. Manual
   foreground use may retain current CLI compatibility, but persistent
   unlimited retry/collection is not authorized by repository implementation;
9. close every response through a context manager or explicit `finally` path on
   success, rejection, timeout, stream end, and interruption;
10. log fixed categories, HTTP status where safe, exception type, and retry
    delay only—never response bodies, SSE lines, headers, proxy environment,
    record values, or credentials; and
11. stop safely on policy violations without sending another request, invoking
    a service, or changing device state.

Do not overconstrain harmless SSE formatting. Preserve current acceptance of
blank/non-`data:` lines and non-object/unapproved events. If multiline SSE data
is proposed, first prove the device behavior and preserve existing evidence
semantics with fixtures.

## 6. Evidence and file-safety requirements

Preserve the already implemented safeguards:

- check every selected manifest/raw/retained path before network contact;
- create every new file exclusively and refuse collisions;
- write and flush authoritative raw before evaluating derived policies;
- isolate open, process, write, flush, and close failure per retained output;
- stop collection on raw write/flush failure;
- append start and terminal manifest records, including retained disablement;
- preserve partial runs and never rewrite evidence in place;
- never delete evidence automatically or write capture files into tracked
  repository paths; and
- keep `esp32-frequency-v1` as the default, with conservative/canary modes
  remaining explicit opt-ins.

Implementation must add deterministic file mode tests under `UMask=0027` or an
equivalent explicit open/chmod design. Before any long capture, the runtime
phase must estimate worst-case raw plus derived growth from prior captures,
check available bytes/inodes against a documented reserve, set a finite
duration, and refuse an unsafe start. Disk-capacity preflight must not delete or
compress prior evidence.

If manifest creation fails, do not open raw or contact the device. If raw open
or write fails, stop. If terminal-manifest finalization fails, preserve all
files and emit a fixed diagnostic; never relabel the run as complete elsewhere.

## 7. Dormant service design

Plan one future systemd service, with no timer, installed disabled and inactive.
Installation must not start or enable it. Repository tests must assert the unit
has no `[Install]` activation target unless a later persistent-operation work
unit intentionally adds one.

Prospective compatible settings:

- `User=solardt-telemetry`, `Group=solardt-telemetry`, `UMask=0027`;
- administrator-owned working/runtime directory;
- an explicit finite collector duration and explicit ESP32 evidence directory;
- `NoNewPrivileges=true`, `PrivateTmp=true`, `ProtectHome=true`, and
  `ProtectSystem=strict`;
- `ReadWritePaths=/var/lib/solar-digital-twin/esp32` only;
- `RestrictAddressFamilies=AF_INET AF_UNIX` if verified compatible;
- bounded `TasksMax`, `LimitNOFILE`, memory, and runtime duration values sized
  from focused tests and prior evidence, not arbitrary tiny limits;
- no credential/environment file, shell command, device-control capability, or
  writable installed code; and
- `Restart=no` for dormant installation and passive verification.

Do not copy hardening directives blindly. Repository tests and the passive
phase must prove Python imports, journal output, fixed IPv4 access, and evidence
writing remain possible. DNS is unnecessary for the fixed endpoint.

## 8. Installer and verification design

Create a future administrator-operated installer modeled on the useful
SolarAssistant patterns but specific to credentialless telemetry:

- `--check`: nonprivileged validation of tracked inputs, unit semantics,
  expected paths/modes, clean-source expectations, credential absence, and
  explicit statement that nothing was installed or contacted;
- no argument (or an explicit `--install` if chosen consistently): create or
  verify the account/group and directories, deploy only tracked content from a
  clean approved commit, install the dormant unit, run daemon reload if
  required, and explicitly leave it disabled/inactive; and
- `--verify`: metadata/access checks only—identity, groups, paths, modes,
  symlink/file-type refusal, installed commit/files, unit disabled/inactive,
  no timer, installed code non-writable, evidence path writable by the service
  and readable but not writable by the trusted reporting operator.

The installer must be idempotent for exact expected state, refuse unexpected
ownership or file types, handle no credentials, preserve prior installed code
through timestamped archive/rollback, never delete existing evidence, and print
compact operator-facing results. It must install only from a clean approved
repository checkpoint and verify an identity-bound tracked-file manifest or
commit marker.

Rollback removes or disables only newly installed runtime metadata after
preserving evidence and restores the archived prior runtime where applicable.
Any removal remains a separately reviewed administrator action.

## 9. Completed repository implementation work unit

The completed repository-only unit changed:

- `src/solar_digital_twin/collectors/esp32_sse.py`;
- `tests/test_esp32_sse.py` and new `tests/test_esp32_runtime.py`;
- new `scripts/install_esp32_runtime.sh`;
- new `scripts/run_esp32_forensic_collector.sh`;
- new `systemd/esp32-forensic-collector.service`;
- this plan and directly related ESP32/security/runtime documentation;
- `PROJECT_STATE.md`, `NEXT_TASK.md`, `PROJECT_INDEX.md`; and
- one appended `CHANGE_AUDIT.md` entry.

Implementation acceptance included local source inspection before changes,
focused tests for every confirmed HTTP gap, unchanged default-policy/record
semantics, full repository tests, repository health, exact staged scope, and
all canonical publication safeguards.

Explicit exclusions are installation, package installation on the host,
identity or directory creation, service daemon reload/start/enable, live device
contact, capture, firmware/ESPHome changes, network changes, credentials,
database work, portal work, evidence changes, and retention-policy promotion.

## 10. Separately approved runtime phases

### Installation — complete

The administrator-operated check, legacy-runtime inspection, archive-first
installation, and metadata-only verification passed. The unit remained static
and inactive and no device was contacted.

### Passive verification — complete

The separately authorized header probe and exact one-hour installed service run
passed fixed-destination, status/content-type, output, allowlist, timestamp,
raw/current-retained, manifest, clean-stop, payload-free log, credentialless,
and dormant-state gates. The resulting evidence is preserved.

### Persistent or long capture

Only owner review after passive verification may select persistent service or a
long capture. That decision must consider storage/inodes, monitoring,
finite-duration behavior, restart policy, evidence retention, duplicate Home
Assistant ingestion, and the diagnostic value of additional collection. No
automatic timer or indefinite restart loop is implied.

## 11. Acceptance gates

### Repository source and tests

- Every confirmed HTTP gap has a focused failing-before/passing-after test.
- Redirects are rejected; proxy environment is ignored; content type and line
  size are enforced; permanent/transient failures differ; responses close.
- Existing allowlist, record schema, UTC receipt timestamp, manifest, raw-first
  ordering, retained isolation, reconnect policy state, exclusive creation,
  and default `esp32-frequency-v1` tests remain green.
- Diagnostics contain no payload or private exception text.

### Installation artifacts

- Installer modes are idempotent and refuse dirty/unexpected/symlink state.
- Installed content is tied to the approved clean commit.
- No credential path is created.
- The unit installs disabled/inactive with no timer and no automatic contact.

### Ownership and access

- Identity is no-login, no-home, no-sudo, and has only its expected group.
- Installed code is administrator-owned and non-writable by the service.
- Service writes only the ESP32 state/evidence tree with directories `0750`
  and files `0640` under restrictive umask.
- Trusted reporting can read evidence without gaining write access or
  unrelated protected access.

### Passive collection

- The actual endpoint returns an accepted SSE content type without redirect or
  proxy use.
- A short finite run records only approved IDs with expected receipt/provenance
  fields and clean manifest closure.
- Raw precedes unchanged retained copies; interruption and failure preserve the
  partial run; logs remain payload-free.

### Recovery and boundaries

- Rollback is documented and tested where safely possible with temporary
  fixtures.
- Prior evidence is never modified or deleted.
- No runtime phase begins from an uncommitted or unreviewed implementation.
- No gate crosses installation, device, firmware, network, credential,
  database, evidence, service-activation, or persistent-operation authority
  without its separate approval.

## 12. Recovery

### Repository implementation

Correct in-scope defects before publication. After publication, use a normal
revert commit if needed; never reset or rewrite history. Raw evidence and the
current deployed runtime remain untouched.

### Failed installation

Leave the service disabled/inactive, preserve existing evidence and any prior
runtime archive, report exact partial state, and restore the verified prior
runtime through a separately approved administrator action. Do not recursively
change unknown ownership or delete directories for convenience.

### Failed passive verification

Stop the finite collector, preserve and inventory every partial output and
manifest, keep the service disabled, and return to repository diagnosis. Do not
retry permanent rejection, weaken validation, change the device, or discard the
failed evidence.

### Service-unit defect

Keep or return the unit to inactive/disabled, capture metadata-only diagnostics,
correct the repository unit/tests, publish normally, and reinstall only under a
new bounded runtime authorization.

### Evidence-writer defect

Stop when authoritative raw writing fails. Preserve the partial raw, manifest,
and derived files. A retained-only failure remains manifested and isolated;
do not rewrite the raw file or silently claim complete derived output. Repair
and validate from synthetic fixtures before any later passive run.

## Remaining decisions and uncertainties

- The 1 MiB input ceiling remains deliberately conservative; the passive run
  validated ordinary device events but did not exercise near-limit input.
- The one-hour run measured normal resource behavior, but any future persistent
  limits still require owner review and appropriate headroom.
- Any future shared telemetry source must be reclassified by maximum effective
  authority before joining `solardt-telemetry`.
