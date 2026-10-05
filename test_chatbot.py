"""
Automated Test Suite for Rule-Based AI Chatbot
=============================================
Tests all 11 mandatory specification test cases plus robustness edge cases:
1. "hello"
2. "HELLO" (case insensitivity)
3. "  hi  " (whitespace trimming)
4. "what is your name"
5. "help"
6. "how are you"
7. "thank you"
8. "xyzabc" (fallback response)
9. "bye" (exit strategy)
10. "exit" (exit strategy)
11. "" and "   " (empty input)
12. "Hello!" and "What is your name?" (trailing punctuation resilience)
"""

import unittest
from chatbot import RuleBasedChatbot


class TestRuleBasedChatbot(unittest.TestCase):

    def setUp(self):
        self.bot = RuleBasedChatbot()

    def test_01_hello(self):
        res = self.bot.get_response("hello")
        self.assertEqual(res["matched_intent"], "greeting")
        self.assertIn("Hello!", res["response"])
        self.assertFalse(res["is_exit"])

    def test_02_hello_uppercase(self):
        res = self.bot.get_response("HELLO")
        self.assertEqual(res["matched_intent"], "greeting")
        self.assertEqual(res["sanitized_input"], "hello")
        self.assertIn("Hello!", res["response"])
        self.assertFalse(res["is_exit"])

    def test_03_hi_with_whitespace(self):
        res = self.bot.get_response("  hi  ")
        self.assertEqual(res["matched_intent"], "greeting")
        self.assertEqual(res["sanitized_input"], "hi")
        self.assertFalse(res["is_exit"])

    def test_04_what_is_your_name(self):
        res = self.bot.get_response("what is your name")
        self.assertEqual(res["matched_intent"], "name")
        self.assertIn("Rule-Based AI Chatbot", res["response"])
        self.assertFalse(res["is_exit"])

    def test_05_help(self):
        res = self.bot.get_response("help")
        self.assertEqual(res["matched_intent"], "help")
        self.assertIn("predefined commands", res["response"].lower())
        self.assertFalse(res["is_exit"])

    def test_06_how_are_you(self):
        res = self.bot.get_response("how are you")
        self.assertEqual(res["matched_intent"], "status")
        self.assertIn("doing great", res["response"].lower())
        self.assertFalse(res["is_exit"])

    def test_07_thank_you(self):
        res = self.bot.get_response("thank you")
        self.assertEqual(res["matched_intent"], "thanks")
        self.assertIn("welcome", res["response"].lower())
        self.assertFalse(res["is_exit"])

    def test_08_unknown_random_input(self):
        res = self.bot.get_response("xyzabc")
        self.assertEqual(res["matched_intent"], "fallback")
        self.assertEqual(res["response"], RuleBasedChatbot.FALLBACK_RESPONSE)
        self.assertFalse(res["is_exit"])

    def test_09_bye_exit(self):
        res = self.bot.get_response("bye")
        self.assertTrue(res["is_exit"])
        self.assertIn("Goodbye", res["response"])

    def test_10_exit_command(self):
        res = self.bot.get_response("exit")
        self.assertTrue(res["is_exit"])
        self.assertIn("Goodbye", res["response"])

    def test_11_empty_input(self):
        res_empty = self.bot.get_response("")
        self.assertEqual(res_empty["matched_intent"], "empty_input")
        self.assertFalse(res_empty["is_exit"])

        res_spaces = self.bot.get_response("     ")
        self.assertEqual(res_spaces["matched_intent"], "empty_input")
        self.assertFalse(res_spaces["is_exit"])

    def test_12_punctuation_resilience(self):
        res1 = self.bot.get_response("hello!")
        self.assertEqual(res1["matched_intent"], "greeting")

        res2 = self.bot.get_response("What is your name???")
        self.assertEqual(res2["matched_intent"], "name")

        res3 = self.bot.get_response("QUIT.")
        self.assertTrue(res3["is_exit"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
