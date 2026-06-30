import os
from flask import Flask, render_template_string, request
from faq_chatbot import FAQChatbot

app = Flask(__name__)
base_dir = os.path.dirname(__file__)
chatbot = FAQChatbot(os.path.join(base_dir, "data", "faqs.json"))

HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>FAQ Chatbot</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; }
      .messages { border: 1px solid #ddd; padding: 15px; border-radius: 8px; min-height: 250px; margin-bottom: 15px; }
      .user { color: #0b5fff; } .bot { color: #1a7f37; }
      form { display: flex; gap: 10px; }
      input[type=text] { flex: 1; padding: 10px; }
      button { padding: 10px 15px; }
    </style>
  </head>
  <body>
    <h2>FAQ Chatbot</h2>
    <div class="messages">
      {% for message in messages %}
        <p><strong class="{{ message['role'] }}">{{ message['role']|capitalize }}:</strong> {{ message['text'] }}</p>
      {% endfor %}
    </div>
    <form method="post">
      <input type="text" name="question" placeholder="Ask a question about the product" autofocus>
      <button type="submit">Send</button>
    </form>
  </body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    messages = []
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        if question:
            messages.append({'role': 'user', 'text': question})
            messages.append({'role': 'bot', 'text': chatbot.get_answer(question)})
    return render_template_string(HTML, messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
