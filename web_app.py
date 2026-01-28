from flask import Flask, Render_Template, request, jsonify
from core import get_bot_reply

app = Flask(__name__)

@app.route("/")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    reply = get_bot_reply(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)