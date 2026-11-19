from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def create_app():
    app = Flask(__name__)

    from app.routes import bp
    app.register_blueprint(bp)

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({"error": error.name}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        # Не показываем пользователю внутренние детали ошибки
        return jsonify({"error": "Internal server error"}), 500

    return app
