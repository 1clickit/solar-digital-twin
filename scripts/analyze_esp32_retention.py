#!/usr/bin/env python3
"""Stream an ESP32 raw/retained capture and summarize retention behavior."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

FREQUENCY_ID = "sensor-01_gen_frequency"
UNAVAILABLE = {"unavailable", "unknown", "none", "nan", "null"}
NUMERIC_DEADBANDS = {
    "sensor-01_estimated_total_ac-coupled_power": 10.0,
    "sensor-01_estimated_active_microinverters": 0.1,
    "sensor-01_estimated_curtailment_percent": 0.5,
    FREQUENCY_ID: 0.04,
    "sensor-01_gen_l1_current": 0.1,
    "sensor-01_estimated_gen_l1-l2_voltage": 0.1,
    "sensor-01_estimated_total_ac-coupled_energy": 10.0,
    "sensor-02_power_ramp_rate": 10.0,
    "sensor-02_frequency_ramp_rate": 0.04,
    "sensor-02_largest_power_drop_since_reset": 10.0,
    "sensor-02_total_events_since_reset": 1.0,
}


def timestamp_seconds(value: str) -> float:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def value_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def unavailable(value: Any) -> bool:
    return value is None or str(value).strip().lower() in UNAVAILABLE


@dataclass
class EntityStats:
    raw_count: int = 0
    raw_bytes: int = 0
    retained_count: int = 0
    retained_bytes: int = 0
    changes: int = 0
    repeats: int = 0
    availability_transitions: int = 0
    largest_gap_seconds: float = 0.0
    last_time: float | None = None
    last_key: str | None = None
    last_unavailable: bool | None = None
    unique_values: set[str] = field(default_factory=set)
    unique_capped: bool = False
    gap_samples: list[float] = field(default_factory=list)
    delta_samples: list[float] = field(default_factory=list)
    numeric_min: float | None = None
    numeric_max: float | None = None

    def observe(self, record: dict[str, Any], byte_count: int) -> None:
        now = timestamp_seconds(record["received_at_utc"])
        key = value_key(record.get("value"))
        is_unavailable = unavailable(record.get("value"))
        current_numeric = numeric(record.get("value"))
        self.raw_count += 1
        self.raw_bytes += byte_count
        if len(self.unique_values) < 20_000:
            self.unique_values.add(key)
        elif key not in self.unique_values:
            self.unique_capped = True
        if self.last_time is not None:
            gap = now - self.last_time
            self.largest_gap_seconds = max(self.largest_gap_seconds, gap)
            if len(self.gap_samples) < 50_000:
                self.gap_samples.append(gap)
            if key == self.last_key:
                self.repeats += 1
            else:
                self.changes += 1
            if is_unavailable != self.last_unavailable:
                self.availability_transitions += 1
            previous_numeric = numeric(json.loads(self.last_key))
            if current_numeric is not None and previous_numeric is not None:
                if len(self.delta_samples) < 50_000:
                    self.delta_samples.append(abs(current_numeric - previous_numeric))
        if current_numeric is not None:
            self.numeric_min = (
                current_numeric if self.numeric_min is None
                else min(self.numeric_min, current_numeric)
            )
            self.numeric_max = (
                current_numeric if self.numeric_max is None
                else max(self.numeric_max, current_numeric)
            )
        self.last_time = now
        self.last_key = key
        self.last_unavailable = is_unavailable


@dataclass
class PolicyState:
    last_value: Any = None
    last_numeric: float | None = None
    last_unavailable: bool | None = None
    last_retained_at: float | None = None
    seen: bool = False


@dataclass(frozen=True)
class Candidate:
    name: str
    heartbeat_seconds: float
    numeric_deadbands: dict[str, float]
    current_frequency_only: bool = False


class CandidateRun:
    def __init__(self, candidate: Candidate):
        self.candidate = candidate
        self.states: dict[str, PolicyState] = {}
        self.count = 0
        self.byte_count = 0
        self.reasons: Counter[str] = Counter()

    def observe(self, record: dict[str, Any], byte_count: int) -> None:
        entity = record["id"]
        if self.candidate.current_frequency_only and entity != FREQUENCY_ID:
            self._retain("pass_through", byte_count)
            return
        state = self.states.setdefault(entity, PolicyState())
        value = record.get("value")
        current_numeric = numeric(value)
        current_unavailable = unavailable(value)
        now = timestamp_seconds(record["received_at_utc"])
        reason = None
        if not state.seen:
            reason = "first"
        elif current_unavailable != state.last_unavailable:
            reason = "availability_transition"
        elif current_numeric is not None and entity in self.candidate.numeric_deadbands:
            threshold = self.candidate.numeric_deadbands[entity]
            if state.last_numeric is None or abs(current_numeric - state.last_numeric) >= threshold:
                reason = "change"
        elif value_key(value) != value_key(state.last_value):
            reason = "change"
        if (
            reason is None
            and state.last_retained_at is not None
            and now - state.last_retained_at >= self.candidate.heartbeat_seconds
        ):
            reason = "heartbeat"
        if reason is not None:
            self._retain(reason, byte_count)
            state.last_value = value
            state.last_numeric = current_numeric
            state.last_unavailable = current_unavailable
            state.last_retained_at = now
            state.seen = True

    def _retain(self, reason: str, byte_count: int) -> None:
        self.count += 1
        self.byte_count += byte_count
        self.reasons[reason] += 1


def candidates() -> list[Candidate]:
    return [
        Candidate("current", 30.0, {FREQUENCY_ID: 0.04}, True),
        Candidate("entity_deadbands_30s", 30.0, NUMERIC_DEADBANDS),
        Candidate("exact_change_120s", 120.0, {}, False),
        Candidate("conservative_combined_60s", 60.0, NUMERIC_DEADBANDS),
    ]


def analyze(raw_path: Path, retained_path: Path) -> dict[str, Any]:
    entities: dict[str, EntityStats] = {}
    runs = [CandidateRun(candidate) for candidate in candidates()]
    raw_count = raw_bytes = 0
    with raw_path.open(encoding="utf-8") as source:
        for line in source:
            record = json.loads(line)
            byte_count = len(line.encode("utf-8"))
            entity = str(record["id"])
            entities.setdefault(entity, EntityStats()).observe(record, byte_count)
            for run in runs:
                run.observe(record, byte_count)
            raw_count += 1
            raw_bytes += byte_count

    retained_count = retained_bytes = 0
    with retained_path.open(encoding="utf-8") as source:
        for line in source:
            record = json.loads(line)
            byte_count = len(line.encode("utf-8"))
            entity = str(record["id"])
            entities[entity].retained_count += 1
            entities[entity].retained_bytes += byte_count
            retained_count += 1
            retained_bytes += byte_count

    def percentile(values: list[float], fraction: float) -> float | None:
        if not values:
            return None
        ordered = sorted(values)
        return round(ordered[round((len(ordered) - 1) * fraction)], 6)

    def delta_bands(entity: str, stats: EntityStats) -> dict[str, int] | None:
        threshold = NUMERIC_DEADBANDS.get(entity)
        if threshold is None or not stats.delta_samples:
            return None
        epsilon = 1e-9
        return {
            "below": sum(value < threshold - epsilon for value in stats.delta_samples),
            "equal": sum(abs(value - threshold) <= epsilon for value in stats.delta_samples),
            "above": sum(value > threshold + epsilon for value in stats.delta_samples),
        }

    return {
        "raw": {"records": raw_count, "bytes": raw_bytes},
        "retained": {"records": retained_count, "bytes": retained_bytes},
        "entities": {
            entity: {
                "raw": stats.raw_count,
                "retained": stats.retained_count,
                "retained_percent": round(100 * stats.retained_count / stats.raw_count, 3),
                "raw_bytes": stats.raw_bytes,
                "retained_bytes": stats.retained_bytes,
                "changes": stats.changes,
                "repeats": stats.repeats,
                "unique_values": len(stats.unique_values),
                "unique_values_capped": stats.unique_capped,
                "availability_transitions": stats.availability_transitions,
                "cadence_median_seconds": percentile(stats.gap_samples, 0.5),
                "largest_gap_seconds": round(stats.largest_gap_seconds, 3),
                "numeric_min": stats.numeric_min,
                "numeric_max": stats.numeric_max,
                "absolute_delta_p50": percentile(stats.delta_samples, 0.5),
                "absolute_delta_p90": percentile(stats.delta_samples, 0.9),
                "absolute_delta_p99": percentile(stats.delta_samples, 0.99),
                "candidate_deadband": NUMERIC_DEADBANDS.get(entity),
                "delta_bands": delta_bands(entity, stats),
            }
            for entity, stats in sorted(
                entities.items(), key=lambda item: item[1].retained_bytes, reverse=True
            )
        },
        "candidates": {
            run.candidate.name: {
                "records": run.count,
                "retained_percent": round(100 * run.count / raw_count, 3),
                "bytes": run.byte_count,
                "byte_percent": round(100 * run.byte_count / raw_bytes, 3),
                "reasons": dict(run.reasons),
            }
            for run in runs
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("raw", type=Path)
    parser.add_argument("retained", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(analyze(args.raw, args.retained), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
