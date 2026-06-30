import json
import os
import re
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "how", "i", "in", "is", "it", "its", "of", "on", "or", "our", "that",
    "the", "their", "this", "to", "was", "what", "when", "where", "which",
    "who", "will", "with", "you", "your"
}


class FAQChatbot:
    def __init__(self, faq_path: str):
        self.faq_path = faq_path
        self.faqs = self._load_faqs()
        self.vectorizer = TfidfVectorizer()
        self._prepare_corpus()

    def _load_faqs(self) -> List[Dict[str, str]]:
        with open(self.faq_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data.get("faqs", [])

    def _prepare_corpus(self):
        self.questions = [self._normalize_text(item["question"]) for item in self.faqs]
        self.answers = [item["answer"] for item in self.faqs]
        self.matrix = self.vectorizer.fit_transform(self.questions)

    def _normalize_text(self, text: str) -> str:
        text = text.lower()
        tokens = re.findall(r"[a-z0-9]+", text)
        tokens = [token for token in tokens if token not in STOP_WORDS]
        return " ".join(tokens)

    def get_answer(self, user_question: str) -> str:
        if not self.faqs:
            return "Sorry, no FAQs are available yet."

        normalized_question = self._normalize_text(user_question)
        query_vector = self.vectorizer.transform([normalized_question])
        similarity_scores = cosine_similarity(query_vector, self.matrix).flatten()
        best_match_index = similarity_scores.argmax()

        if similarity_scores[best_match_index] < 0.1:
            return "Sorry, I could not find a relevant answer. Please try a different question."

        return self.answers[best_match_index]


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    chatbot = FAQChatbot(os.path.join(base_dir, "data", "faqs.json"))
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break
        print("Bot:", chatbot.get_answer(user_input))
