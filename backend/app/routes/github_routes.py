"""
backend/app/routes/github_routes.py
GitHub analysis endpoints.
"""
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity
from backend.app.middleware.auth import jwt_required_custom
from backend.app.controllers.github_controller import analyze_github

github_bp = Blueprint("github", __name__)


@github_bp.get("/<username>")
@jwt_required_custom
def analyze(username):
    """GET /api/github/:username — Analyze a GitHub profile."""
    user_id = get_jwt_identity()
    return analyze_github(user_id, username)
