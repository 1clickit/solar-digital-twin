"""Offline, read-only adapters for forensic-correlation input records."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from solar_digital_twin.analysis.forensic_correlation import (
    TimedRecord,
    normalize_timestamp,
)

UTC = timezone.utc
CENTRAL = "America/Chicago"
APPROVED_ESP32_IDS = frozenset(
    {
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
)

DAY_COLUMNS = {
    "serial_num",
    "sample_time",
    "solar_pv_w",
    "grid_power_w",
    "battery_discharging_w",
    "consumption_w",
    "soc",
    "ac_couple_power_w",
}
RUNTIME_COLUMNS = {
    "serial_num",
    "server_time",
    "status_text",
    "soc",
    "v_bat",
    "grid_freq_hz",
    "eps_freq_hz",
    "consumption_power_w",
    "ac_couple_power_w",
    "raw_json",
    "captured_at",
}


class AdapterError(ValueError):
    """A bounded, payload-free adapter diagnostic."""


def _utc_bound(value: datetime, name: str) -> datetime:
    if value.tzinfo is None:
        raise AdapterError(f"{name} must include an explicit timezone")
    return value.astimezone(UTC)


def _in_window(timestamp: datetime, start: datetime, end: datetime) -> bool:
    return start <= timestamp <= end


def _readonly_connection(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise AdapterError("EG4 database input does not exist or is not a file")
    try:
        connection = sqlite3.connect(
            f"{path.resolve().as_uri()}?mode=ro&immutable=1", uri=True
        )
        connection.execute("PRAGMA query_only = ON")
        return connection
    except sqlite3.Error as exc:
        raise AdapterError("EG4 database could not be opened read-only") from exc


def _require_columns(
    connection: sqlite3.Connection, table: str, expected: set[str]
) -> None:
    try:
        actual = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
    except sqlite3.Error as exc:
        raise AdapterError(f"EG4 schema unavailable for {table}") from exc
    missing = expected - actual
    if missing:
        names = ", ".join(sorted(missing))
        raise AdapterError(f"EG4 table {table} is missing required fields: {names}")


def iter_eg4_day_records(
    database_path: Path,
    start_utc: datetime,
    end_utc: datetime,
    *,
    batch_size: int = 256,
) -> Iterator[TimedRecord]:
    """Stream bounded EG4 day-series rows from an explicitly supplied database."""
    start = _utc_bound(start_utc, "start_utc")
    end = _utc_bound(end_utc, "end_utc")
    if start > end:
        raise AdapterError("start_utc must not be after end_utc")
    if batch_size < 1:
        raise AdapterError("batch_size must be positive")

    connection = _readonly_connection(Path(database_path))
    connection.row_factory = sqlite3.Row
    try:
        _require_columns(connection, "day_multiline_samples", DAY_COLUMNS)
        local_start = start.astimezone(ZoneInfo(CENTRAL))
        local_end = end.astimezone(ZoneInfo(CENTRAL))
        cursor = connection.execute(
            """
            SELECT serial_num, sample_time, solar_pv_w, grid_power_w,
                   battery_discharging_w, consumption_w, soc, ac_couple_power_w
            FROM day_multiline_samples
            WHERE sample_time >= ? AND sample_time <= ?
            ORDER BY sample_time
            """,
            (
                local_start.replace(tzinfo=None).isoformat(sep=" "),
                local_end.replace(tzinfo=None).isoformat(sep=" "),
            ),
        )
        while rows := cursor.fetchmany(batch_size):
            for row in rows:
                yield TimedRecord.from_source(
                    "eg4",
                    row["sample_time"],
                    "cloud_source_time",
                    {
                        "ac_couple_power_w": row["ac_couple_power_w"],
                        "load_power_w": row["consumption_w"],
                        "grid_power_w": row["grid_power_w"],
                        "solar_pv_w": row["solar_pv_w"],
                        "battery_discharge_power_w": row["battery_discharging_w"],
                        "estimated_soc_percent": row["soc"],
                    },
                    naive_timezone=CENTRAL,
                    provenance={
                        "input_name": Path(database_path).name,
                        "table": "day_multiline_samples",
                        "serial_num": row["serial_num"],
                    },
                )
    except sqlite3.Error as exc:
        raise AdapterError("EG4 day-series query failed") from exc
    finally:
        connection.close()


def _selected_runtime_context(raw_json: Any) -> dict[str, Any]:
    if not isinstance(raw_json, str):
        return {}
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError:
        return {"raw_context_valid": False}
    if not isinstance(parsed, dict):
        return {"raw_context_valid": False}
    selected: dict[str, Any] = {"raw_context_valid": True}
    for output, candidates in {
        "warning": ("warning", "warningCode", "warningText"),
        "fault": ("fault", "faultCode", "faultText"),
        "operating_mode": ("mode", "operatingMode", "workMode"),
    }.items():
        for candidate in candidates:
            if candidate in parsed:
                selected[output] = parsed[candidate]
                break
    return selected


def iter_eg4_runtime_records(
    database_path: Path,
    start_utc: datetime,
    end_utc: datetime,
    *,
    batch_size: int = 256,
) -> Iterator[TimedRecord]:
    """Stream bounded EG4 runtime context using its UTC server timestamp."""
    start = _utc_bound(start_utc, "start_utc")
    end = _utc_bound(end_utc, "end_utc")
    if start > end:
        raise AdapterError("start_utc must not be after end_utc")
    if batch_size < 1:
        raise AdapterError("batch_size must be positive")
    connection = _readonly_connection(Path(database_path))
    connection.row_factory = sqlite3.Row
    try:
        _require_columns(connection, "runtime_snapshots", RUNTIME_COLUMNS)
        cursor = connection.execute(
            """
            SELECT serial_num, server_time, status_text, soc, v_bat,
                   grid_freq_hz, eps_freq_hz, consumption_power_w,
                   ac_couple_power_w, raw_json, captured_at
            FROM runtime_snapshots
            WHERE server_time >= ? AND server_time <= ?
            ORDER BY server_time
            """,
            (
                start.replace(tzinfo=None).isoformat(sep=" "),
                end.replace(tzinfo=None).isoformat(sep=" "),
            ),
        )
        while rows := cursor.fetchmany(batch_size):
            for row in rows:
                if row["server_time"] is None:
                    raise AdapterError("EG4 runtime row has no server_time")
                values = {
                    "ac_couple_power_w": row["ac_couple_power_w"],
                    "load_power_w": row["consumption_power_w"],
                    "estimated_soc_percent": row["soc"],
                    "battery_voltage_v": row["v_bat"],
                    "grid_frequency_hz": row["grid_freq_hz"],
                    "eps_frequency_hz": row["eps_freq_hz"],
                    "operating_state": row["status_text"],
                    **_selected_runtime_context(row["raw_json"]),
                }
                yield TimedRecord.from_source(
                    "eg4_runtime",
                    row["server_time"],
                    "cloud_server_time",
                    values,
                    naive_timezone="UTC",
                    provenance={
                        "input_name": Path(database_path).name,
                        "table": "runtime_snapshots",
                        "serial_num": row["serial_num"],
                        "captured_at": row["captured_at"],
                    },
                )
    except sqlite3.Error as exc:
        raise AdapterError("EG4 runtime query failed") from exc
    finally:
        connection.close()


def _json_object(line: str, source: str, line_number: int) -> dict[str, Any]:
    try:
        value = json.loads(line)
    except json.JSONDecodeError as exc:
        raise AdapterError(f"{source} line {line_number}: malformed JSON") from exc
    if not isinstance(value, dict):
        raise AdapterError(f"{source} line {line_number}: record must be an object")
    return value


def _receipt_time(record: dict[str, Any], source: str, line_number: int) -> datetime:
    value = record.get("received_at_utc")
    if not isinstance(value, str):
        raise AdapterError(f"{source} line {line_number}: missing received_at_utc")
    try:
        normalized = normalize_timestamp(value)
    except (TypeError, ValueError) as exc:
        raise AdapterError(
            f"{source} line {line_number}: invalid canonical UTC receipt timestamp"
        ) from exc
    if not value.endswith("Z") or normalized.utcoffset() != UTC.utcoffset(None):
        raise AdapterError(
            f"{source} line {line_number}: receipt timestamp must use canonical UTC Z"
        )
    return normalized


def _metric_key(topic: str) -> str:
    return topic.replace("/", "_").replace("-", "_").replace(" ", "_")


def _solar_poll_record(
    path: Path,
    timestamp: str,
    metrics: dict[str, dict[str, Any]],
    first_line: int,
    last_line: int,
) -> TimedRecord:
    values: dict[str, Any] = {"metrics": metrics}
    for topic, metric in metrics.items():
        values[_metric_key(topic)] = metric["value"]
    trusted = metrics.get("total/battery_state_of_charge")
    if trusted is not None:
        values["trusted_soc_percent"] = trusted["value"]
    return TimedRecord.from_source(
        "solarassistant",
        timestamp,
        "solardt_receipt_time",
        values,
        provenance={
            "input_name": path.name,
            "line_start": first_line,
            "line_end": last_line,
            "battery_scope": "combined_and_per_battery",
        },
    )


def iter_solarassistant_records(
    input_path: Path, start_utc: datetime, end_utc: datetime
) -> Iterator[TimedRecord]:
    """Stream and group one SolarAssistant poll at a time from raw NDJSON."""
    start = _utc_bound(start_utc, "start_utc")
    end = _utc_bound(end_utc, "end_utc")
    if start > end:
        raise AdapterError("start_utc must not be after end_utc")
    path = Path(input_path)
    current_timestamp: str | None = None
    metrics: dict[str, dict[str, Any]] = {}
    first_line = 0
    last_line = 0
    previous_time: datetime | None = None
    try:
        handle = path.open("r", encoding="utf-8")
    except OSError as exc:
        raise AdapterError("SolarAssistant input could not be opened read-only") from exc
    with handle:
        for line_number, line in enumerate(handle, 1):
            record = _json_object(line, "SolarAssistant", line_number)
            timestamp = _receipt_time(record, "SolarAssistant", line_number)
            if previous_time is not None and timestamp < previous_time:
                raise AdapterError(
                    f"SolarAssistant line {line_number}: timestamps are not monotonic"
                )
            previous_time = timestamp
            if timestamp > end:
                if current_timestamp is not None:
                    current_time = normalize_timestamp(current_timestamp)
                    if _in_window(current_time, start, end):
                        yield _solar_poll_record(
                            path, current_timestamp, metrics, first_line, last_line
                        )
                current_timestamp = None
                break
            topic = record.get("topic")
            if not isinstance(topic, str) or not topic:
                raise AdapterError(f"SolarAssistant line {line_number}: missing topic")
            if "value" not in record:
                raise AdapterError(f"SolarAssistant line {line_number}: missing value")
            timestamp_text = record["received_at_utc"]
            if current_timestamp is not None and timestamp_text != current_timestamp:
                current_time = normalize_timestamp(current_timestamp)
                if _in_window(current_time, start, end):
                    yield _solar_poll_record(
                        path, current_timestamp, metrics, first_line, last_line
                    )
                metrics = {}
                first_line = line_number
            if current_timestamp is None:
                first_line = line_number
            current_timestamp = timestamp_text
            last_line = line_number
            metrics[topic] = {
                "value": record["value"],
                "unit": record.get("unit"),
                "device": record.get("device"),
                "number": record.get("number"),
                "group": record.get("group"),
                "name": record.get("name"),
            }
    if current_timestamp is not None:
        current_time = normalize_timestamp(current_timestamp)
        if _in_window(current_time, start, end):
            yield _solar_poll_record(
                path, current_timestamp, metrics, first_line, last_line
            )


ESP32_VALUE_KEYS = {
    "sensor-01_gen_frequency": "frequency_hz",
    "sensor-01_estimated_total_ac-coupled_power": "estimated_ac_couple_power_w",
    "sensor-01_estimated_active_microinverters": "active_microinverters",
    "text_sensor-04_forensic_event_log": "event",
    "text_sensor-00_current_status": "status",
}


def iter_esp32_records(
    input_path: Path,
    start_utc: datetime,
    end_utc: datetime,
    *,
    stream_kind: str,
) -> Iterator[TimedRecord]:
    """Stream bounded raw or retained ESP32 NDJSON observations."""
    if stream_kind not in {"raw", "retained"}:
        raise AdapterError("ESP32 stream_kind must be raw or retained")
    start = _utc_bound(start_utc, "start_utc")
    end = _utc_bound(end_utc, "end_utc")
    if start > end:
        raise AdapterError("start_utc must not be after end_utc")
    path = Path(input_path)
    previous_time: datetime | None = None
    try:
        handle = path.open("r", encoding="utf-8")
    except OSError as exc:
        raise AdapterError("ESP32 input could not be opened read-only") from exc
    with handle:
        for line_number, line in enumerate(handle, 1):
            record = _json_object(line, "ESP32", line_number)
            timestamp = _receipt_time(record, "ESP32", line_number)
            if previous_time is not None and timestamp < previous_time:
                raise AdapterError(
                    f"ESP32 line {line_number}: timestamps are not monotonic"
                )
            previous_time = timestamp
            if timestamp > end:
                break
            entity_id = record.get("id")
            if not isinstance(entity_id, str) or not entity_id:
                raise AdapterError(f"ESP32 line {line_number}: missing entity id")
            if entity_id not in APPROVED_ESP32_IDS:
                raise AdapterError(
                    f"ESP32 line {line_number}: entity id is not approved"
                )
            if "value" not in record and "state" not in record:
                raise AdapterError(f"ESP32 line {line_number}: missing value and state")
            if not _in_window(timestamp, start, end):
                continue
            value = record.get("value", record.get("state"))
            state = record.get("state")
            available = record.get("available")
            if not isinstance(available, bool):
                available = state not in {"unavailable", "unknown"}
            values: dict[str, Any] = {
                "metric_id": entity_id,
                "value": value,
                "unit": record.get("unit"),
                "available": available,
            }
            mapped = ESP32_VALUE_KEYS.get(entity_id)
            if mapped is not None:
                values[mapped] = value
            yield TimedRecord.from_source(
                "esp32",
                record["received_at_utc"],
                "solardt_receipt_time",
                values,
                provenance={
                    "input_name": path.name,
                    "line_number": line_number,
                    "stream_kind": stream_kind,
                    "entity_id": entity_id,
                    "name": record.get("name"),
                    "domain": record.get("domain"),
                    "retention_reason": record.get("retention_reason"),
                },
            )
