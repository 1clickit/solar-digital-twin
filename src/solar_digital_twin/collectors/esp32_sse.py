"""Read-only collector for approved ESPHome SSE telemetry."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


SSE_URL = "http://192.168.3.13/events"
MAX_BACKOFF_SECONDS = 30.0

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--duration",
        type=float,
        default=0,
        help="Stop after N seconds; 0 runs until interrupted.",
    )
    return parser.parse_args()


def collect(duration: float) -> tuple[Path, int]:
    output = new_output_path()
    output.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + duration if duration > 0 else None
    backoff = 1.0
    written = 0

    print(f"Writing approved ESP32 updates to {output}")

    with output.open("a", encoding="utf-8", buffering=1) as evidence:
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
                        return output, written
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

                    evidence.write(
                        json.dumps(
                            record,
                            separators=(",", ":"),
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                    evidence.flush()
                    written += 1

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

    return output, written


def main() -> None:
    args = parse_args()

    try:
        output, written = collect(args.duration)
    except KeyboardInterrupt:
        print("\nStopped cleanly by user.")
    else:
        print(
            f"Stopped cleanly after writing {written} "
            f"records to {output}."
        )


if __name__ == "__main__":
    main()
