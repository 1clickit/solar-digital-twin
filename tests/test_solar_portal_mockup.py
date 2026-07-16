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
        for panel_id in ("panel-trends", "panel-forensics", "panel-sources"):
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
        self.assertIn("ΔV 0.05 V", self.html)
        self.assertIn("Average DC", self.html)
        self.assertIn("+3.3 kW", self.html)
        self.assertIn("AC amps net", self.html)

    def test_battery_current_comparison_replaces_combined_bank_card(self):
        self.assertEqual(1, self.html.count('data-ring="battery-current-comparison"'))
        self.assertIn("B1 +25.8 A DC", self.html)
        self.assertIn("B2 +25.3 A DC", self.html)
        self.assertIn("Positive = charging", self.html)
        self.assertIn("negative = discharging", self.html)
        self.assertIn("2.8 kW DC", self.html)
        self.assertNotIn("270", self.html)
        self.assertNotIn("° zero", self.html)
        self.assertNotIn("<h3>Battery bank power</h3>", self.html)
        self.assertNotIn('data-ring="battery-bipolar"', self.html)
        self.assertNotIn("<h3>Combined bank</h3>", self.html)

    def test_battery_current_is_in_top_operational_row(self):
        operations = self.html.split('class="operations-grid"', 1)[1].split("</section>", 1)[0]
        battery_section = self.html.split('class="battery-grid"', 1)[1].split("</section>", 1)[0]
        self.assertIn('data-ring="battery-current-comparison"', operations)
        self.assertNotIn('data-ring="battery-current-comparison"', battery_section)
        self.assertLess(operations.index("Battery current comparison"), operations.index("Current AC source"))
        self.assertIn('data-ring="soc-comparison"', battery_section)
        self.assertIn('data-ring="voltage-comparison"', battery_section)

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
        self.assertIn("AC amps", self.html)
        self.assertIn("A DC", self.html)
        self.assertIn("Synthetic measured", self.html)
        self.assertIn("Synthetic calculated", self.html)

    def test_major_widgets_have_accessible_labels(self):
        self.assertGreaterEqual(len(self.parser.aria_labels), 18)
        for concept in ("system health", "Solar and house load", "Battery current comparison", "Combined SOC", "Combined battery voltage", "Current AC source"):
            with self.subTest(concept=concept):
                self.assertTrue(any(concept.lower() in label.lower() for label in self.parser.aria_labels))


if __name__ == "__main__":
    unittest.main()
