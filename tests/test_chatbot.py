import json
import os
import unittest

from faq_chatbot import FAQChatbot


class FAQChatbotTests(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data", "faqs.json")
        self.chatbot = FAQChatbot(self.data_path)

    def test_loads_faqs(self):
        self.assertGreater(len(self.chatbot.faqs), 0)

    def test_returns_best_matching_answer(self):
        answer = self.chatbot.get_answer("How do I reset my password?")
        self.assertIn("password", answer.lower())

    def test_returns_fallback_when_no_match(self):
        answer = self.chatbot.get_answer("This is a completely unrelated question")
        self.assertIn("Sorry", answer)


if __name__ == "__main__":
    unittest.main()
