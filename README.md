# FAQ Chatbot

A simple FAQ chatbot built with Python, scikit-learn, and Flask. It preprocesses FAQ questions, matches a user query against the most relevant FAQ using TF-IDF and cosine similarity, and returns the best matching answer.

## Features
- Loads FAQs from a JSON file
- Preprocesses text for matching
- Uses TF-IDF vectorization and cosine similarity
- Provides a simple web chat interface
- Includes basic unit tests

## Project Structure
- `faq_chatbot.py` — core chatbot logic and FAQ matching
- `app.py` — Flask web app for interactive chat
- `data/faqs.json` — sample FAQ dataset
- `tests/test_chatbot.py` — basic tests for matching and fallback behavior

## Requirements
Install the required packages:

```bash
pip install flask scikit-learn
```

## Run Locally
1. Navigate to the project folder
2. Start the Flask app:

```bash
python app.py
```

3. Open your browser and go to:

```text
http://127.0.0.1:5000/
```

## Example
Try asking questions such as:
- How do I reset my password?
- What is your refund policy?
- How do I contact support?

## Testing
Run the tests with:

```bash
python -m unittest discover -s tests -v
```

## Notes
This project is intended as a beginner-friendly FAQ chatbot example and can be extended with more FAQs, better NLP preprocessing, or a more polished UI.
