import unittest

from solar_digital_twin.collectors.retention import meaningful_change


class MeaningfulChangeTests(unittest.TestCase):
    def test_frequency_deadband_both_directions(self):
        self.assertFalse(meaningful_change(60.00, 60.03, 0.04))
        self.assertTrue(meaningful_change(60.00, 60.04, 0.04))
        self.assertFalse(meaningful_change(60.00, 59.97, 0.04))
        self.assertTrue(meaningful_change(60.00, 59.96, 0.04))

    def test_first_and_unchanged_values(self):
        self.assertTrue(meaningful_change(None, 60.00, 0.04))
        self.assertFalse(meaningful_change(60.00, 60.00, 0.04))

    def test_text_transitions(self):
        self.assertTrue(meaningful_change("On", "Off"))
        self.assertFalse(meaningful_change("On", "On"))

    def test_negative_deadband_rejected(self):
        with self.assertRaises(ValueError):
            meaningful_change(60.00, 60.01, -0.04)


class HeartbeatDueTests(unittest.TestCase):
    def test_heartbeat_boundary(self):
        from solar_digital_twin.collectors.retention import heartbeat_due

        self.assertFalse(heartbeat_due(29.9, 30))
        self.assertTrue(heartbeat_due(30, 30))
        self.assertTrue(heartbeat_due(31, 30))

    def test_first_retention_is_due(self):
        from solar_digital_twin.collectors.retention import heartbeat_due

        self.assertTrue(heartbeat_due(None, 30))

    def test_invalid_intervals_rejected(self):
        from solar_digital_twin.collectors.retention import heartbeat_due

        with self.assertRaises(ValueError):
            heartbeat_due(10, 0)
        with self.assertRaises(ValueError):
            heartbeat_due(-1, 30)

if __name__ == "__main__":
    unittest.main()
