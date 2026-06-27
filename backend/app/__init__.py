"""
backend/app/__init__.py
Flask application factory. Creates and configures the Flask app.
"""
import os
import sys
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Ensure project root is on path for database/ml imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.config import get_config
from database.connection import db_connection


def create_app(config_class=None) -> Flask:
    """Application factory pattern."""
    app = Flask(__name__)

    # Load configuration
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ── Extensions ──────────────────────────────────────────────────────────────
    JWTManager(app)

    CORS(
        app,
        origins=app.config["CORS_ORIGINS"],
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    )

    # ── Database connection ─────────────────────────────────────────────────────
    with app.app_context():
        try:
            db_connection.connect()
        except Exception as e:
            app.logger.warning(f"Database connection failed: {e}")

    # ── Error handlers ──────────────────────────────────────────────────────────
    from backend.app.middleware.error_handler import register_error_handlers
    register_error_handlers(app)

    # ── Blueprints ──────────────────────────────────────────────────────────────
    from backend.app.routes.auth_routes import auth_bp
    from backend.app.routes.resume_routes import resume_bp
    from backend.app.routes.analysis_routes import analysis_bp
    from backend.app.routes.career_routes import career_bp
    from backend.app.routes.github_routes import github_bp
    from backend.app.routes.activity_routes import activity_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(resume_bp, url_prefix="/api/resume")
    app.register_blueprint(analysis_bp, url_prefix="/api/analysis")
    app.register_blueprint(career_bp, url_prefix="/api/career")
    app.register_blueprint(github_bp, url_prefix="/api/github")
    app.register_blueprint(activity_bp, url_prefix="/api/activity")

    # ── Health check ────────────────────────────────────────────────────────────
    @app.get("/api/health")
    def health():
        return {"status": "ok", "service": "Nexora-AI API", "version": "1.0.0"}

    return app
