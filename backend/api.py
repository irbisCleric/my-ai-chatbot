from flask import Flask, request, jsonify
from backend.chatbot import chatbot_conversation

app = Flask(__name__)

@app.route('/chatbot', methods=['POST'])
def chatbot_route():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = chatbot_conversation(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
