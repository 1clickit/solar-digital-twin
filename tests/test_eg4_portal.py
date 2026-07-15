import csv
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from zoneinfo import ZoneInfo

from solar_digital_twin.reporting import eg4_portal


LOCAL_TZ = ZoneInfo("America/Chicago")
NOW = datetime(2026, 7, 14, 12, 0, tzinfo=LOCAL_TZ)


class PortalFixture(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.reports_dir = Path(self.tempdir.name)
        self.reports_patch = patch.object(
            eg4_portal,
            "REPORTS_DIR",
            self.reports_dir,
        )
        self.reports_patch.start()
        self.addCleanup(self.reports_patch.stop)
        self.addCleanup(self.tempdir.cleanup)

    def write_csv(self, filename, rows, fieldnames=None):
        path = self.reports_dir / filename
        if not rows:
            path.write_text("" if fieldnames is None else ",".join(fieldnames) + "\n")
            return
        fieldnames = fieldnames or list(rows[0])
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def write_sources(
        self,
        runtime_time="2026-07-14T16:55:00+00:00",
        energy_time="2026-07-14T16:50:00+00:00",
        day_time="2026-07-14T11:45:00",
        status="Normal",
        soc="50",
        usage="4.2",
        ac_power="1200",
        load="900",
    ):
        self.write_csv(
            "runtime_snapshots.csv",
            [{
                "server_time": runtime_time,
                "status_text": status,
                "fw_code": "test-fw",
                "soc": soc,
            }],
        )
        self.write_csv(
            "energy_snapshots.csv",
            [{"server_time": energy_time, "today_usage_kwh": usage}],
        )
        self.write_csv(
            "day_multiline_samples.csv",
            [{
                "sample_time": day_time,
                "ac_couple_power_w": ac_power,
                "consumption_w": load,
            }],
        )


class SourceHealthTests(PortalFixture):
    def health(self, value, rows=True):
        data = [{"time": value}] if rows else []
        return eg4_portal.source_health(data, "time", LOCAL_TZ, NOW, 30)

    def test_all_freshness_states(self):
        self.assertEqual(self.health("2026-07-14T11:45:00").state, "Fresh")
        self.assertEqual(self.health("2026-07-14T11:00:00").state, "Stale")
        self.assertEqual(self.health("", rows=False).state, "Missing")
        self.assertEqual(self.health("not-a-time").state, "Invalid timestamp")
        self.assertEqual(self.health("2026-07-14T12:01:00").state, "Future-dated")

    def test_runtime_utc_and_day_central_semantics(self):
        runtime = eg4_portal.source_health(
            [{"time": "2026-07-14T16:55:00"}],
            "time",
            timezone.utc,
            NOW,
            30,
        )
        day = self.health("2026-07-14T11:45:00")

        self.assertEqual(runtime.timestamp_text, "2026-07-14 11:55:00 CDT")
        self.assertEqual(day.timestamp_text, "2026-07-14 11:45:00 CDT")


class PortalRenderingTests(PortalFixture):
    def test_independent_source_health_and_labels(self):
        self.write_sources()

        output = eg4_portal.build_portal(NOW)

        self.assertIn("<h2>EG4 Estimated SOC</h2>", output)
        self.assertIn(
            "Trusted Battery SOC (JK BMS via SolarAssistant) is already "
            "collected by the project but is not yet integrated into this portal",
            output,
        )
        self.assertIn("<h2>EG4 Source Health</h2>", output)
        self.assertIn("<th scope='row'>Runtime</th>", output)
        self.assertIn("<th scope='row'>Energy</th>", output)
        self.assertIn("<th scope='row'>Day Telemetry</th>", output)
        self.assertIn("2026-07-14 11:55:00 CDT", output)
        self.assertIn("2026-07-14 11:50:00 CDT", output)
        self.assertIn("2026-07-14 11:45:00 CDT", output)
        self.assertIn("<div class='value ok'>Normal</div>", output)

    def test_unknown_status_is_not_styled_as_healthy(self):
        self.write_sources(status="")

        output = eg4_portal.build_portal(NOW)

        self.assertIn("<h2>System Status</h2><div class='value warn'>n/a</div>", output)
        self.assertNotIn("<div class='value ok'>n/a</div>", output)

    def test_runtime_stale_suppresses_status_and_soc(self):
        self.write_sources(runtime_time="2026-07-14T16:00:00+00:00")

        output = eg4_portal.build_portal(NOW)

        self.assertIn("<h2>System Status</h2><div class='value warn'>n/a</div>", output)
        self.assertIn("<h2>EG4 Estimated SOC</h2>", output)
        self.assertIn("<div class='value'>n/a</div>", output)
        self.assertIn("Runtime data unavailable: Stale", output)

    def test_energy_stale_suppresses_today_usage(self):
        self.write_sources(energy_time="2026-07-14T16:00:00+00:00")

        output = eg4_portal.build_portal(NOW)

        self.assertIn("<h2>Today Usage</h2><div class='value'>n/a</div>", output)
        self.assertIn("Energy data unavailable: Stale", output)

    def test_day_stale_suppresses_ac_couple_and_load(self):
        self.write_sources(day_time="2026-07-14T11:00:00")

        output = eg4_portal.build_portal(NOW)

        self.assertEqual(output.count("Day telemetry unavailable: Stale"), 2)
        self.assertIn("<h2>AC-couple Power</h2>", output)
        self.assertIn("<h2>Load</h2>", output)

    def test_valid_zero_values_are_preserved(self):
        self.write_sources(soc="0", usage="0", ac_power="0", load="0")

        output = eg4_portal.build_portal(NOW)

        self.assertIn("0.0%", output)
        self.assertIn("0.0 kWh", output)
        self.assertEqual(output.count("0.0 W"), 2)

    def test_generation_time_is_distinct_and_html_is_escaped(self):
        self.write_sources(status="Normal <ready> & safe")

        output = eg4_portal.build_portal(NOW)

        self.assertIn("Portal generated: 2026-07-14T12:00:00-05:00", output)
        self.assertIn("Runtime observation: 2026-07-14 11:55:00 CDT", output)
        self.assertIn("Normal &lt;ready&gt; &amp; safe", output)
        self.assertNotIn("Normal <ready>", output)

    def test_missing_and_empty_csv_inputs_are_safe(self):
        missing_output = eg4_portal.build_portal(NOW)
        self.assertEqual(missing_output.count(">Missing</td>"), 3)

        self.write_csv("runtime_snapshots.csv", [], ["server_time"])
        self.write_csv("energy_snapshots.csv", [], ["server_time"])
        self.write_csv("day_multiline_samples.csv", [], ["sample_time"])
        empty_output = eg4_portal.build_portal(NOW)
        self.assertEqual(empty_output.count(">Missing</td>"), 3)

    def test_invalid_and_future_timestamps_are_visible(self):
        self.write_sources(
            runtime_time="invalid",
            energy_time="2026-07-14T17:01:00+00:00",
        )

        output = eg4_portal.build_portal(NOW)

        self.assertIn(">Invalid timestamp</td>", output)
        self.assertIn(">Future-dated</td>", output)
        self.assertIn("1.0 minutes in future", output)

    def test_cache_busting_reload_is_preserved(self):
        output = eg4_portal.build_portal(NOW)

        self.assertIn("setTimeout", output)
        self.assertIn("_refresh", output)
        self.assertIn("60000", output)


if __name__ == "__main__":
    unittest.main()
