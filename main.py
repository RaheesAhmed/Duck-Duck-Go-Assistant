from flask import Flask, request, jsonify, send_from_directory
import flask_cors
from chat_with_assistant import chat_with_assistant

app = Flask(__name__, static_folder="static")

# Enable CORS
flask_cors.CORS(app)


@app.route("/")
def serve_static_index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/chat", methods=["GET"])
def index():
    return jsonify(
        [
            "Welcome to the Search Assistant API! Send a POST request to /chat with a user query to chat with the assistant."
        ]
    )


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "No query provided"}), 400

    user_query = data["query"]
    response = chat_with_assistant(user_query)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
