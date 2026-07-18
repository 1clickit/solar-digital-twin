import unittest
from datetime import datetime, timezone

from solar_digital_twin.analysis.forensic_correlation import (
    CorrelationConfig,
    TimedRecord,
    analyze_correlation,
    normalize_timestamp,
)


BASE = datetime(2026, 1, 15, 18, 0, tzinfo=timezone.utc)


def record(source, seconds, timestamp_kind, **values):
    timestamp = datetime.fromtimestamp(BASE.timestamp() + seconds, timezone.utc)
    return TimedRecord.from_source(
        source,
        timestamp.isoformat().replace("+00:00", "Z"),
        timestamp_kind,
        values,
        provenance={"fixture": "synthetic"},
    )


def eg4(seconds, power, **values):
    return record(
        "eg4", seconds, "cloud_source_time", ac_couple_power_w=power, **values
    )


def solar(seconds, **values):
    return record("solarassistant", seconds, "solardt_receipt_time", **values)


def esp(seconds, **values):
    return record("esp32", seconds, "solardt_receipt_time", **values)


def clear_event():
    return [eg4(0, 5000), eg4(60, 1500), eg4(120, 1600), eg4(180, 4800)]


class ForensicCorrelationTests(unittest.TestCase):
    def test_clear_partial_event_calculations_and_source_roles(self):
        report = analyze_correlation(
            clear_event(),
            [solar(60, trusted_soc_percent=64)],
            [esp(60, frequency_hz=60.0)],
        )
        self.assertEqual(report["event_count"], 1)
        event = report["events"][0]
        self.assertEqual(event["event_type"], "partial_collapse")
        self.assertEqual(event["pre_event_baseline_w"], 5000)
        self.assertEqual(event["plateau_representative_w"], 1550)
        self.assertEqual(event["absolute_reduction_w"], 3500)
        self.assertEqual(event["percentage_reduction"], 70.0)
        self.assertEqual(event["plateau_duration_seconds"], 60)
        self.assertEqual(event["recovery_seconds"], 120)
        self.assertEqual(
            set(event["aligned_context"]["solarassistant"]),
            {"before", "during", "after"},
        )
        self.assertEqual(
            event["aligned_context"]["solarassistant"]["during"]["status"],
            "exact",
        )
        self.assertEqual(report["analysis_config"]["esp32_tolerance_seconds"], 2.0)
        self.assertFalse(event["causation_claimed"])
        self.assertIn("comparison estimate", report["source_roles"]["eg4"])
        self.assertIn("trusted", report["source_roles"]["solarassistant"])

    def test_partial_dropout_can_report_gradual_post_recovery_ramp(self):
        series = clear_event() + [eg4(240, 4900), eg4(300, 5000)]
        event = analyze_correlation(series, [], [])["events"][0]
        self.assertEqual(event["post_recovery_behavior"], "gradual_ramp")
        self.assertIn(
            "gradual_post_recovery_behavior_is_not_unique_to_dropout",
            event["confidence"]["lowering_factors"],
        )

    def test_gradual_cloud_decline_does_not_qualify(self):
        series = [eg4(0, 5000), eg4(60, 4600), eg4(120, 4100), eg4(180, 3500)]
        self.assertEqual(analyze_correlation(series, [], [])["event_count"], 0)

    def test_single_sample_dip_does_not_qualify(self):
        series = [eg4(0, 5000), eg4(60, 1500), eg4(120, 5000)]
        self.assertEqual(analyze_correlation(series, [], [])["event_count"], 0)

    def test_missing_source_context_remains_explicitly_missing(self):
        event = analyze_correlation(clear_event(), [], [])["events"][0]
        self.assertEqual(event["solarassistant_context"]["status"], "missing")
        self.assertEqual(event["solarassistant_context"]["reason"], "no_records")
        self.assertEqual(event["esp32_nearest"]["status"], "missing")
        self.assertEqual(event["esp32_window"]["records"], 0)

    def test_out_of_tolerance_records_are_not_forced_into_alignment(self):
        event = analyze_correlation(
            clear_event(), [solar(100, trusted_soc_percent=64)], [esp(65, frequency_hz=60)]
        )["events"][0]
        self.assertEqual(event["solarassistant_context"]["reason"], "out_of_tolerance")
        self.assertEqual(event["esp32_nearest"]["reason"], "out_of_tolerance")
        self.assertIsNone(event["solarassistant_context"]["record"])

    def test_timestamp_timezone_normalization_requires_explicit_zone(self):
        normalized = normalize_timestamp("2026-01-15T12:00:00", "America/Chicago")
        self.assertEqual(normalized.isoformat(), "2026-01-15T18:00:00+00:00")
        with self.assertRaisesRegex(ValueError, "explicit source timezone"):
            normalize_timestamp("2026-01-15T12:00:00")

    def test_eg4_cadence_gap_is_reported(self):
        series = [eg4(0, 5000), eg4(60, 1500), eg4(800, 1600), eg4(860, 4800)]
        event = analyze_correlation(series, [], [])["events"][0]
        self.assertTrue(event["eg4_gap_limited"])
        self.assertIn(
            "eg4_cadence_gap_limits_timing_precision",
            event["confidence"]["lowering_factors"],
        )

    def test_availability_and_frequency_context_support_candidate(self):
        context = [
            esp(50, available=True, frequency_hz=60.00),
            esp(70, available=False, frequency_hz=60.06, event="state_change"),
        ]
        event = analyze_correlation(clear_event(), [solar(60)], context)["events"][0]
        self.assertEqual(event["esp32_window"]["availability_transitions"], 1)
        self.assertTrue(event["esp32_window"]["frequency_supporting"])
        self.assertIn("state_change", event["esp32_window"]["events"])
        self.assertEqual(event["confidence"]["level"], "high")

    def test_transitions_are_per_entity_and_event_text_is_bounded(self):
        context = [
            esp(50, metric_id="binary_sensor-a", value="OFF", available=True),
            esp(51, metric_id="binary_sensor-b", value="ON", available=False),
            esp(52, metric_id="binary_sensor-a", value="ON", available=False),
            esp(53, metric_id="binary_sensor-b", value="ON", available=False),
            esp(60, metric_id="text_sensor-log", value="x", event="x" * 300),
        ]
        summary = analyze_correlation(clear_event(), [], context)["events"][0][
            "esp32_window"
        ]
        self.assertEqual(summary["availability_transitions"], 1)
        self.assertEqual(summary["state_transition_count"], 1)
        self.assertFalse(summary["state_transitions_truncated"])
        self.assertEqual(len(summary["state_transitions"]), 1)
        self.assertEqual(summary["state_transitions"][0]["metric_id"], "binary_sensor-a")
        self.assertLessEqual(len(summary["events"][0]), 160)
        self.assertTrue(
            all(
                len(change[side]) <= 160
                for change in summary["state_transitions"]
                for side in ("from", "to")
            )
        )

    def test_frequency_change_without_eg4_step_produces_no_event(self):
        steady = [eg4(0, 5000), eg4(60, 4900), eg4(120, 5000)]
        context = [esp(50, frequency_hz=59.95), esp(70, frequency_hz=60.10)]
        self.assertEqual(analyze_correlation(steady, [], context)["event_count"], 0)

    def test_no_event_control_window(self):
        steady = [eg4(0, 2000), eg4(60, 2050), eg4(120, 1980), eg4(180, 2010)]
        report = analyze_correlation(steady, [solar(60)], [esp(60)])
        self.assertEqual(report["events"], [])
        self.assertFalse(report["interpolation_used"])

    def test_eg4_estimated_soc_and_trusted_soc_stay_separate(self):
        series = [
            eg4(0, 5000, estimated_soc_percent=59),
            eg4(60, 1500, estimated_soc_percent=58),
            eg4(120, 1600, estimated_soc_percent=58),
            eg4(180, 4800, estimated_soc_percent=57),
        ]
        event = analyze_correlation(
            series, [solar(60, trusted_soc_percent=64)], [esp(60)]
        )["events"][0]
        self.assertEqual(event["eg4_before"]["values"]["estimated_soc_percent"], 59)
        self.assertEqual(
            event["solarassistant_context"]["record"]["values"]["trusted_soc_percent"],
            64,
        )

    def test_zero_output_is_distinct_from_target_partial_plateau(self):
        series = [eg4(0, 5000), eg4(60, 0), eg4(120, 0), eg4(180, 4800)]
        event = analyze_correlation(series, [], [])["events"][0]
        self.assertEqual(event["event_type"], "zero_output")
        self.assertFalse(event["target_partial_collapse"])

    def test_later_zero_in_plateau_is_classified_as_zero_output(self):
        series = [eg4(0, 5000), eg4(60, 1000), eg4(120, 0), eg4(180, 4800)]
        event = analyze_correlation(series, [], [])["events"][0]
        self.assertEqual(event["event_type"], "zero_output")
        self.assertFalse(event["target_partial_collapse"])

    def test_nearest_event_log_record_is_bounded(self):
        context = [
            esp(
                60,
                metric_id="text_sensor-04_forensic_event_log",
                value="x" * 300,
                event="x" * 300,
            )
        ]
        nearest = analyze_correlation(clear_event(), [], context)["events"][0][
            "esp32_nearest"
        ]["record"]
        self.assertLessEqual(len(nearest["values"]["value"]), 160)
        self.assertLessEqual(len(nearest["values"]["event"]), 160)

    def test_multiple_candidates_are_detected(self):
        series = clear_event() + [
            eg4(240, 5000),
            eg4(300, 1400),
            eg4(360, 1500),
            eg4(420, 4900),
        ]
        self.assertEqual(analyze_correlation(series, [], [])["event_count"], 2)

    def test_unsorted_inputs_are_normalized_deterministically(self):
        sorted_report = analyze_correlation(clear_event(), [], [])
        unsorted_report = analyze_correlation(list(reversed(clear_event())), [], [])
        self.assertEqual(sorted_report, unsorted_report)

    def test_analysis_does_not_modify_inputs(self):
        source = clear_event()
        original = list(source)
        analyze_correlation(source, [], [])
        self.assertEqual(source, original)

    def test_reduced_esp32_stream_preserves_equivalent_key_event_context(self):
        raw = [
            esp(50, available=True, frequency_hz=60.00),
            esp(55, available=True, frequency_hz=60.00),
            esp(60, available=False, frequency_hz=60.06, event="transition"),
            esp(65, available=False, frequency_hz=60.06),
        ]
        reduced = [raw[0], raw[2], raw[3]]
        raw_event = analyze_correlation(clear_event(), [], raw)["events"][0]
        reduced_event = analyze_correlation(clear_event(), [], reduced)["events"][0]
        for key in ("frequency_change_hz", "frequency_supporting", "events", "availability_transitions"):
            self.assertEqual(raw_event["esp32_window"][key], reduced_event["esp32_window"][key])


if __name__ == "__main__":
    unittest.main()
