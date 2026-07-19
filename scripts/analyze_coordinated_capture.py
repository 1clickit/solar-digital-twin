#!/usr/bin/env python3
"""Run bounded, deterministic correlation over an explicit coordinated capture."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median
from typing import Any, Iterable
from zoneinfo import ZoneInfo

from solar_digital_twin.analysis.correlation_adapters import (
    AdapterError,
    iter_eg4_day_records,
    iter_eg4_runtime_records,
    iter_esp32_records,
    iter_solarassistant_records,
)
from solar_digital_twin.analysis.forensic_correlation import (
    CorrelationConfig,
    TimedRecord,
    analyze_correlation,
    nearest_record,
    normalize_timestamp,
)

UTC = timezone.utc
CENTRAL = ZoneInfo("America/Chicago")
MAX_EVENTS = 10
CONTEXT_MARGIN = timedelta(seconds=60)
CONTROL_RADIUS = timedelta(minutes=10)
EVENT_TOKENS = re.compile(
    r"\b(?:POWER_DROP|POWER_RISE|FREQ_DROP|FREQ_RISE|VOLT_DROP|VOLT_RISE|HIGH_FREQ|LOW_FREQ)\b"
)

PRIMARY_CONFIG = CorrelationConfig()
STRICT_CONFIG = replace(
    PRIMARY_CONFIG,
    minimum_baseline_w=1500.0,
    minimum_drop_w=750.0,
    minimum_drop_fraction=0.45,
    recovery_fraction=0.85,
)
LOOSE_CONFIG = replace(
    PRIMARY_CONFIG,
    minimum_baseline_w=750.0,
    minimum_drop_w=350.0,
    minimum_drop_fraction=0.25,
    recovery_fraction=0.75,
)
SENSITIVITY_CONFIGS = {
    "strict": STRICT_CONFIG,
    "primary": PRIMARY_CONFIG,
    "loose": LOOSE_CONFIG,
}

INPUT_ARGUMENTS = {
    "eg4": "eg4/eg4_capture.sqlite",
    "esp32_raw": "esp32/esp32_sse_20260718_062127Z.ndjson",
    "esp32_current": "esp32/esp32_sse_20260718_062127Z_retained.ndjson",
    "esp32_conservative": (
        "esp32/esp32_sse_20260718_062127Z_"
        "retained_esp32-conservative-v1.ndjson"
    ),
    "solarassistant_raw": (
        "solarassistant/solarassistant_20260718_062127Z.ndjson"
    ),
    "solarassistant_retained": (
        "solarassistant/solarassistant_20260718_062127Z_retained.ndjson"
    ),
}

TSV_FIELDS = [
    "identifier",
    "kind",
    "utc_time",
    "central_time",
    "classification",
    "eg4_before_w",
    "eg4_nadir_w",
    "eg4_recovery_w",
    "eg4_load_before_w",
    "eg4_load_at_nadir_w",
    "eg4_load_recovery_w",
    "drop_w",
    "drop_percent",
    "plateau_seconds",
    "recovery_seconds",
    "eg4_runtime_status",
    "solarassistant_status",
    "esp32_status",
    "esp32_frequency_hz",
    "esp32_voltage_v",
    "esp32_estimated_power_w",
    "esp32_curtailment_percent",
    "esp32_event_tokens",
    "esp32_availability_transitions",
    "esp32_active_microinverters",
    "trusted_soc_percent",
    "battery_voltage_v",
    "battery_current_a",
    "battery_power_w",
    "battery_flow_transition",
    "raw_preservation",
    "current_preservation",
    "conservative_preservation",
    "confidence",
    "principal_alternatives",
    "source_gap_qualification",
]


@dataclass(frozen=True)
class Identity:
    relative_path: str
    bytes: int
    mtime_ns: int
    sha256: str


@dataclass(frozen=True)
class Window:
    identifier: str
    kind: str
    start_utc: datetime
    center_utc: datetime
    end_utc: datetime


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def _parse_utc(value: str) -> datetime:
    parsed = normalize_timestamp(value)
    if not value.endswith("Z") and "+" not in value:
        raise argparse.ArgumentTypeError("UTC bounds must include an explicit offset")
    return parsed


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def load_inventory(path: Path) -> dict[str, Identity]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = csv.DictReader(handle, delimiter="\t")
            required = {"path", "bytes", "mtime_ns", "sha256"}
            if set(rows.fieldnames or ()) != required:
                raise ValueError("inventory fields are invalid")
            return {
                row["path"]: Identity(
                    row["path"], int(row["bytes"]), int(row["mtime_ns"]), row["sha256"]
                )
                for row in rows
            }
    except (OSError, ValueError, KeyError) as exc:
        raise ValueError("inventory could not be read safely") from exc


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def verify_identities(
    paths: dict[str, Path], evidence_root: Path, inventory_path: Path
) -> dict[str, Identity]:
    inventory = load_inventory(inventory_path)
    verified: dict[str, Identity] = {}
    for label, path in paths.items():
        resolved = path.resolve()
        if not _is_within(resolved, evidence_root):
            raise ValueError(f"{label} input is outside the authorized evidence root")
        try:
            relative = str(resolved.relative_to(evidence_root.resolve()))
        except ValueError as exc:  # defensive duplicate of the non-disclosure check
            raise ValueError(f"{label} input is outside the authorized evidence root") from exc
        if relative != INPUT_ARGUMENTS[label]:
            raise ValueError(f"{label} input is not the required primary artifact")
        expected = inventory.get(relative)
        if expected is None:
            raise ValueError(f"{label} input is absent from the tracked inventory")
        try:
            stat = resolved.stat()
        except OSError as exc:
            raise ValueError(f"{label} input is not readable") from exc
        actual = Identity(relative, stat.st_size, stat.st_mtime_ns, _sha256(resolved))
        if actual != expected:
            raise ValueError(f"{label} input identity does not match the tracked inventory")
        verified[label] = actual
    return verified


def refuse_evidence_output(output: Path, evidence_root: Path) -> None:
    if _is_within(output, evidence_root):
        raise ValueError("output path must not be beneath the evidence directory")


def _event_key(event: dict[str, Any]) -> str:
    return event["event_start_utc"]


def detect_candidates(
    eg4: list[TimedRecord], config: CorrelationConfig
) -> list[dict[str, Any]]:
    events = analyze_correlation(eg4, [], [], config)["events"]
    return sorted(
        events,
        key=lambda item: (-item["absolute_reduction_w"], item["event_start_utc"]),
    )


def _numeric(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _series_summary(records: Iterable[TimedRecord]) -> dict[str, Any]:
    grouped: dict[str, list[float]] = {}
    availability: dict[str, bool] = {}
    availability_changes = 0
    state_last: dict[str, Any] = {}
    state_changes = 0
    event_tokens: set[str] = set()
    count = 0
    for record in records:
        count += 1
        metric = str(record.values.get("metric_id", "unknown"))
        value = record.values.get("value")
        numeric = _numeric(value)
        if numeric is not None:
            grouped.setdefault(metric, []).append(numeric)
        current_available = bool(record.values.get("available", True))
        if metric in availability and availability[metric] != current_available:
            availability_changes += 1
        availability[metric] = current_available
        if metric.startswith(("binary_sensor-", "text_sensor-")):
            if metric in state_last and state_last[metric] != value:
                state_changes += 1
            state_last[metric] = value
        if metric == "text_sensor-04_forensic_event_log":
            event_tokens.update(EVENT_TOKENS.findall(str(value)))
    metrics = {
        name: {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "median": median(values),
            "first": values[0],
            "last": values[-1],
        }
        for name, values in sorted(grouped.items())
    }
    return {
        "records": count,
        "metrics": metrics,
        "availability_transitions": availability_changes,
        "state_transitions": state_changes,
        "event_tokens": sorted(event_tokens),
    }


def _solar_summary(records: list[TimedRecord]) -> dict[str, Any]:
    grouped: dict[str, list[float]] = {}
    for record in records:
        for topic, metric in record.values.get("metrics", {}).items():
            numeric = _numeric(metric.get("value"))
            if numeric is not None:
                grouped.setdefault(topic, []).append(numeric)
    return {
        topic: {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "median": median(values),
            "first": values[0],
            "last": values[-1],
        }
        for topic, values in sorted(grouped.items())
    }


def _metric_range(summary: dict[str, Any], metric: str) -> str:
    values = summary.get("metrics", {}).get(metric)
    if not values:
        return "missing"
    return f"{values['min']:.3f}..{values['max']:.3f}"


def _summary_range(summary: dict[str, Any], metric: str) -> str:
    values = summary.get(metric)
    if not values:
        return "missing"
    return f"{values['min']:.3f}..{values['max']:.3f}"


def _battery_flow(summary: dict[str, Any]) -> str:
    values = summary.get("total/battery_power")
    if not values:
        return "missing"

    def state(value: float) -> str:
        if value > 0:
            return "charging"
        if value < 0:
            return "discharging"
        return "idle"

    first = state(float(values["first"]))
    last = state(float(values["last"]))
    return first if first == last else f"{first}_to_{last}"


def _identity_payload(identities: dict[str, Identity]) -> dict[str, Any]:
    return {name: asdict(identity) for name, identity in sorted(identities.items())}


def _sanitize_derived(value: Any) -> Any:
    """Remove device identifiers from derived machine output recursively."""
    if isinstance(value, dict):
        return {
            key: _sanitize_derived(item)
            for key, item in value.items()
            if key != "serial_num"
        }
    if isinstance(value, list):
        return [_sanitize_derived(item) for item in value]
    return value


def _event_window(event: dict[str, Any], identifier: str) -> Window:
    before = normalize_timestamp(event["eg4_before"]["timestamp_utc"])
    center = normalize_timestamp(event["event_start_utc"])
    recovery = normalize_timestamp(event["recovery_time_utc"])
    return Window(identifier, "event", before - CONTEXT_MARGIN, center, recovery + CONTEXT_MARGIN)


def _overlaps_events(record: TimedRecord, events: list[dict[str, Any]]) -> bool:
    for event in events:
        start = normalize_timestamp(event["eg4_before"]["timestamp_utc"])
        end = normalize_timestamp(event["recovery_time_utc"])
        if start <= record.timestamp_utc <= end:
            return True
    return False


def select_controls(
    eg4: list[TimedRecord], events: list[dict[str, Any]]
) -> list[Window]:
    eligible = [record for record in eg4 if not _overlaps_events(record, events)]
    triples = [eligible[index : index + 3] for index in range(len(eligible) - 2)]
    contiguous = [
        group
        for group in triples
        if (group[-1].timestamp_utc - group[0].timestamp_utc) <= timedelta(minutes=20)
    ]
    strong = [
        group
        for group in contiguous
        if all((_numeric(row.values.get("ac_couple_power_w")) or 0) >= 2000 for row in group)
    ]
    if not strong:
        raise ValueError("no deterministic stable strong-production control is available")
    stable = min(
        strong,
        key=lambda group: (
            max(float(row.values["ac_couple_power_w"]) for row in group)
            - min(float(row.values["ac_couple_power_w"]) for row in group),
            group[1].timestamp_utc,
        ),
    )
    gradual = [
        group
        for group in contiguous
        if all((_numeric(row.values.get("ac_couple_power_w")) or 0) > 100 for row in group)
        and 0
        < max(float(row.values["ac_couple_power_w"]) for row in group)
        - min(float(row.values["ac_couple_power_w"]) for row in group)
        < PRIMARY_CONFIG.minimum_drop_w
    ]
    if not gradual:
        raise ValueError("no deterministic gradual-variation control is available")
    varying = max(
        gradual,
        key=lambda group: (
            max(float(row.values["ac_couple_power_w"]) for row in group)
            - min(float(row.values["ac_couple_power_w"]) for row in group),
            -group[1].timestamp_utc.timestamp(),
        ),
    )
    night = next(
        (record for record in eligible if (_numeric(record.values.get("ac_couple_power_w")) or 0) <= PRIMARY_CONFIG.zero_output_threshold_w),
        None,
    )
    if night is None:
        raise ValueError("no deterministic nighttime control is available")
    choices = [
        ("control-strong", "stable_strong_production", stable[1]),
        ("control-gradual", "gradual_variation", varying[1]),
        ("control-night", "nighttime_near_zero", night),
    ]
    return [
        Window(identifier, kind, row.timestamp_utc - CONTROL_RADIUS, row.timestamp_utc, row.timestamp_utc + CONTROL_RADIUS)
        for identifier, kind, row in choices
    ]


def _records_for_window(
    args: argparse.Namespace, window: Window, stream: str
) -> list[TimedRecord]:
    path = getattr(args, stream)
    kind = "raw" if stream == "esp32_raw" else "retained"
    return list(iter_esp32_records(path, window.start_utc, window.end_utc, stream_kind=kind))


def _bounded_file_stats(path: Path, window: Window) -> dict[str, int]:
    records = 0
    byte_count = 0
    try:
        handle = path.open("rb")
    except OSError as exc:
        raise ValueError("bounded NDJSON input could not be opened") from exc
    with handle:
        for number, line in enumerate(handle, 1):
            try:
                record = json.loads(line)
                timestamp = normalize_timestamp(record["received_at_utc"])
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"bounded NDJSON line {number} is invalid") from exc
            if timestamp > window.end_utc:
                break
            if timestamp >= window.start_utc:
                records += 1
                byte_count += len(line)
    return {"records": records, "bytes": byte_count}


def _matching_event(report: dict[str, Any], start_utc: str) -> dict[str, Any] | None:
    return next((item for item in report["events"] if item["event_start_utc"] == start_utc), None)


def _preservation(
    primary: dict[str, Any] | None,
    candidate: dict[str, Any] | None,
    summary: dict[str, Any],
) -> str:
    if primary is None:
        return "no_event" if candidate is None else "changed"
    if candidate is None or candidate["event_type"] != primary["event_type"]:
        return "changed"
    critical = {
        "sensor-01_gen_frequency",
        "sensor-01_estimated_gen_l1-l2_voltage",
        "sensor-01_estimated_total_ac-coupled_power",
        "sensor-01_estimated_active_microinverters",
    }
    return "preserved" if critical <= set(summary["metrics"]) else "qualified_missing"


def _context_status(event: dict[str, Any] | None, source: str) -> str:
    if event is None:
        return "not_applicable"
    if source == "runtime":
        return event["aligned_context"]["eg4_runtime"]["during"]["status"]
    if source == "solar":
        return event["solarassistant_context"]["status"]
    return event["esp32_nearest"]["status"]


def _event_context(
    args: argparse.Namespace,
    eg4: list[TimedRecord],
    window: Window,
    event: dict[str, Any] | None,
) -> dict[str, Any]:
    runtime = list(iter_eg4_runtime_records(args.eg4, window.start_utc, window.end_utc))
    solar = list(iter_solarassistant_records(args.solarassistant_raw, window.start_utc, window.end_utc))
    retained_solar = list(iter_solarassistant_records(args.solarassistant_retained, window.start_utc, window.end_utc))
    streams: dict[str, Any] = {}
    detector_event = event
    for name in ("esp32_raw", "esp32_current", "esp32_conservative"):
        records = _records_for_window(args, window, name)
        summary = _series_summary(records)
        near_records = [
            record
            for record in records
            if abs((record.timestamp_utc - window.center_utc).total_seconds()) <= 30
        ]
        report = analyze_correlation(
            eg4,
            solar,
            records,
            PRIMARY_CONFIG,
            eg4_context_records=runtime,
        )
        matched = _matching_event(report, event["event_start_utc"]) if event else None
        streams[name] = {
            "summary": summary,
            "near_summary": _series_summary(near_records),
            "bounded_file": _bounded_file_stats(getattr(args, name), window),
            "event": matched,
            "preservation": _preservation(detector_event, matched, summary),
        }
    center_day = nearest_record(eg4, window.center_utc, 420.0)
    center_runtime = nearest_record(runtime, window.center_utc, PRIMARY_CONFIG.eg4_runtime_tolerance_seconds)
    center_solar = nearest_record(solar, window.center_utc, PRIMARY_CONFIG.solarassistant_tolerance_seconds)
    return {
        "identifier": window.identifier,
        "kind": window.kind,
        "window": {"start_utc": _iso(window.start_utc), "center_utc": _iso(window.center_utc), "end_utc": _iso(window.end_utc)},
        "detector_event": detector_event,
        "primary_event": streams["esp32_raw"]["event"] if detector_event else None,
        "eg4_day_center": center_day,
        "eg4_runtime_center": center_runtime,
        "solarassistant_center": center_solar,
        "solarassistant_summary": _solar_summary(solar),
        "solarassistant_near_summary": _solar_summary(
            [
                record
                for record in solar
                if abs((record.timestamp_utc - window.center_utc).total_seconds()) <= 30
            ]
        ),
        "solarassistant_retained_summary": _solar_summary(retained_solar),
        "solarassistant_raw_polls": len(solar),
        "solarassistant_retained_polls": len(retained_solar),
        "streams": streams,
    }


def _control_eg4(eg4: list[TimedRecord], window: Window) -> list[TimedRecord]:
    return [record for record in eg4 if window.start_utc <= record.timestamp_utc <= window.end_utc]


def _compact_row(context: dict[str, Any]) -> dict[str, Any]:
    event = context["primary_event"]
    raw = context["streams"]["esp32_raw"]
    raw_summary = raw["summary"]
    solar = context["solarassistant_summary"]
    center = normalize_timestamp(context["window"]["center_utc"])
    frequency = _metric_range(raw_summary, "sensor-01_gen_frequency")
    voltage = _metric_range(raw_summary, "sensor-01_estimated_gen_l1-l2_voltage")
    estimated_power = _metric_range(
        raw["near_summary"], "sensor-01_estimated_total_ac-coupled_power"
    )
    curtailment = _metric_range(
        raw["near_summary"], "sensor-01_estimated_curtailment_percent"
    )
    active = _metric_range(raw_summary, "sensor-01_estimated_active_microinverters")
    trusted = solar.get("total/battery_state_of_charge", {})
    battery_voltage = solar.get("total/battery_voltage", {})
    battery_current = solar.get("total/battery_current", {})
    battery_power = solar.get("total/battery_power", {})
    confidence = event["confidence"]["level"] if event else "control"
    return {
        "identifier": context["identifier"],
        "kind": context["kind"],
        "utc_time": _iso(center),
        "central_time": center.astimezone(CENTRAL).isoformat(timespec="seconds"),
        "classification": event["event_type"] if event else context["kind"],
        "eg4_before_w": event["pre_event_baseline_w"] if event else "",
        "eg4_nadir_w": event["plateau_low_w"] if event else "",
        "eg4_recovery_w": event["eg4_recovery"]["values"]["ac_couple_power_w"] if event else "",
        "eg4_load_before_w": event["eg4_before"]["values"].get("load_power_w", "") if event else "",
        "eg4_load_at_nadir_w": (
            min(
                event["eg4_plateau"],
                key=lambda row: row["values"]["ac_couple_power_w"],
            )["values"].get("load_power_w", "")
            if event
            else ""
        ),
        "eg4_load_recovery_w": event["eg4_recovery"]["values"].get("load_power_w", "") if event else "",
        "drop_w": event["absolute_reduction_w"] if event else "",
        "drop_percent": event["percentage_reduction"] if event else "",
        "plateau_seconds": event["plateau_duration_seconds"] if event else "",
        "recovery_seconds": event["recovery_seconds"] if event else "",
        "eg4_runtime_status": _context_status(raw.get("event"), "runtime"),
        "solarassistant_status": _context_status(raw.get("event"), "solar"),
        "esp32_status": _context_status(raw.get("event"), "esp32"),
        "esp32_frequency_hz": frequency,
        "esp32_voltage_v": voltage,
        "esp32_estimated_power_w": estimated_power,
        "esp32_curtailment_percent": curtailment,
        "esp32_event_tokens": ";".join(raw["near_summary"]["event_tokens"]),
        "esp32_availability_transitions": raw_summary["availability_transitions"],
        "esp32_active_microinverters": active,
        "trusted_soc_percent": trusted.get("median", ""),
        "battery_voltage_v": _summary_range(solar, "total/battery_voltage"),
        "battery_current_a": _summary_range(solar, "total/battery_current"),
        "battery_power_w": battery_power.get("median", ""),
        "battery_flow_transition": _battery_flow(solar),
        "raw_preservation": raw["preservation"],
        "current_preservation": context["streams"]["esp32_current"]["preservation"],
        "conservative_preservation": context["streams"]["esp32_conservative"]["preservation"],
        "confidence": confidence,
        "principal_alternatives": "cloud_or_solar_variability;load;battery_constraints;aggregation_and_timing;electrical_control_or_dropout",
        "source_gap_qualification": "eg4_cadence" if event and event["eg4_gap_limited"] else "none_observed",
    }


def write_tsv(path: Path, contexts: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TSV_FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(_compact_row(context) for context in contexts)


def write_svg(path: Path, contexts: list[dict[str, Any]]) -> None:
    """Write a deterministic, self-contained event/control overview."""
    rows = [_compact_row(context) for context in contexts]
    width = 1200
    left = 255
    chart_width = 860
    row_height = 54
    height = 112 + row_height * len(rows)
    event_values = [
        float(row[field])
        for row in rows
        if row["kind"] == "event"
        for field in ("eg4_before_w", "eg4_nadir_w", "eg4_recovery_w")
        if row[field] != ""
    ]
    maximum = max(event_values, default=1.0)

    def x(value: float) -> float:
        return left + chart_width * value / maximum

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:system-ui,sans-serif;fill:#17202a}.title{font-size:22px;font-weight:700}.sub{font-size:13px;fill:#52606d}.label{font-size:13px}.value{font-size:12px;fill:#334e68}.grid{stroke:#d9e2ec;stroke-width:1}.path{stroke:#486581;stroke-width:2;fill:none}.point{stroke:#ffffff;stroke-width:1.5}.control{fill:#829ab1}</style>',
        '<text class="title" x="32" y="35">Coordinated capture correlation overview</text>',
        '<text class="sub" x="32" y="59">EG4 baseline → nadir → recovery; points are observed samples, not interpolated transition times</text>',
    ]
    for tick in range(0, 5):
        value = maximum * tick / 4
        xpos = x(value)
        lines.append(f'<line class="grid" x1="{xpos:.1f}" y1="78" x2="{xpos:.1f}" y2="{height - 24}"/>')
        lines.append(f'<text class="sub" text-anchor="middle" x="{xpos:.1f}" y="75">{value / 1000:.1f} kW</text>')
    for index, row in enumerate(rows):
        ypos = 104 + index * row_height
        label = f'{row["identifier"]}  {row["central_time"][11:19]}  {row["classification"]}'
        lines.append(f'<text class="label" x="32" y="{ypos + 5}">{html.escape(label)}</text>')
        if row["kind"] == "event":
            values = [float(row[name]) for name in ("eg4_before_w", "eg4_nadir_w", "eg4_recovery_w")]
            points = " ".join(f'{x(value):.1f},{ypos:.1f}' for value in values)
            lines.append(f'<polyline class="path" points="{points}"/>')
            for value, color in zip(values, ("#2f855a", "#c53030", "#2b6cb0")):
                lines.append(f'<circle class="point" cx="{x(value):.1f}" cy="{ypos:.1f}" r="6" fill="{color}"/>')
            summary = f'{values[0]:.0f} → {values[1]:.0f} → {values[2]:.0f} W'
            lines.append(f'<text class="value" x="{left}" y="{ypos + 20}">{summary}</text>')
        else:
            lines.append(f'<circle class="control" cx="{left:.1f}" cy="{ypos:.1f}" r="6"/>')
            lines.append(f'<text class="value" x="{left + 14}" y="{ypos + 5}">comparison window (no candidate)</text>')
    lines.append('</svg>')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    for name in INPUT_ARGUMENTS:
        parser.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    parser.add_argument("--start-utc", type=_parse_utc, required=True)
    parser.add_argument("--end-utc", type=_parse_utc, required=True)
    parser.add_argument("--analysis-commit", required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--tsv-output", type=Path, required=True)
    parser.add_argument("--svg-output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.start_utc > args.end_utc:
        parser.error("--start-utc must not be after --end-utc")
    outputs = (args.json_output, args.tsv_output, args.svg_output)
    if len({output.resolve() for output in outputs}) != len(outputs):
        parser.error("derived output paths must be distinct")
    for output in outputs:
        try:
            refuse_evidence_output(output, args.evidence_root)
        except ValueError as exc:
            parser.error(str(exc))
    return args


def run(args: argparse.Namespace) -> dict[str, Any]:
    paths = {name: getattr(args, name) for name in INPUT_ARGUMENTS}
    pre = verify_identities(paths, args.evidence_root, args.inventory)
    print("Verified six pre-analysis evidence identities.")
    eg4 = list(iter_eg4_day_records(args.eg4, args.start_utc, args.end_utc))
    primary = detect_candidates(eg4, PRIMARY_CONFIG)
    sensitivity_events = {
        name: detect_candidates(eg4, config)
        for name, config in SENSITIVITY_CONFIGS.items()
    }
    selected = primary[:MAX_EVENTS]
    windows = [_event_window(event, f"event-{index:02d}") for index, event in enumerate(selected, 1)]
    controls = select_controls(eg4, primary)
    contexts = [
        _event_context(args, eg4, window, event)
        for window, event in zip(windows, selected)
    ]
    for window in controls:
        local_eg4 = _control_eg4(eg4, window)
        context = _event_context(args, local_eg4, window, None)
        contexts.append(context)
    post = verify_identities(paths, args.evidence_root, args.inventory)
    if pre != post:
        raise ValueError("primary evidence identity changed during analysis")
    primary_keys = {_event_key(event) for event in primary}
    sensitivity = {
        name: {
            "config": asdict(SENSITIVITY_CONFIGS[name]),
            "candidate_count": len(events),
            "candidate_starts_utc": [_event_key(event) for event in events],
            "primary_stable_starts_utc": [
                _event_key(event) for event in events if _event_key(event) in primary_keys
            ],
        }
        for name, events in sensitivity_events.items()
    }
    report = {
        "schema": "solar-digital-twin.coordinated-correlation.v1",
        "capture_id": args.evidence_root.name,
        "analysis_commit": args.analysis_commit,
        "analysis_bounds": {"start_utc": _iso(args.start_utc), "end_utc": _iso(args.end_utc)},
        "timestamp_semantics": {
            "eg4_day": "naive America/Chicago cloud sample_time normalized to UTC",
            "eg4_runtime": "naive text server_time explicitly interpreted as UTC",
            "solarassistant": "canonical solardt UTC receipt time",
            "esp32": "canonical solardt UTC receipt time",
        },
        "identity_pre": _identity_payload(pre),
        "identity_post": _identity_payload(post),
        "identities_stable": pre == post,
        "primary_config": asdict(PRIMARY_CONFIG),
        "candidate_count": len(primary),
        "candidate_summaries": primary,
        "selected_event_count": len(selected),
        "control_count": len(controls),
        "sensitivity": sensitivity,
        "contexts": contexts,
        "esp32_manifest_qualification": (
            "source-specific manifest lacks terminal record; common manifest records "
            "controlled SIGTERM and all ESP32 streams end cleanly"
        ),
        "causation_claimed": False,
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    report = _sanitize_derived(report)
    args.json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_tsv(args.tsv_output, report["contexts"])
    write_svg(args.svg_output, report["contexts"])
    print(f"Primary candidates: {len(primary)}; detailed: {len(selected)}; controls: {len(controls)}.")
    print("Verified stable post-analysis evidence identities.")
    return report


def main() -> int:
    try:
        run(parse_args())
    except (AdapterError, OSError, ValueError) as exc:
        print(f"Analysis stopped: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
