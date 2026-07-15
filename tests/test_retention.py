import unittest

from solar_digital_twin.collectors.retention import (
    FrequencyRetentionPolicy,
    meaningful_change,
    retention_reason,
)


class FrequencyRetentionPolicyTests(unittest.TestCase):
    def test_first_numeric_value_and_deadband_changes_are_retained(self):
        policy = FrequencyRetentionPolicy()

        self.assertTrue(policy.should_retain(60.00, 100.0))
        self.assertFalse(policy.should_retain(60.03, 101.0))
        self.assertTrue(policy.should_retain(60.04, 102.0))
        self.assertFalse(policy.should_retain(60.01, 103.0))
        self.assertTrue(policy.should_retain(60.00, 104.0))

    def test_heartbeat_uses_elapsed_monotonic_time(self):
        policy = FrequencyRetentionPolicy()

        self.assertTrue(policy.should_retain("60.00", 500.0))
        self.assertFalse(policy.should_retain("60.00", 529.9))
        self.assertTrue(policy.should_retain("60.00", 530.0))

    def test_invalid_values_do_not_retain_or_change_state(self):
        policy = FrequencyRetentionPolicy()

        for value in (None, "unknown", "nan", float("inf"), True):
            self.assertFalse(policy.should_retain(value, 10.0))

        self.assertTrue(policy.should_retain(60.00, 11.0))

    def test_change_is_compared_with_last_retained_value(self):
        policy = FrequencyRetentionPolicy()

        self.assertTrue(policy.should_retain(60.00, 0.0))
        self.assertFalse(policy.should_retain(60.03, 1.0))
        self.assertTrue(policy.should_retain(60.04, 2.0))


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


class RetentionReasonTests(unittest.TestCase):
    def test_meaningful_change_takes_priority(self):
        self.assertEqual(
            retention_reason(60.00, 60.04, 0.04, 30, 30),
            "change",
        )

    def test_heartbeat_retains_unchanged_value(self):
        self.assertEqual(
            retention_reason(60.00, 60.00, 0.04, 30, 30),
            "heartbeat",
        )

    def test_unchanged_value_before_heartbeat_is_not_retained(self):
        self.assertIsNone(
            retention_reason(60.00, 60.00, 0.04, 29.9, 30)
        )

if __name__ == "__main__":
    unittest.main()
