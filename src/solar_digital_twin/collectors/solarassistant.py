"""Read-only collector for approved SolarAssistant battery telemetry."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from solar_digital_twin.collectors.solarassistant_retention import (
    SolarAssistantRetentionPolicy,
)


METRICS_URL = "http://192.168.3.12/api/v1/metrics"
USERNAME = "admin"
MAX_BACKOFF_SECONDS = 30.0
DEFAULT_OUTPUT_DIR = Path("evidence/solarassistant")


class AuthenticationRejected(Exception):
    """SolarAssistant rejected the supplied credential."""


class CredentialLoadError(Exception):
    """The local SolarAssistant credential could not be loaded safely."""

COMBINED_TOPICS = {
    "total/battery_state_of_charge",
    "total/battery_voltage",
    "total/battery_current",
    "total/battery_power",
    "total/battery_temperature",
    "total/battery_state_of_health",
    "total/battery_cell_voltage_-_average",
    "total/battery_cell_voltage_-_highest",
    "total/battery_cell_voltage_-_lowest",
    "total/battery_cell_imbalance_-_average",
}

INDIVIDUAL_SUFFIXES = {
    "state_of_charge",
    "voltage",
    "current",
    "power",
    "state_of_health",
    "capacity",
    "charge_capacity",
    "cycles",
    "cell_voltage_-_average",
    "cell_voltage_-_highest",
    "cell_voltage_-_lowest",
    "cell_voltage_-_imbalance",
    "temperature",
    "temperature_1",
    "temperature_2",
    "temperature_mos",
}


def approved_topic(topic: str) -> bool:
    if topic in COMBINED_TOPICS:
        return True

    for prefix in ("battery_1/", "battery_2/"):
        if topic.startswith(prefix):
            return topic[len(prefix):] in INDIVIDUAL_SUFFIXES

    return False


def receipt_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def new_output_path(output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    return output_dir / f"solarassistant_{stamp}.ndjson"


def retained_output_path(raw_output: Path) -> Path:
    return raw_output.with_name(f"{raw_output.stem}_retained{raw_output.suffix}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--duration",
        type=float,
        default=0,
        help="Stop after N seconds; 0 runs until interrupted.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds between successful polls; minimum 1 second.",
    )
    parser.add_argument(
        "--password-file",
        type=Path,
        help="Read the password from this protected file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for raw and retained NDJSON evidence.",
    )
    return parser.parse_args()


def _strip_trailing_line_ending(value: str) -> str:
    if value.endswith("\r\n"):
        return value[:-2]
    if value.endswith(("\n", "\r")):
        return value[:-1]
    return value


def get_password(password_file: Path | None = None) -> str:
    if password_file is not None:
        try:
            password = _strip_trailing_line_ending(
                password_file.read_bytes().decode("utf-8")
            )
        except (OSError, UnicodeError) as exc:
            raise CredentialLoadError from exc
        if not password or not password.strip():
            raise CredentialLoadError
        return password

    password = os.environ.get("SOLARASSISTANT_PASSWORD")
    if password:
        return password
    return getpass.getpass("SolarAssistant password: ")


def collect(
    duration: float,
    interval: float,
    password: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> tuple[Path, int]:
    if interval < 1.0:
        raise ValueError("--interval must be at least 1 second")

    output = new_output_path(output_dir)
    retained_output = retained_output_path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    deadline = time.monotonic() + duration if duration > 0 else None
    session = requests.Session()
    backoff = 1.0
    written = 0
    retention = SolarAssistantRetentionPolicy()

    print(f"Writing approved SolarAssistant updates to {output}")
    print(f"Writing retained SolarAssistant updates to {retained_output}")

    with (
        output.open("a", encoding="utf-8", buffering=1) as evidence,
        retained_output.open("a", encoding="utf-8", buffering=1) as retained,
    ):
        while deadline is None or time.monotonic() < deadline:
            try:
                response = session.get(
                    METRICS_URL,
                    auth=(USERNAME, password),
                    timeout=(3, 10),
                )
                try:
                    if response.status_code in (401, 403):
                        raise AuthenticationRejected

                    response.raise_for_status()

                    rows = response.json()
                    if not isinstance(rows, list):
                        raise ValueError("Metrics response is not a list")

                    received_at_utc = receipt_timestamp()
                    backoff = 1.0

                    for row in rows:
                        if not isinstance(row, dict):
                            continue

                        topic = row.get("topic")
                        if not isinstance(topic, str) or not approved_topic(topic):
                            continue

                        record = {
                            "received_at_utc": received_at_utc,
                            "source_url": METRICS_URL,
                            "topic": topic,
                            "device": row.get("device"),
                            "number": row.get("number"),
                            "group": row.get("group"),
                            "name": row.get("name"),
                            "value": row.get("value"),
                            "unit": row.get("unit"),
                        }

                        evidence.write(
                            json.dumps(record, separators=(",", ":"), ensure_ascii=False)
                            + "\n"
                        )
                        evidence.flush()
                        written += 1

                        reason = retention.retention_reason(
                            record,
                            time.monotonic(),
                        )
                        if reason is not None:
                            retained_record = dict(record)
                            retained_record["retention_reason"] = reason
                            retained.write(
                                json.dumps(
                                    retained_record,
                                    separators=(",", ":"),
                                    ensure_ascii=False,
                                )
                                + "\n"
                            )
                            retained.flush()
                finally:
                    response.close()

                remaining = (
                    None
                    if deadline is None
                    else deadline - time.monotonic()
                )
                if remaining is not None and remaining <= 0:
                    break

                delay = interval if remaining is None else min(interval, remaining)
                time.sleep(delay)

            except (requests.RequestException, ValueError) as exc:
                remaining = (
                    None
                    if deadline is None
                    else deadline - time.monotonic()
                )
                if remaining is not None and remaining <= 0:
                    break

                delay = backoff if remaining is None else min(backoff, remaining)
                print(f"SolarAssistant error: {exc}; retrying in {delay:.0f}s")
                time.sleep(delay)
                backoff = min(backoff * 2, MAX_BACKOFF_SECONDS)

    return output, written


def main() -> None:
    args = parse_args()

    try:
        password = get_password(args.password_file)
        output, written = collect(
            duration=args.duration,
            interval=args.interval,
            password=password,
            output_dir=args.output_dir,
        )
    except KeyboardInterrupt:
        print("\nStopped cleanly by user.")
    except AuthenticationRejected:
        print(
            "SolarAssistant authentication failed; correct the credential "
            "before running the collector again."
        )
        raise SystemExit(1) from None
    except CredentialLoadError:
        print(
            "SolarAssistant credential file could not be read or is empty; "
            "correct it before running the collector again."
        )
        raise SystemExit(1) from None
    except OSError:
        print(
            "SolarAssistant evidence directory or output file could not be "
            "prepared; correct the local path before running again."
        )
        raise SystemExit(1) from None
    else:
        print(
            f"Stopped cleanly after writing {written} "
            f"records to {output}."
        )


if __name__ == "__main__":
    main()
