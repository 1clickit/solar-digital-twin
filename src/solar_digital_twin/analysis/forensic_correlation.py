"""Pure offline helpers for source-labeled forensic event correlation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from statistics import median
from typing import Any, Iterable, Mapping, Sequence
from zoneinfo import ZoneInfo

UTC = timezone.utc


def normalize_timestamp(value: str, naive_timezone: str | None = None) -> datetime:
    """Normalize an ISO timestamp, rejecting naive input without an explicit zone."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        if naive_timezone is None:
            raise ValueError("naive timestamp requires an explicit source timezone")
        parsed = parsed.replace(tzinfo=ZoneInfo(naive_timezone))
    return parsed.astimezone(UTC)


@dataclass(frozen=True)
class TimedRecord:
    source: str
    timestamp_utc: datetime
    original_timestamp: str
    timestamp_kind: str
    values: Mapping[str, Any]
    provenance: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_source(
        cls,
        source: str,
        timestamp: str,
        timestamp_kind: str,
        values: Mapping[str, Any],
        *,
        naive_timezone: str | None = None,
        provenance: Mapping[str, Any] | None = None,
    ) -> "TimedRecord":
        return cls(
            source=source,
            timestamp_utc=normalize_timestamp(timestamp, naive_timezone),
            original_timestamp=timestamp,
            timestamp_kind=timestamp_kind,
            values=dict(values),
            provenance=dict(provenance or {}),
        )


@dataclass(frozen=True)
class CorrelationConfig:
    minimum_baseline_w: float = 1000.0
    minimum_drop_w: float = 500.0
    minimum_drop_fraction: float = 0.35
    minimum_plateau_samples: int = 2
    recovery_fraction: float = 0.80
    zero_output_threshold_w: float = 25.0
    maximum_search_samples: int = 12
    maximum_eg4_gap_seconds: float = 600.0
    eg4_runtime_tolerance_seconds: float = 600.0
    solarassistant_tolerance_seconds: float = 15.0
    esp32_tolerance_seconds: float = 2.0
    context_before_seconds: float = 30.0
    context_after_seconds: float = 30.0
    supporting_frequency_change_hz: float = 0.04

    def __post_init__(self) -> None:
        if self.minimum_baseline_w <= 0 or self.minimum_drop_w <= 0:
            raise ValueError("power thresholds must be positive")
        if not 0 < self.minimum_drop_fraction < 1:
            raise ValueError("minimum_drop_fraction must be between zero and one")
        if self.minimum_plateau_samples < 2:
            raise ValueError("minimum_plateau_samples must be at least two")
        if not 0 < self.recovery_fraction <= 1:
            raise ValueError("recovery_fraction must be between zero and one")


def ordered(records: Iterable[TimedRecord]) -> list[TimedRecord]:
    """Return deterministic native records ordered by normalized UTC time."""
    return sorted(records, key=lambda record: record.timestamp_utc)


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def _safe_record(record: TimedRecord) -> dict[str, Any]:
    return {
        "source": record.source,
        "timestamp_utc": _iso(record.timestamp_utc),
        "original_timestamp": record.original_timestamp,
        "timestamp_kind": record.timestamp_kind,
        "values": dict(record.values),
        "provenance": dict(record.provenance),
    }


def nearest_record(
    records: Sequence[TimedRecord],
    target: datetime,
    tolerance_seconds: float,
) -> dict[str, Any]:
    """Return an exact/nearest match or an explicit missing result."""
    if tolerance_seconds < 0:
        raise ValueError("tolerance_seconds must not be negative")
    if not records:
        return {"status": "missing", "reason": "no_records", "record": None}
    candidate = min(records, key=lambda item: abs((item.timestamp_utc - target).total_seconds()))
    delta = (candidate.timestamp_utc - target).total_seconds()
    if abs(delta) > tolerance_seconds:
        return {
            "status": "missing",
            "reason": "out_of_tolerance",
            "nearest_delta_seconds": round(delta, 3),
            "record": None,
        }
    return {
        "status": "exact" if delta == 0 else "nearest",
        "delta_seconds": round(delta, 3),
        "record": _safe_record(candidate),
    }


def _aligned_phases(
    records: Sequence[TimedRecord],
    phases: Mapping[str, datetime],
    tolerance_seconds: float,
) -> dict[str, Any]:
    return {
        name: nearest_record(records, timestamp, tolerance_seconds)
        for name, timestamp in phases.items()
    }


def _window(
    records: Sequence[TimedRecord], start: datetime, end: datetime
) -> list[TimedRecord]:
    return [record for record in records if start <= record.timestamp_utc <= end]


def _availability_transitions(records: Sequence[TimedRecord]) -> int:
    states = [record.values.get("available") for record in records if "available" in record.values]
    return sum(before != after for before, after in zip(states, states[1:]))


def _esp32_summary(records: Sequence[TimedRecord], threshold: float) -> dict[str, Any]:
    frequencies = [
        float(record.values["frequency_hz"])
        for record in records
        if isinstance(record.values.get("frequency_hz"), (int, float))
    ]
    event_names = sorted(
        {
            str(record.values["event"])
            for record in records
            if record.values.get("event") not in (None, "")
        }
    )
    frequency_range = max(frequencies) - min(frequencies) if frequencies else None
    return {
        "records": len(records),
        "frequency_min_hz": min(frequencies) if frequencies else None,
        "frequency_max_hz": max(frequencies) if frequencies else None,
        "frequency_change_hz": frequency_range,
        "frequency_supporting": frequency_range is not None and frequency_range >= threshold,
        "events": event_names,
        "availability_transitions": _availability_transitions(records),
    }


def _post_recovery_behavior(records: Sequence[TimedRecord], recovery_index: int) -> str:
    following = [
        float(record.values["ac_couple_power_w"])
        for record in records[recovery_index : recovery_index + 3]
        if isinstance(record.values.get("ac_couple_power_w"), (int, float))
    ]
    if len(following) >= 3 and following[0] < following[1] < following[2]:
        return "gradual_ramp"
    if len(following) >= 2 and following[1] >= following[0]:
        return "step_recovery"
    return "unknown"


def _confidence(
    *,
    persistent_plateau: bool,
    recovery: bool,
    post_behavior: str,
    esp32: Mapping[str, Any],
    solar_match: Mapping[str, Any],
    gap_limited: bool,
) -> dict[str, Any]:
    raising = ["abrupt_eg4_power_reduction"]
    lowering = ["cloud_cover_or_normal_solar_variability_remains_possible"]
    score = 1
    if persistent_plateau:
        raising.append("persistent_non_zero_plateau")
        score += 1
    if recovery:
        raising.append("recovery_observed")
        score += 1
    if esp32["events"] or esp32["availability_transitions"]:
        raising.append("esp32_event_or_availability_transition")
        score += 1
    if esp32["frequency_supporting"]:
        raising.append("supporting_esp32_frequency_change")
        score += 1
    if post_behavior == "gradual_ramp":
        lowering.append("gradual_post_recovery_behavior_is_not_unique_to_dropout")
    if solar_match["status"] == "missing":
        lowering.append("trusted_battery_context_missing")
        score -= 1
    if esp32["records"] == 0:
        lowering.append("esp32_context_missing")
        score -= 1
    if gap_limited:
        lowering.append("eg4_cadence_gap_limits_timing_precision")
        score -= 1
    level = "high" if score >= 4 else "moderate" if score >= 2 else "low"
    return {"level": level, "raising_factors": raising, "lowering_factors": lowering}


def analyze_correlation(
    eg4_records: Iterable[TimedRecord],
    solarassistant_records: Iterable[TimedRecord],
    esp32_records: Iterable[TimedRecord],
    config: CorrelationConfig | None = None,
    *,
    eg4_context_records: Iterable[TimedRecord] = (),
) -> dict[str, Any]:
    """Analyze already parsed records without I/O, interpolation, or mutation."""
    cfg = config or CorrelationConfig()
    eg4 = ordered(eg4_records)
    eg4_context = ordered(eg4_context_records)
    solar = ordered(solarassistant_records)
    esp32 = ordered(esp32_records)
    events: list[dict[str, Any]] = []
    index = 1
    while index < len(eg4):
        before = eg4[index - 1]
        dropped = eg4[index]
        baseline = before.values.get("ac_couple_power_w")
        after = dropped.values.get("ac_couple_power_w")
        if not isinstance(baseline, (int, float)) or not isinstance(after, (int, float)):
            index += 1
            continue
        reduction = float(baseline) - float(after)
        fraction = reduction / float(baseline) if baseline else 0.0
        qualifies = (
            baseline >= cfg.minimum_baseline_w
            and reduction >= cfg.minimum_drop_w
            and fraction >= cfg.minimum_drop_fraction
        )
        if not qualifies:
            index += 1
            continue
        event_type = (
            "zero_output" if after <= cfg.zero_output_threshold_w else "partial_collapse"
        )
        plateau_limit = float(baseline) - cfg.minimum_drop_w
        plateau: list[TimedRecord] = []
        recovery_index = None
        search_end = min(len(eg4), index + cfg.maximum_search_samples + 1)
        for cursor in range(index, search_end):
            power = eg4[cursor].values.get("ac_couple_power_w")
            if not isinstance(power, (int, float)):
                break
            if power >= float(baseline) * cfg.recovery_fraction:
                recovery_index = cursor
                break
            if power <= plateau_limit:
                plateau.append(eg4[cursor])
            else:
                break
        if len(plateau) < cfg.minimum_plateau_samples or recovery_index is None:
            index += 1
            continue
        recovery = eg4[recovery_index]
        start = dropped.timestamp_utc
        end = recovery.timestamp_utc
        context_start = start.timestamp() - cfg.context_before_seconds
        context_end = end.timestamp() + cfg.context_after_seconds
        esp_window = _window(
            esp32,
            datetime.fromtimestamp(context_start, UTC),
            datetime.fromtimestamp(context_end, UTC),
        )
        solar_match = nearest_record(solar, start, cfg.solarassistant_tolerance_seconds)
        esp_match = nearest_record(esp32, start, cfg.esp32_tolerance_seconds)
        phases = {
            "before": before.timestamp_utc,
            "during": start,
            "after": recovery.timestamp_utc,
        }
        esp_summary = _esp32_summary(esp_window, cfg.supporting_frequency_change_hz)
        gaps = [
            (right.timestamp_utc - left.timestamp_utc).total_seconds()
            for left, right in zip([before, *plateau], [*plateau, recovery])
        ]
        gap_limited = any(gap > cfg.maximum_eg4_gap_seconds for gap in gaps)
        post_behavior = _post_recovery_behavior(eg4, recovery_index)
        confidence = _confidence(
            persistent_plateau=True,
            recovery=True,
            post_behavior=post_behavior,
            esp32=esp_summary,
            solar_match=solar_match,
            gap_limited=gap_limited,
        )
        plateau_powers = [float(item.values["ac_couple_power_w"]) for item in plateau]
        events.append(
            {
                "event_type": event_type,
                "target_partial_collapse": event_type == "partial_collapse",
                "event_start_utc": _iso(start),
                "pre_event_baseline_w": float(baseline),
                "plateau_representative_w": median(plateau_powers),
                "plateau_low_w": min(plateau_powers),
                "absolute_reduction_w": reduction,
                "percentage_reduction": round(fraction * 100, 3),
                "plateau_duration_seconds": (
                    plateau[-1].timestamp_utc - plateau[0].timestamp_utc
                ).total_seconds(),
                "recovery_time_utc": _iso(recovery.timestamp_utc),
                "recovery_seconds": (recovery.timestamp_utc - start).total_seconds(),
                "post_recovery_behavior": post_behavior,
                "eg4_gap_limited": gap_limited,
                "eg4_gaps_seconds": [round(gap, 3) for gap in gaps],
                "eg4_before": _safe_record(before),
                "eg4_plateau": [_safe_record(item) for item in plateau],
                "eg4_recovery": _safe_record(recovery),
                "solarassistant_context": solar_match,
                "esp32_nearest": esp_match,
                "aligned_context": {
                    "eg4_runtime": _aligned_phases(
                        eg4_context, phases, cfg.eg4_runtime_tolerance_seconds
                    ),
                    "solarassistant": _aligned_phases(
                        solar, phases, cfg.solarassistant_tolerance_seconds
                    ),
                    "esp32": _aligned_phases(
                        esp32, phases, cfg.esp32_tolerance_seconds
                    ),
                },
                "esp32_window": esp_summary,
                "confidence": confidence,
                "alternative_explanations": ["cloud_cover_or_normal_solar_variability"],
                "causation_claimed": False,
            }
        )
        index = recovery_index + 1
    return {
        "timeline": "UTC",
        "source_roles": {
            "eg4": "aggregate inverter context and EG4 SOC comparison estimate",
            "solarassistant": "trusted JK BMS battery telemetry",
            "esp32": "high-resolution supporting forensic telemetry",
        },
        "events": events,
        "event_count": len(events),
        "analysis_config": asdict(cfg),
        "interpolation_used": False,
        "causation_claimed": False,
    }
