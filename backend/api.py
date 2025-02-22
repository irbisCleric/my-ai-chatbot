from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.chatbot import chatbot_conversation

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chatbot_route():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    reply = chatbot_conversation(user_message)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
