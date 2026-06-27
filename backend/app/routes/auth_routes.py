"""
backend/app/routes/auth_routes.py
Authentication endpoints: register, login, refresh, forgot password, profile.
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.controllers.auth_controller import (
    register, login, get_me, refresh_token,
    forgot_password, reset_password, update_profile
)
from backend.app.middleware.auth import jwt_required_custom

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register_route():
    """POST /api/auth/register — Create new user account."""
    return register(request.get_json(silent=True) or {})


@auth_bp.post("/login")
def login_route():
    """POST /api/auth/login — Authenticate and return JWT tokens."""
    return login(request.get_json(silent=True) or {})


@auth_bp.get("/me")
@jwt_required_custom
def me_route():
    """GET /api/auth/me — Get current authenticated user."""
    user_id = get_jwt_identity()
    return get_me(user_id)


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh_route():
    """POST /api/auth/refresh — Issue new access token from refresh token."""
    return refresh_token()


@auth_bp.post("/forgot-password")
def forgot_password_route():
    """POST /api/auth/forgot-password — Send password reset email."""
    return forgot_password(request.get_json(silent=True) or {})


@auth_bp.post("/reset-password")
def reset_password_route():
    """POST /api/auth/reset-password — Reset password using token."""
    return reset_password(request.get_json(silent=True) or {})


@auth_bp.put("/profile")
@jwt_required_custom
def update_profile_route():
    """PUT /api/auth/profile — Update user profile."""
    user_id = get_jwt_identity()
    return update_profile(user_id, request.get_json(silent=True) or {})
