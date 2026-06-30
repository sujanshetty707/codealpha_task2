import os
from flask import Flask, render_template_string, request, session
from faq_chatbot import FAQChatbot

app = Flask(__name__)
app.secret_key = "faq-chatbot-secret"
base_dir = os.path.dirname(__file__)
chatbot = FAQChatbot(os.path.join(base_dir, "data", "faqs.json"))

HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>FAQ Chatbot</title>
    <style>
      body { font-family: Arial, sans-serif; background: #f5f7fb; color: #1f2937; margin: 0; padding: 24px; }
      .card { max-width: 760px; margin: 30px auto; background: white; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); overflow: hidden; }
      .header { background: linear-gradient(135deg, #2563eb, #4f46e5); color: white; padding: 24px; }
      .messages { padding: 20px; min-height: 320px; display: flex; flex-direction: column; gap: 10px; }
      .bubble { max-width: 80%; padding: 12px 14px; border-radius: 14px; line-height: 1.5; }
      .user { align-self: flex-end; background: #dbeafe; color: #1e3a8a; }
      .bot { align-self: flex-start; background: #eef2ff; color: #3730a3; }
      form { display: flex; gap: 10px; padding: 16px 20px 20px; }
      input[type=text] { flex: 1; padding: 12px; border: 1px solid #d1d5db; border-radius: 999px; outline: none; }
      button { padding: 12px 16px; border: none; border-radius: 999px; background: #2563eb; color: white; cursor: pointer; }
      .hint { padding: 0 20px 20px; color: #6b7280; font-size: 0.95rem; }
    </style>
  </head>
  <body>
    <div class="card">
      <div class="header">
        <h2>FAQ Chatbot</h2>
        <p>Ask anything about our product or services and I’ll find the best matching answer.</p>
      </div>
      <div class="messages">
        {% for message in messages %}
          <div class="bubble {{ message['role'] }}">{{ message['text'] }}</div>
        {% endfor %}
      </div>
      <div class="hint">Try: password reset, refund policy, shipping, or support</div>
      <form method="post">
        <input type="text" name="question" placeholder="Type your question here" autofocus>
        <button type="submit">Send</button>
      </form>
    </div>
  </body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    messages = session.get('messages', [])
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        if question:
            messages.append({'role': 'user', 'text': question})
            messages.append({'role': 'bot', 'text': chatbot.get_answer(question)})
            session['messages'] = messages
    return render_template_string(HTML, messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
