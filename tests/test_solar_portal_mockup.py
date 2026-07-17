from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MOCKUP = ROOT / "prototypes" / "solar_portal_mockup.html"
DESIGN = ROOT / "docs" / "PORTAL_UI_DESIGN.md"


class _ResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.external_resources = []
        self.aria_labels = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "aria-label" in attributes:
            self.aria_labels.append(attributes["aria-label"])
        resource_attributes = {
            "script": "src",
            "link": "href",
            "img": "src",
            "iframe": "src",
            "source": "src",
        }
        attribute = resource_attributes.get(tag)
        if attribute and attributes.get(attribute):
            self.external_resources.append((tag, attributes[attribute]))


class SolarPortalMockupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = MOCKUP.read_text(encoding="utf-8")
        cls.design = DESIGN.read_text(encoding="utf-8")
        cls.parser = _ResourceParser()
        cls.parser.feed(cls.html)

    def test_visible_synthetic_notice_exists(self):
        self.assertIn("Synthetic UI Prototype — Not Live Data", self.html)

    def test_has_no_external_resources_or_network_urls(self):
        self.assertEqual([], self.parser.external_resources)
        self.assertIsNone(re.search(r"(?:https?:)?//", self.html, re.IGNORECASE))
        self.assertNotRegex(self.html, r"@import\s")
        self.assertNotRegex(self.html, r"url\s*\(")

    def test_has_no_browser_data_access_api(self):
        for forbidden in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.html)

    def test_accessible_tab_controls_and_panels_exist(self):
        tabs = (
            ("tab-overview", "panel-overview", "true"),
            ("tab-trends", "panel-trends", "false"),
            ("tab-forensics", "panel-forensics", "false"),
            ("tab-sources", "panel-sources", "false"),
            ("tab-eg4", "panel-eg4", "false"),
            ("tab-sa", "panel-sa", "false"),
            ("tab-esp32", "panel-esp32", "false"),
            ("tab-volcast", "panel-volcast", "false"),
        )
        for tab_id, panel_id, selected in tabs:
            with self.subTest(tab=tab_id):
                self.assertRegex(
                    self.html,
                    rf'<button[^>]+id="{tab_id}"[^>]+role="tab"[^>]+aria-selected="{selected}"[^>]+aria-controls="{panel_id}"',
                )
                self.assertRegex(
                    self.html,
                    rf'<section[^>]+id="{panel_id}"[^>]+role="tabpanel"[^>]+aria-labelledby="{tab_id}"',
                )
        self.assertIn('role="tablist"', self.html)
        self.assertRegex(self.html, r'id="panel-overview" role="tabpanel" aria-labelledby="tab-overview">')
        for panel_id in ("panel-trends", "panel-forensics", "panel-sources", "panel-eg4", "panel-sa", "panel-esp32", "panel-volcast"):
            self.assertRegex(self.html, rf'id="{panel_id}" role="tabpanel"[^>]+ hidden>')

    def test_context_content_is_in_its_named_tab_panel(self):
        overview = self.html.split('id="panel-overview"', 1)[1].split('id="panel-trends"', 1)[0]
        trends = self.html.split('id="panel-trends"', 1)[1].split('id="panel-forensics"', 1)[0]
        forensics = self.html.split('id="panel-forensics"', 1)[1].split('id="panel-sources"', 1)[0]
        sources = self.html.split('id="panel-sources"', 1)[1].split("<footer>", 1)[0]
        for moved_content in ("Recent trends", "Latest forensic notice", "Source health", "Evidence traceability"):
            self.assertNotIn(moved_content, overview)
        self.assertIn("Recent trends", trends)
        self.assertIn("Latest forensic notice", forensics)
        self.assertIn("Source health", sources)
        self.assertIn("Evidence traceability", sources)

    def test_theme_and_scale_variables_are_centralized(self):
        for variable in (
            "--battery-charging",
            "--battery-discharging",
            "--solar-input",
            "--grid-export",
            "--house-load",
            "--trusted-soc",
            "--estimated-soc",
            "--battery-one",
            "--battery-two",
            "--neutral-track",
            "--state-healthy",
            "--state-warning",
            "--state-stale",
            "--state-unavailable",
            "--panel-bg",
            "--text",
            "--muted",
            "--ring-size",
            "--ring-stroke",
            "--ring-radius",
        ):
            with self.subTest(variable=variable):
                self.assertIn(variable, self.html)

    def test_bipolar_current_ring_structure_exists(self):
        self.assertEqual(1, self.html.count('data-ring="battery-current-comparison"'))
        self.assertEqual(2, len(re.findall(r'class="[^"]*\bupper-track\b[^"]*"', self.html)))
        self.assertEqual(2, len(re.findall(r'class="[^"]*\blower-track\b[^"]*"', self.html)))
        self.assertGreaterEqual(self.html.count("current-upper"), 3)
        self.assertGreaterEqual(self.html.count("current-lower"), 3)

    def test_combined_comparison_ring_structures_exist(self):
        for ring in ("soc-comparison", "voltage-comparison", "solar-load-comparison"):
            with self.subTest(ring=ring):
                self.assertEqual(1, self.html.count(f'data-ring="{ring}"'))
        self.assertIn("EG4 +5 pts", self.html)
        self.assertIn("comparison only", self.html)
        self.assertNotIn("ΔV 0.05 V", self.html)
        self.assertNotIn("Average DC", self.html)
        self.assertIn("13.8 A", self.html)
        self.assertIn("240.1 V", self.html)
        solar_card = self.html.split('class="panel solar-card"', 1)[1].split("</article>", 1)[0]
        solar_text = " ".join(re.sub(r"<[^>]+>", " ", solar_card).split())
        self.assertIn("3.3 kW 13.8 A 240.1 V", solar_text)
        self.assertNotIn("+3.3", solar_card)
        self.assertIn("solar-range", solar_card)
        self.assertIn("load-range", solar_card)
        self.assertGreaterEqual(solar_card.count("range-mark"), 4)
        self.assertNotIn("AC amps net", self.html)
        self.assertNotIn("Grid return/export: 0.0 kW", self.html)
        self.assertNotIn("ESP32 1s · Synthetic measured solar", self.html)
        self.assertNotIn("Synthetic calculated load", self.html)

    def test_battery_current_comparison_replaces_combined_bank_card(self):
        current_card = self.html.split('data-ring="battery-current-comparison"', 1)[1].split("</article>", 1)[0]
        self.assertEqual(1, self.html.count('data-ring="battery-current-comparison"'))
        self.assertIn("B1 25.8 A", self.html)
        self.assertIn("B2 25.3 A", self.html)
        self.assertNotIn("2.8 kW DC", self.html)
        self.assertIn("54.8 V", self.html)
        self.assertNotIn("Net charging", self.html)
        self.assertNotIn("270", current_card)
        self.assertNotIn("° zero", self.html)
        self.assertNotIn("<h3>Battery bank power</h3>", self.html)
        self.assertNotIn('data-ring="battery-bipolar"', self.html)
        self.assertNotIn("<h3>Combined bank</h3>", self.html)

    def test_approved_overview_card_order_and_battery_row(self):
        operations = self.html.split('class="operations-grid"', 1)[1].split("</section>", 1)[0]
        battery_section = self.html.split('class="battery-grid"', 1)[1].split("</section>", 1)[0]
        headings = ("Solar vs house load", "Volcast forecast", "System health", "Current AC source")
        positions = [operations.index(heading) for heading in headings]
        self.assertEqual(sorted(positions), positions)
        self.assertNotIn('data-ring="battery-current-comparison"', operations)
        self.assertIn('data-ring="battery-current-comparison"', battery_section)
        self.assertIn('data-ring="soc-comparison"', battery_section)
        self.assertIn('data-ring="voltage-comparison"', battery_section)
        battery_positions = [
            battery_section.index("Battery SOC"),
            battery_section.index("Battery voltage"),
            battery_section.index("Battery current"),
            battery_section.index("Battery cell voltage"),
        ]
        self.assertEqual(sorted(battery_positions), battery_positions)
        for obsolete_title in ("Battery SOC comparison", "Battery voltage comparison", "Battery current comparison"):
            self.assertNotIn(f"<h3>{obsolete_title}</h3>", battery_section)

    def test_compact_scrollable_volcast_forecast(self):
        self.assertIn('class="panel volcast-card"', self.html)
        self.assertIn('class="forecast-scroll"', self.html)
        self.assertRegex(self.html, r"\.forecast-scroll\s*\{[^}]*overflow-y:\s*scroll")
        self.assertIn("Favorable solar day expected", self.html)
        self.assertIn("26.8 kWh", self.html)
        self.assertIn("Expected today · forecast, not measured", self.html)
        self.assertIn("Hourly forecast", self.html)
        self.assertIn("Last update - Thursday - 07-16-2026 - 17:56", self.html)
        self.assertNotIn("Future: 30-minute server refresh", self.html)

    def test_compact_operation_cards_and_current_state_styles(self):
        self.assertRegex(self.html, r"\.operations-grid\s*>\s*\.panel\s*\{[^}]*height:\s*19rem")
        self.assertIn('data-current-state="positive"', self.html)
        for state in ("positive", "negative", "neutral"):
            with self.subTest(state=state):
                self.assertIn(f"current-{state}", self.html)
                self.assertIn(f'data-current-state="{state}"]', self.html)
        current_card = self.html.split('data-ring="battery-current-comparison"', 1)[1].split("</article>", 1)[0]
        current_text = " ".join(re.sub(r"<[^>]+>", " ", current_card).split())
        self.assertIn("51.1 A 54.8 V", current_text)
        self.assertNotIn("+51.1", current_card)
        self.assertIn("negative values use accounting style, for example (3000)", current_card)

    def test_battery_voltage_and_cell_voltage_cleanup(self):
        voltage_card = self.html.split('data-ring="voltage-comparison"', 1)[1].split("</article>", 1)[0]
        voltage_text = " ".join(re.sub(r"<[^>]+>", " ", voltage_card).split())
        self.assertIn("54.80 VDC", voltage_text)
        self.assertNotIn("Average", voltage_card)
        self.assertNotIn("ΔV", voltage_card)
        cell_card = self.html.split("<h3>Battery cell voltage</h3>", 1)[1].split("</article>", 1)[0]
        for value in ("Battery 1", "MIN <b data-readout=\"minimum\">3.420", "AVG <b data-readout=\"average\">3.426", "MAX <b data-readout=\"maximum\">3.433", "Battery 2", "MIN <b data-readout=\"minimum\">3.417", "AVG <b data-readout=\"average\">3.423", "MAX <b data-readout=\"maximum\">3.430"):
            self.assertIn(value, cell_card)

    def test_cell_voltage_fixed_scale_values_and_states(self):
        cell_card = self.html.split("<h3>Battery cell voltage</h3>", 1)[1].split("</article>", 1)[0]
        self.assertEqual(2, cell_card.count('data-low-limit="2.50"'))
        self.assertEqual(2, cell_card.count('data-high-limit="3.65"'))
        self.assertEqual(2, cell_card.count('data-low-position="5-o\'clock"'))
        self.assertEqual(2, cell_card.count('data-high-position="2-o\'clock"'))
        self.assertEqual(2, cell_card.count('data-direction="clockwise-long-arc"'))
        self.assertEqual(2, cell_card.count("cell-cutoff-marker"))
        self.assertEqual(2, cell_card.count("cell-upper-marker"))
        self.assertNotIn("%", cell_card)
        battery_1 = cell_card.split("<strong>Battery 1</strong>", 1)[1].split("<strong>Battery 2</strong>", 1)[0]
        battery_2 = cell_card.split("<strong>Battery 2</strong>", 1)[1]
        for battery, values in (
            (battery_1, ("MIN <b", "AVG <b", "MAX <b")),
            (battery_2, ("MIN <b", "AVG <b", "MAX <b")),
        ):
            positions = [battery.index(value) for value in values]
            self.assertEqual(sorted(positions), positions)
            self.assertIn('DIFF <span data-readout="differential">—</span> mV', battery)
        self.assertNotIn("13 mV Differential", cell_card)
        for state in ("normal", "under-voltage", "over-voltage", "under-over-voltage"):
            self.assertIn(f"'{state}'", self.html)
        self.assertEqual(2, cell_card.count('data-clamp-policy="endpoint-only; preserve numeric value"'))
        self.assertIn("alarm banners retain exact live values", cell_card)
        self.assertNotIn("data-imbalance-threshold", self.html)

    def test_cell_voltage_size_typography_and_alarm_banners(self):
        cell_card = self.html.split("<h3>Battery cell voltage</h3>", 1)[1].split("</article>", 1)[0]
        self.assertRegex(self.html, r"\.cell-dial\s*\{[^}]*10\.5rem")
        self.assertRegex(self.html, r"\.cell-readout-values\s*\{[^}]*font-size:\s*\.58rem")
        self.assertRegex(self.html, r"\.cell-readout-values \.cell-readout-average\s*\{[^}]*color:\s*var\(--text\)[^}]*font-weight:\s*800")
        self.assertIn("cell-normal-range", cell_card)
        self.assertIn("cell-caution-low", cell_card)
        self.assertIn("cell-caution-high", cell_card)
        self.assertNotIn("cell-alarm-low", cell_card)
        self.assertNotIn("cell-alarm-high", cell_card)
        self.assertIn("UNDER VOLTAGE <span id=\"b1-under-voltage\" data-live-value=\"minimum\">2.43 V", cell_card)
        self.assertIn("OVER VOLTAGE <span id=\"b1-over-voltage\" data-live-value=\"maximum\">3.71 V", cell_card)
        self.assertIn("UNDER VOLTAGE <span id=\"b2-under-voltage\" data-live-value=\"minimum\">2.43 V", cell_card)
        self.assertIn("OVER VOLTAGE <span id=\"b2-over-voltage\" data-live-value=\"maximum\">3.71 V", cell_card)
        self.assertRegex(self.html, r'data-state="under-voltage"[^}]*\.cell-readout|data-state="under-voltage"\] \.cell-readout')
        self.assertIn('data-state="under-over-voltage"] .cell-alarm-stack', self.html)
        self.assertEqual(2, cell_card.count('aria-live="polite"'))

    def test_cell_voltage_open_arc_and_endpoint_stops(self):
        cell_card = self.html.split("<h3>Battery cell voltage</h3>", 1)[1].split("</article>", 1)[0]
        self.assertRegex(self.html, r"\.cell-scale-track\s*\{[^}]*stroke-dasharray:\s*75 25[^}]*stroke-dashoffset:\s*-41\.67")
        self.assertEqual(2, cell_card.count('transform="rotate(150 80 80)"'))
        self.assertEqual(2, cell_card.count('transform="rotate(60 80 80)"'))
        self.assertRegex(self.html, r"\.cell-cutoff-marker, \.cell-upper-marker\s*\{[^}]*var\(--battery-discharging\)")
        self.assertRegex(self.html, r"\.cell-caution-low\s*\{[^}]*stroke-dasharray:\s*10 90")
        self.assertRegex(self.html, r"\.cell-caution-high\s*\{[^}]*stroke-dasharray:\s*10 90")
        self.assertRegex(self.html, r"\.cell-normal-range\s*\{[^}]*stroke:\s*var\(--state-healthy\)[^}]*stroke-dasharray:\s*55 45")
        self.assertIn("const clamp =", self.html)
        self.assertIn("cellVoltageAngle(value, low, high)", self.html)
        self.assertIn("Low limit 2.50 V · High limit 3.65 V", cell_card)
        self.assertNotIn("2.00–3.80 V", cell_card)

    def test_cell_voltage_markers_share_scale_and_overlap_naturally(self):
        cell_card = self.html.split("<h3>Battery cell voltage</h3>", 1)[1].split("</article>", 1)[0]
        self.assertNotIn("cell-average-arc", self.html)
        for marker in ("minimum", "average", "maximum"):
            self.assertEqual(2, cell_card.count(f'data-marker="{marker}"'))
        self.assertIn("const CELL_START_ANGLE = 150", self.html)
        self.assertIn("const CELL_ARC_DEGREES = 270", self.html)
        self.assertEqual(1, self.html.count("const cellVoltageAngle"))
        self.assertNotIn("angular-offset", self.html)
        self.assertRegex(self.html, r"\.cell-min-marker\s*\{[^}]*var\(--grid-export\)")
        self.assertRegex(self.html, r"\.cell-average-marker\s*\{[^}]*var\(--text\)")
        self.assertRegex(self.html, r"\.cell-max-marker\s*\{[^}]*var\(--battery-discharging\)")
        self.assertRegex(self.html, r"\.cell-alarm-banner\s*\{[^}]*font-size:\s*\.72rem[^}]*font-weight:\s*900")

        def angle(value):
            return 150 + ((value - 2.50) / (3.65 - 2.50)) * 270

        close_spread = angle(3.433) - angle(3.420)
        wider_spread = angle(3.55) - angle(3.20)
        self.assertLess(close_spread, 4)
        self.assertGreater(wider_spread, close_spread)

    def test_cell_voltage_readout_and_differential_are_calculated(self):
        cell_card = self.html.split("<h3>Battery cell voltage</h3>", 1)[1].split("</article>", 1)[0]
        self.assertIn("Math.round((values.maximum - values.minimum) * 1000)", self.html)
        self.assertNotIn(">13</span> mV", cell_card)
        samples = re.findall(
            r'data-minimum="([0-9.]+)" data-average="([0-9.]+)" data-maximum="([0-9.]+)"',
            cell_card,
        )
        self.assertEqual(2, len(samples))
        for minimum, _average, maximum in samples:
            self.assertEqual(13, round((float(maximum) - float(minimum)) * 1000))
        changed_minimum = float(samples[0][0]) - 0.005
        self.assertEqual(18, round((float(samples[0][2]) - changed_minimum) * 1000))

    def test_cell_voltage_alarm_values_and_clamping_remain_independent(self):
        cell_card = self.html.split("<h3>Battery cell voltage</h3>", 1)[1].split("</article>", 1)[0]
        self.assertIn("clamp(value, low, high)", self.html)
        self.assertIn("values.minimum < low", self.html)
        self.assertIn("values.maximum > high", self.html)
        self.assertIn("under && over ? 'under-over-voltage'", self.html)
        for battery in ("b1", "b2"):
            self.assertIn(f'id="{battery}-under-voltage" data-live-value="minimum">2.43 V', cell_card)
            self.assertIn(f'id="{battery}-over-voltage" data-live-value="maximum">3.71 V', cell_card)
        self.assertIn("values.minimum.toFixed(2)", self.html)
        self.assertIn("values.maximum.toFixed(2)", self.html)

    def test_homepage_dial_provenance_footers_are_removed(self):
        overview = self.html.split('id="panel-overview"', 1)[1].split('id="panel-trends"', 1)[0]
        for removed in (
            "SolarAssistant 4s · EG4 8m · no averaging or correction",
            "Synthetic measured values · average calculated",
            "SolarAssistant / JK BMS · 4s old · Synthetic measured",
            "48–58 V DC display range · JK BMS · 4s old",
        ):
            self.assertNotIn(removed, overview)

    def test_source_tabs_and_synthetic_catalog_panels(self):
        navigation = self.html.split('role="tablist"', 1)[1].split("</nav>", 1)[0]
        labels = (">EG4</button>", ">SA</button>", ">ESP32</button>", ">Volcast</button>")
        positions = [navigation.index(label) for label in labels]
        self.assertEqual(sorted(positions), positions)
        self.assertIn('class="tab-divider"', navigation)
        panels = {
            "panel-eg4": "<h2>EG4</h2>",
            "panel-sa": "<h2>SolarAssistant</h2>",
            "panel-esp32": "<h2>ESP32</h2>",
            "panel-volcast": "<h2>Volcast</h2>",
        }
        for panel_id, heading in panels.items():
            with self.subTest(panel=panel_id):
                panel = self.html.split(f'id="{panel_id}"', 1)[1].split("</section>", 1)[0]
                self.assertIn(heading, panel)
                self.assertIn("Synthetic layout preview", panel)
                self.assertIn("Production Show all will expose every parsed, non-secret, read-only parameter", panel)
                self.assertIn('type="search"', panel)
                self.assertIn("Show changed", panel)
                self.assertIn("Show unavailable", panel)
        volcast = self.html.split('id="panel-volcast"', 1)[1].split("</section>", 1)[0]
        for grouping in ("Daily forecast", "Hourly forecast", "Five-minute forecast", "all parsed five-minute entries"):
            self.assertIn(grouping, volcast)

    def test_future_device_navigation_and_history_are_documented(self):
        design = " ".join(self.design.split())
        for term in (
            "`EG4`",
            "`SolarAssistant`",
            "`ESP32`",
            "stable metric identifier",
            "clickable to open its history",
            "time-range selection",
            "side drawer",
            "dedicated parameter page or URL",
        ):
            with self.subTest(term=term):
                self.assertIn(term, design)

    def test_device_tab_completeness_boundary_is_documented(self):
        design = " ".join(self.design.split())
        for requirement in (
            "Overview is curated; device tabs are complete.",
            "every available parsed, non-secret, read-only parameter",
            "null, unavailable, stale, unsupported, and unknown values",
            "must not silently omit parameters from a true `Show all` view",
            "passwords, tokens, API keys, encryption keys, credentials",
            "Writable controls and device actions must not be mixed into the read-only telemetry view",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, design)

    def test_electrical_labels_identify_ac_and_dc_amps(self):
        self.assertIn("13.8 A", self.html)
        self.assertIn("A DC", self.html)
        self.assertIn("Synthetic measured", self.html)
        self.assertIn("Synthetic calculated", self.html)

    def test_major_widgets_have_accessible_labels(self):
        self.assertGreaterEqual(len(self.parser.aria_labels), 18)
        for concept in ("system health", "Solar and house load", "Battery current", "Battery SOC", "Battery voltage", "Battery cell voltage", "Current AC source"):
            with self.subTest(concept=concept):
                self.assertTrue(any(concept.lower() in label.lower() for label in self.parser.aria_labels))


if __name__ == "__main__":
    unittest.main()
