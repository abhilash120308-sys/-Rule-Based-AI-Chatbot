"""
Rule-Based AI Chatbot - Web Server Application
==============================================
Flask-based backend application serving the modern interactive web interface
and RESTful API endpoints for the deterministic chatbot engine.

Author: Industrial Training Kit - Project 1
"""

import time
from flask import Flask, render_template, request, jsonify
from chatbot import RuleBasedChatbot

app = Flask(__name__)

# Instantiate a single chatbot engine
bot_engine = RuleBasedChatbot()


@app.route("/")
def index():
    """Renders the main Chatbot interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chat API endpoint.
    Accepts: { "message": "user input text" }
    Returns: JSON response containing bot reply and full transparent execution trace.
    """
    start_time = time.perf_counter()
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")

    # Execute deterministic rule-based processing
    result = bot_engine.get_response(user_message)
    
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
    result["elapsed_ms"] = elapsed_ms
    result["server_timestamp"] = time.strftime("%H:%M:%S")

    return jsonify(result)


@app.route("/api/intents", methods=["GET"])
def get_intents():
    """
    Returns knowledge base intents and sample triggers
    for UI exploration and developer evaluation cheatsheet.
    """
    intents_summary = []
    for intent_name, data in bot_engine.knowledge_base.items():
        intents_summary.append({
            "intent": intent_name,
            "description": data["description"],
            "sample_patterns": data["patterns"][:4],
            "response": data["response"]
        })
    return jsonify({
        "total_intents": len(intents_summary),
        "exit_commands": sorted(list(bot_engine.EXIT_COMMANDS)),
        "intents": intents_summary
    })


@app.route("/api/reset", methods=["POST"])
def reset_session():
    """Resets the chat session and returns standard welcome message."""
    return jsonify({
        "status": "success",
        "message": "Chat session reset successfully.",
        "welcome_message": "Hello! I am a Rule-Based AI Chatbot. How can I help you today?"
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error occurred"}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("  Starting Rule-Based AI Chatbot Web Server")
    print("  Open your browser at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=True)
