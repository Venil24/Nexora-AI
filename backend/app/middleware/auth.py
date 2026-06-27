"""
backend/app/middleware/auth.py
JWT authentication middleware and decorators.
"""
from functools import wraps
from flask import request, current_app
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_identity, get_jwt
)
from database.crud import find_user_by_id
from backend.app.middleware.error_handler import error_response


def jwt_required_custom(fn):
    """Custom JWT required decorator that validates user still exists and is active."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = find_user_by_id(user_id)
            if not user:
                return error_response("User not found", 401)
            if not user.get("is_active", True):
                return error_response("Account is deactivated", 401)
            return fn(*args, **kwargs)
        except Exception as e:
            return error_response(str(e), 401)
    return wrapper


def admin_required(fn):
    """Decorator requiring admin role."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = find_user_by_id(user_id)
            if not user or user.get("role") != "admin":
                return error_response("Admin access required", 403)
            return fn(*args, **kwargs)
        except Exception as e:
            return error_response(str(e), 401)
    return wrapper


def get_current_user():
    """Get the current authenticated user."""
    user_id = get_jwt_identity()
    return find_user_by_id(user_id)
