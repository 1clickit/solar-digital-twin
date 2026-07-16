# Next Task

## Objective

Make SolarAssistant HTTP authentication failures stop automated retries and
guarantee response closure, with focused offline tests and unchanged raw evidence.

## Context

The project-wide Home Assistant-style security model is approved. SolarAssistant
uses a separate runtime identity until the `admin` credential's effective
authority is confirmed. No SolarAssistant credential is installed, and exact
credential implementation remains deferred. The existing standalone collector
and raw NDJSON behavior were manually verified previously.

## Scope

- Harden only the existing standalone SolarAssistant collector's HTTP failure handling.
- Preserve its current raw NDJSON filename, record format, allowlist, receipt timestamps, and flushing.
- Treat HTTP `401` and `403` as authentication failures that stop automated attempts and require operator correction.
- Keep temporary network failures distinct and preserve limited controlled backoff.
- Close every HTTP response on success and failure paths.
- Add focused tests requiring no device, credential, network, or existing evidence.
- Keep credential storage, live authentication, portal, SQLite, and systemd integration deferred.

## Boundaries

- Keep the work bounded, standalone, and reviewable.
- Do not implement credential storage, install credentials, enter passwords,
  contact SolarAssistant, or perform authenticated collector work.
- Preserve current polling, backoff, duration, and interruption behavior unless
  the bounded change explicitly requires and tests an adjustment.
- HTTP `401` or `403` must stop automated authentication attempts; temporary
  network failures remain distinct and may use limited controlled backoff.
- Do not alter device configuration or expand the approved security model.

## Success

Authentication rejection stops without retrying, temporary failures retain
bounded backoff, every response closes, raw evidence remains intact, and no
credential, live-device, or deferred integration boundary is crossed.
