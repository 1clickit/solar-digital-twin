"""Read-only collector for approved ESPHome SSE telemetry."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from solar_digital_twin.collectors.retention import FrequencyRetentionPolicy


SSE_URL = "http://192.168.3.13/events"
MAX_BACKOFF_SECONDS = 30.0
FREQUENCY_ID = "sensor-01_gen_frequency"

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


def receipt_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def new_output_path() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    return Path("evidence/esp32") / f"esp32_sse_{stamp}.ndjson"


def retained_output_path(raw_output: Path) -> Path:
    return raw_output.with_name(f"{raw_output.stem}_retained.ndjson")


def should_retain_record(
    record: dict[str, object],
    frequency_policy: FrequencyRetentionPolicy,
    monotonic_now: float,
) -> bool:
    """Apply selective retention without changing the raw record."""
    if record.get("id") != FREQUENCY_ID:
        return True
    return frequency_policy.should_retain(record.get("value"), monotonic_now)


def disable_retained_output(retained: object | None, exc: Exception) -> None:
    """Report one retained-stage failure and close its output if open."""
    print(
        "Retained ESP32 output disabled after "
        f"{type(exc).__name__}. Raw collection continues."
    )
    if retained is not None:
        try:
            retained.close()
        except Exception:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--duration",
        type=float,
        default=0,
        help="Stop after N seconds; 0 runs until interrupted.",
    )
    return parser.parse_args()


def collect(duration: float) -> tuple[Path, Path, int, int]:
    output = new_output_path()
    retained_output = retained_output_path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + duration if duration > 0 else None
    backoff = 1.0
    written = 0
    retained_written = 0
    frequency_policy = FrequencyRetentionPolicy()

    print(f"Writing raw approved ESP32 updates to {output}")
    print(f"Writing retained ESP32 updates to {retained_output}")

    with output.open("a", encoding="utf-8", buffering=1) as evidence:
        retained = None
        try:
            retained = retained_output.open(
                "a", encoding="utf-8", buffering=1
            )
        except Exception as exc:
            disable_retained_output(retained, exc)

        try:
            while deadline is None or time.monotonic() < deadline:
                try:
                    response = requests.get(
                        SSE_URL,
                        headers={"Accept": "text/event-stream"},
                        stream=True,
                        timeout=(3, 30),
                    )
                    response.raise_for_status()
                    backoff = 1.0

                    for line in response.iter_lines(
                        chunk_size=1,
                        decode_unicode=True,
                    ):
                        if deadline is not None and time.monotonic() >= deadline:
                            response.close()
                            return output, retained_output, written, retained_written
                        if not line or not line.startswith("data:"):
                            continue

                        try:
                            event = json.loads(line[5:].strip())
                        except json.JSONDecodeError:
                            continue

                        if not isinstance(event, dict):
                            continue
                        if event.get("id") not in APPROVED_IDS:
                            continue

                        record = {
                            "received_at_utc": receipt_timestamp(),
                            "source_url": SSE_URL,
                            "id": event.get("id"),
                            "name": event.get("name"),
                            "domain": event.get("domain"),
                            "value": event.get("value"),
                            "state": event.get("state"),
                        }

                        encoded_record = json.dumps(
                            record,
                            separators=(",", ":"),
                            ensure_ascii=False,
                        ) + "\n"
                        evidence.write(encoded_record)
                        evidence.flush()
                        written += 1

                        if retained is not None:
                            try:
                                if should_retain_record(
                                    record,
                                    frequency_policy,
                                    time.monotonic(),
                                ):
                                    retained.write(encoded_record)
                                    retained.flush()
                                    retained_written += 1
                            except Exception as exc:
                                disable_retained_output(retained, exc)
                                retained = None

                    response.close()
                    raise requests.ConnectionError("SSE stream ended")

                except requests.RequestException as exc:
                    if "response" in locals():
                        response.close()

                    remaining = (
                        None
                        if deadline is None
                        else deadline - time.monotonic()
                    )
                    if remaining is not None and remaining <= 0:
                        break

                    delay = backoff if remaining is None else min(backoff, remaining)
                    print(f"SSE connection error: {exc}; retrying in {delay:.0f}s")
                    time.sleep(delay)
                    backoff = min(backoff * 2, MAX_BACKOFF_SECONDS)
        finally:
            if retained is not None:
                try:
                    retained.close()
                except Exception as exc:
                    disable_retained_output(None, exc)

    return output, retained_output, written, retained_written


def main() -> None:
    args = parse_args()

    try:
        output, retained_output, written, retained_written = collect(args.duration)
    except KeyboardInterrupt:
        print("\nStopped cleanly by user.")
    else:
        print(
            f"Stopped cleanly after writing {written} "
            f"raw records to {output} and {retained_written} "
            f"records to {retained_output}."
        )


if __name__ == "__main__":
    main()
