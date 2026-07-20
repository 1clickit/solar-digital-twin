"""Read-only collector for approved ESPHome SSE telemetry."""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from email.message import Message
from pathlib import Path
from typing import Any, BinaryIO, Iterator, TextIO

import requests

from solar_digital_twin.collectors.esp32_retention import (
    CONSERVATIVE_POLICY_ID,
    CURRENT_POLICY_ID,
    ConservativeESP32RetentionPolicy,
    CurrentESP32RetentionPolicy,
)

SSE_URL = "http://192.168.3.13/events"
MAX_BACKOFF_SECONDS = 30.0
MAX_RETRY_AFTER_SECONDS = 30.0
MAX_SSE_LINE_BYTES = 1024 * 1024
STREAM_CHUNK_BYTES = 8192
HTTP_TIMEOUT = (3.0, 30.0)
RETRYABLE_HTTP_STATUSES = frozenset({429, 500, 502, 503, 504})
MANIFEST_SCHEMA = "solar-digital-twin.esp32-capture.v1"
RETENTION_MODES = ("current", "canary", "conservative")
DEFAULT_OUTPUT_DIR = Path("evidence/esp32")

APPROVED_IDS = {
    "binary_sensor-03_gen_frequency_high",
    "binary_sensor-03_gen_frequency_low",
    "binary_sensor-03_large_power_drop_active",
    "binary_sensor-03_large_power_rise_active",
    "sensor-01_estimated_total_ac-coupled_power",
    "sensor-01_estimated_active_microinverters",
    "sensor-01_estimated_curtailment_percent",
    "sensor-01_gen_frequency",
    "sensor-01_gen_l1_current",
    "sensor-01_estimated_gen_l1-l2_voltage",
    "sensor-01_estimated_total_ac-coupled_energy",
    "sensor-02_power_ramp_rate",
    "sensor-02_frequency_ramp_rate",
    "sensor-02_largest_power_drop_since_reset",
    "sensor-02_total_events_since_reset",
    "text_sensor-00_current_status",
    "text_sensor-04_forensic_event_log",
}


class PermanentSSEError(Exception):
    """A destination, response, or stream policy failure that must not retry."""


class TransientSSEError(Exception):
    """A transport or selected HTTP failure that may retry."""

    def __init__(self, category: str, retry_after: float | None = None) -> None:
        super().__init__(category)
        self.category = category
        self.retry_after = retry_after


def receipt_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def new_output_path(output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    return output_dir / f"esp32_sse_{stamp}.ndjson"


def retained_output_path(raw_output: Path) -> Path:
    return raw_output.with_name(f"{raw_output.stem}_retained.ndjson")


def conservative_output_path(raw_output: Path) -> Path:
    return raw_output.with_name(
        f"{raw_output.stem}_retained_{CONSERVATIVE_POLICY_ID}.ndjson"
    )


def manifest_output_path(raw_output: Path) -> Path:
    return raw_output.with_name(f"{raw_output.stem}_manifest.ndjson")


def _json_line(payload: dict[str, Any]) -> str:
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n"


def _open_exclusive_text(path: Path) -> TextIO:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o640)
    try:
        os.fchmod(descriptor, 0o640)
        return os.fdopen(descriptor, "w", encoding="utf-8", buffering=1)
    except BaseException:
        os.close(descriptor)
        raise


def _ensure_output_directory(path: Path) -> None:
    existed = path.exists()
    path.mkdir(parents=True, exist_ok=True, mode=0o750)
    if not existed:
        path.chmod(0o750)


def _new_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    return session


def _retry_after_seconds(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        parsed = float(value.strip())
    except (TypeError, ValueError):
        return None
    if not 0 <= parsed < float("inf"):
        return None
    return min(parsed, MAX_RETRY_AFTER_SECONDS)


def _validate_response(response: requests.Response) -> None:
    status = response.status_code
    if status == 200:
        pass
    elif status in RETRYABLE_HTTP_STATUSES:
        retry_after = (
            _retry_after_seconds(response.headers.get("Retry-After"))
            if status == 429
            else None
        )
        raise TransientSSEError(f"http_{status}", retry_after)
    elif 300 <= status <= 399:
        raise PermanentSSEError("redirect_rejected")
    elif 400 <= status <= 499:
        raise PermanentSSEError("http_rejected")
    else:
        raise PermanentSSEError("http_status_rejected")

    content_type = response.headers.get("Content-Type")
    if not content_type:
        raise PermanentSSEError("content_type_rejected")
    message = Message()
    message["content-type"] = content_type
    if message.get_content_type().lower() != "text/event-stream":
        raise PermanentSSEError("content_type_rejected")


def _iter_bounded_lines(
    raw: BinaryIO,
    *,
    max_line_bytes: int = MAX_SSE_LINE_BYTES,
    chunk_bytes: int = STREAM_CHUNK_BYTES,
) -> Iterator[str]:
    """Yield UTF-8 SSE lines without ever accumulating an unbounded line."""
    pending = bytearray()
    for chunk in raw.stream(chunk_bytes, decode_content=True):
        if not chunk:
            continue
        view = memoryview(chunk)
        while view:
            newline = bytes(view).find(b"\n")
            if newline < 0:
                if len(pending) + len(view) > max_line_bytes:
                    raise PermanentSSEError("input_limit_exceeded")
                pending.extend(view)
                break
            segment = view[:newline]
            if len(pending) + len(segment) > max_line_bytes:
                raise PermanentSSEError("input_limit_exceeded")
            pending.extend(segment)
            if pending.endswith(b"\r"):
                pending.pop()
            try:
                yield pending.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise PermanentSSEError("stream_encoding_rejected") from exc
            pending.clear()
            view = view[newline + 1 :]
    if pending:
        if pending.endswith(b"\r"):
            pending.pop()
        try:
            yield pending.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise PermanentSSEError("stream_encoding_rejected") from exc


@dataclass
class RetainedOutput:
    """One independently stateful and independently disableable output."""

    label: str
    path: Path
    policy: Any
    handle: TextIO | None = None
    written: int = 0
    error_type: str | None = None

    @property
    def policy_id(self) -> str:
        return self.policy.policy_id

    def disable(self, exc: Exception) -> None:
        if self.error_type is not None:
            return
        self.error_type = type(exc).__name__
        print(
            f"{self.label} ESP32 output disabled after {self.error_type}. "
            "Raw collection continues."
        )
        if self.handle is not None:
            try:
                self.handle.close()
            except Exception:
                pass
            self.handle = None

    def process(
        self, record: dict[str, Any], encoded_record: str, monotonic_now: float
    ) -> None:
        if self.handle is None:
            return
        try:
            if self.policy.retention_reason(record, monotonic_now) is None:
                return
            self.handle.write(encoded_record)
            self.handle.flush()
            self.written += 1
        except Exception as exc:
            self.disable(exc)

    def close(self) -> None:
        if self.handle is None:
            return
        try:
            self.handle.close()
        except Exception as exc:
            self.disable(exc)
        else:
            self.handle = None


def _retained_outputs(raw_output: Path, mode: str) -> list[RetainedOutput]:
    outputs: list[RetainedOutput] = []
    if mode in {"current", "canary"}:
        outputs.append(
            RetainedOutput(
                "Retained",
                retained_output_path(raw_output),
                CurrentESP32RetentionPolicy(),
            )
        )
    if mode in {"canary", "conservative"}:
        outputs.append(
            RetainedOutput(
                "Conservative",
                conservative_output_path(raw_output),
                ConservativeESP32RetentionPolicy(),
            )
        )
    return outputs


def _assert_outputs_absent(paths: list[Path]) -> None:
    collision = next((path for path in paths if path.exists()), None)
    if collision is not None:
        raise FileExistsError(f"capture output already exists: {collision.name}")


def _append_manifest(manifest: TextIO, payload: dict[str, Any]) -> None:
    manifest.write(_json_line(payload))
    manifest.flush()


def _finalize_manifest(manifest: TextIO, payload: dict[str, Any]) -> None:
    try:
        _append_manifest(manifest, payload)
    except Exception as exc:
        print(f"Manifest finalization failed after {type(exc).__name__}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--duration",
        type=float,
        default=0,
        help="Stop after N seconds; 0 runs until interrupted.",
    )
    parser.add_argument(
        "--retention-mode",
        choices=RETENTION_MODES,
        default="current",
        help="Select current output, opt-in canary, or future conservative mode.",
    )
    parser.add_argument(
        "--collector-version",
        help="Non-secret implementation commit recorded in capture provenance.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for raw, retained, and manifest capture outputs.",
    )
    args = parser.parse_args()
    if args.retention_mode != "current" and not args.collector_version:
        parser.error("--collector-version is required outside current mode")
    return args


def _manifest_start(
    raw_output: Path,
    retained_outputs: list[RetainedOutput],
    retention_mode: str,
    collector_version: str | None,
) -> dict[str, Any]:
    return {
        "manifest_schema": MANIFEST_SCHEMA,
        "event": "start",
        "capture_id": raw_output.stem,
        "started_at_utc": receipt_timestamp(),
        "collector_version": collector_version or "unspecified",
        "retention_mode": retention_mode,
        "canary": retention_mode == "canary",
        "raw_file": raw_output.name,
        "retained_outputs": [
            {"file": item.path.name, "policy_id": item.policy_id}
            for item in retained_outputs
        ],
    }


def _manifest_stop(
    event: str,
    stop_reason: str,
    raw_records: int,
    retained_outputs: list[RetainedOutput],
) -> dict[str, Any]:
    return {
        "manifest_schema": MANIFEST_SCHEMA,
        "event": event,
        "ended_at_utc": receipt_timestamp(),
        "stop_reason": stop_reason,
        "raw_records": raw_records,
        "retained_outputs": [
            {
                "file": item.path.name,
                "policy_id": item.policy_id,
                "records": item.written,
                "status": "disabled" if item.error_type else "complete",
                "error_type": item.error_type,
            }
            for item in retained_outputs
        ],
    }


def collect(
    duration: float,
    retention_mode: str = "current",
    collector_version: str | None = None,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> tuple[Path, Path, int, int]:
    if retention_mode not in RETENTION_MODES:
        raise ValueError(f"unsupported retention mode: {retention_mode}")
    if retention_mode != "current" and not collector_version:
        raise ValueError("collector_version is required outside current mode")

    output = new_output_path(output_dir)
    retained_output = retained_output_path(output)
    manifest_output = manifest_output_path(output)
    retained_outputs = _retained_outputs(output, retention_mode)
    _ensure_output_directory(output.parent)
    _assert_outputs_absent(
        [output, manifest_output, *(item.path for item in retained_outputs)]
    )

    deadline = time.monotonic() + duration if duration > 0 else None
    backoff = 1.0
    written = 0
    final_event = "completion"
    stop_reason = "duration" if duration > 0 else "stream_stopped"

    print(f"Writing raw approved ESP32 updates to {output.name}")
    for item in retained_outputs:
        print(f"Writing {item.policy_id} ESP32 updates to {item.path.name}")

    with _open_exclusive_text(manifest_output) as manifest:
        _append_manifest(
            manifest,
            _manifest_start(
                output, retained_outputs, retention_mode, collector_version
            ),
        )
        try:
            with _open_exclusive_text(output) as evidence:
                for item in retained_outputs:
                    try:
                        item.handle = _open_exclusive_text(item.path)
                    except Exception as exc:
                        item.disable(exc)

                session = _new_session()
                try:
                    while deadline is None or time.monotonic() < deadline:
                        response = None
                        try:
                            response = session.get(
                                SSE_URL,
                                headers={"Accept": "text/event-stream"},
                                stream=True,
                                timeout=HTTP_TIMEOUT,
                                allow_redirects=False,
                            )
                            _validate_response(response)
                            backoff = 1.0

                            for line in _iter_bounded_lines(response.raw):
                                if (
                                    deadline is not None
                                    and time.monotonic() >= deadline
                                ):
                                    return (
                                        output,
                                        retained_output,
                                        written,
                                        next(
                                            (
                                                item.written
                                                for item in retained_outputs
                                                if item.policy_id == CURRENT_POLICY_ID
                                            ),
                                            0,
                                        ),
                                    )
                                if not line or not line.startswith("data:"):
                                    continue

                                try:
                                    incoming = json.loads(line[5:].strip())
                                except json.JSONDecodeError:
                                    continue
                                if not isinstance(incoming, dict):
                                    continue
                                if incoming.get("id") not in APPROVED_IDS:
                                    continue

                                record = {
                                    "received_at_utc": receipt_timestamp(),
                                    "source_url": SSE_URL,
                                    "id": incoming.get("id"),
                                    "name": incoming.get("name"),
                                    "domain": incoming.get("domain"),
                                    "value": incoming.get("value"),
                                    "state": incoming.get("state"),
                                }
                                encoded_record = _json_line(record)
                                evidence.write(encoded_record)
                                evidence.flush()
                                written += 1

                                monotonic_now = time.monotonic()
                                for item in retained_outputs:
                                    item.process(
                                        record, encoded_record, monotonic_now
                                    )

                            raise TransientSSEError("stream_ended")

                        except PermanentSSEError as exc:
                            print(f"SSE stopped: {exc}.")
                            raise
                        except (requests.RequestException, TransientSSEError) as exc:
                            category = (
                                exc.category
                                if isinstance(exc, TransientSSEError)
                                else type(exc).__name__
                            )
                            requested_delay = (
                                exc.retry_after
                                if isinstance(exc, TransientSSEError)
                                else None
                            )
                            remaining = (
                                None
                                if deadline is None
                                else deadline - time.monotonic()
                            )
                            if remaining is not None and remaining <= 0:
                                break
                            base_delay = (
                                backoff
                                if requested_delay is None
                                else min(
                                    max(backoff, requested_delay),
                                    MAX_RETRY_AFTER_SECONDS,
                                )
                            )
                            delay = (
                                base_delay
                                if remaining is None
                                else min(base_delay, remaining)
                            )
                            print(
                                f"SSE transient failure ({category}); "
                                f"retrying in {delay:.0f}s"
                            )
                            time.sleep(delay)
                            backoff = min(backoff * 2, MAX_BACKOFF_SECONDS)
                        finally:
                            if response is not None:
                                response.close()
                finally:
                    session.close()
                    for item in retained_outputs:
                        item.close()
        except KeyboardInterrupt:
            final_event = "interruption"
            stop_reason = "keyboard_interrupt"
            raise
        except BaseException as exc:
            final_event = "failure"
            stop_reason = type(exc).__name__
            raise
        finally:
            if final_event == "completion" and any(
                item.error_type for item in retained_outputs
            ):
                final_event = "retained_output_failure"
                stop_reason = "retained_output_disabled"
            _finalize_manifest(
                manifest,
                _manifest_stop(
                    final_event, stop_reason, written, retained_outputs
                ),
            )

    retained_written = next(
        (
            item.written
            for item in retained_outputs
            if item.policy_id == CURRENT_POLICY_ID
        ),
        0,
    )
    return output, retained_output, written, retained_written


def main() -> None:
    args = parse_args()
    try:
        output, retained_output, written, retained_written = collect(
            args.duration,
            retention_mode=args.retention_mode,
            collector_version=args.collector_version,
            output_dir=args.output_dir,
        )
    except KeyboardInterrupt:
        print("\nStopped cleanly by user.")
    else:
        print(
            f"Stopped cleanly after writing {written} "
            f"raw records to {output.name} and {retained_written} "
            f"records to {retained_output.name}."
        )


if __name__ == "__main__":
    main()
