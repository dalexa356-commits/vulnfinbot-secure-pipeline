import html
import re

from flask import Blueprint, jsonify, request

bp = Blueprint("main", __name__)

MAX_MESSAGE_LENGTH = 1000
MAX_RESPONSE_LENGTH = 2000
SYSTEM_PROMPT = "You are a financial assistant. Only answer questions about personal finance."
FALLBACK_RESPONSE = "Sorry, I cannot provide that response."

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{10,}"),
    re.compile(r"\b\d{16}\b"),
]


def generate_mock_response(message):
    # Заглушка вместо настоящего ИИ
    return "You can start by tracking your income and expenses."


def validate_output(text):
    # Проверяем ответ модели перед отправкой пользователю
    if not isinstance(text, str) or not text.strip():
        return FALLBACK_RESPONSE
    if SYSTEM_PROMPT in text:
        return FALLBACK_RESPONSE
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            return FALLBACK_RESPONSE
    return html.escape(text[:MAX_RESPONSE_LENGTH])


@bp.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@bp.post("/api/chat")
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    if "message" not in data:
        return jsonify({"error": "Field 'message' is required"}), 400

    message = data["message"]

    if not isinstance(message, str):
        return jsonify({"error": "Field 'message' must be a string"}), 400

    message = message.strip()

    if not message:
        return jsonify({"error": "Message must not be empty"}), 400

    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": "Message is too long"}), 400

    response_text = validate_output(generate_mock_response(message))
    return jsonify({"response": response_text}), 200
