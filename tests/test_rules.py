import unittest
from services.rules import has_generic_ai_phrase, evaluate_behavioral_flags

class TestRules(unittest.TestCase):
    def test_ai_phrase_detection(self):
        self.assertTrue(has_generic_ai_phrase("As an AI language model, I cannot..."))
        self.assertFalse(has_generic_ai_phrase("I am a software engineer with 5 years experience."))

    def test_flag_evaluation(self):
        flags = ["lip_sync_error", "unnatural_blink"]
        penalty, reasons = evaluate_behavioral_flags(flags)
        # 18 (critical) + 8 (warning) = 26
        self.assertEqual(penalty, 26)
        self.assertEqual(len(reasons), 2)
        self.assertIn("Critical observation: Lip Sync Error", reasons)
        self.assertIn("Behavioral warning: Unnatural Blink", reasons)

if __name__ == "__main__":
    unittest.main()
