"""
backend/app/controllers/auth_controller.py
Authentication business logic: signup, login, forgot password, profile.
"""
import re
import secrets
from datetime import datetime, timedelta
import bcrypt
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from bson import ObjectId
from database.crud import (
    create_one, find_user_by_email, find_user_by_id,
    update_one, update_by_id, find_one
)
from database.connection import get_collection
from backend.app.middleware.error_handler import success_response, error_response
from backend.app.services.email_service import send_password_reset_email

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PASSWORD_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')


def _hash_password(password: str) -> str:
    rounds = current_app.config.get("BCRYPT_ROUNDS", 12)
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds)).decode()


def _check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def register(data: dict):
    """Register a new user."""
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    # Validation
    errors = {}
    if not name or len(name) < 2:
        errors["name"] = "Name must be at least 2 characters"
    if not EMAIL_RE.match(email):
        errors["email"] = "Invalid email address"
    if not PASSWORD_RE.match(password):
        errors["password"] = "Password must be at least 8 characters with uppercase, lowercase, and number"
    if errors:
        return error_response("Validation failed", 422, errors)

    # Check duplicate email
    if find_user_by_email(email):
        return error_response("An account with this email already exists", 409)

    # Create user
    user_doc = {
        "email": email,
        "password_hash": _hash_password(password),
        "name": name,
        "avatar_url": f"https://api.dicebear.com/7.x/avataaars/svg?seed={name.replace(' ', '')}",
        "is_verified": False,
        "is_active": True,
        "role": "user",
        "reset_token": None,
        "reset_token_expires": None,
        "last_login": None,
    }
    user = create_one("users", user_doc)

    # Create blank profile
    profile_doc = {
        "user_id": ObjectId(user["id"]),
        "bio": "",
        "phone": "",
        "location": "",
        "website": "",
        "github_url": "",
        "linkedin_url": "",
        "target_role": "",
        "experience_years": 0,
        "skills": [],
        "preferred_career": "",
    }
    create_one("profiles", profile_doc)

    # Log activity
    _log_activity(user["id"], "signup", None, None)

    # Generate tokens
    access_token = create_access_token(identity=user["id"])
    refresh_token = create_refresh_token(identity=user["id"])

    return success_response(
        {
            "user": _safe_user(user),
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        "Account created successfully",
        201
    )


def login(data: dict):
    """Login with email and password."""
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return error_response("Email and password are required", 400)

    # Fetch user including password_hash
    users_col = get_collection("users")
    user_doc = users_col.find_one({"email": email})
    if not user_doc:
        return error_response("Invalid email or password", 401)

    if not _check_password(password, user_doc.get("password_hash", "")):
        return error_response("Invalid email or password", 401)

    if not user_doc.get("is_active", True):
        return error_response("Your account has been deactivated", 403)

    # Update last login
    users_col.update_one(
        {"_id": user_doc["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )

    user_id = str(user_doc["_id"])
    _log_activity(user_id, "login", None, None)

    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    return success_response(
        {
            "user": {
                "id": user_id,
                "name": user_doc.get("name"),
                "email": user_doc.get("email"),
                "avatar_url": user_doc.get("avatar_url"),
                "role": user_doc.get("role", "user"),
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        "Login successful"
    )


def get_me(user_id: str):
    """Get current user profile."""
    from database.crud import find_one as crud_find_one
    user = find_user_by_id(user_id)
    if not user:
        return error_response("User not found", 404)

    profile = crud_find_one("profiles", {"user_id": ObjectId(user_id)})

    return success_response({
        "user": _safe_user(user),
        "profile": profile,
    })


def refresh_token():
    """Issue a new access token from a valid refresh token."""
    user_id = get_jwt_identity()
    user = find_user_by_id(user_id)
    if not user:
        return error_response("User not found", 401)

    new_access_token = create_access_token(identity=user_id)
    return success_response({"access_token": new_access_token}, "Token refreshed")


def forgot_password(data: dict):
    """Initiate password reset flow."""
    email = (data.get("email") or "").strip().lower()
    if not EMAIL_RE.match(email):
        return error_response("Invalid email address", 400)

    user = find_user_by_email(email)
    # Always return success to prevent email enumeration
    if not user:
        return success_response(message="If that email exists, a reset link was sent.")

    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)

    users_col = get_collection("users")
    users_col.update_one(
        {"email": email},
        {"$set": {"reset_token": token, "reset_token_expires": expires}}
    )

    try:
        send_password_reset_email(email, user.get("name", ""), token)
    except Exception as e:
        current_app.logger.warning(f"Email send failed: {e}")

    return success_response(message="If that email exists, a reset link was sent.")


def reset_password(data: dict):
    """Reset password using the token sent by email."""
    token = data.get("token", "").strip()
    new_password = data.get("password", "")

    if not token:
        return error_response("Reset token is required", 400)
    if not PASSWORD_RE.match(new_password):
        return error_response("Password must be at least 8 characters with uppercase, lowercase, and number", 400)

    users_col = get_collection("users")
    user_doc = users_col.find_one({
        "reset_token": token,
        "reset_token_expires": {"$gt": datetime.utcnow()}
    })

    if not user_doc:
        return error_response("Invalid or expired reset token", 400)

    users_col.update_one(
        {"_id": user_doc["_id"]},
        {"$set": {
            "password_hash": _hash_password(new_password),
            "reset_token": None,
            "reset_token_expires": None,
        }}
    )

    return success_response(message="Password reset successfully. Please log in.")


def update_profile(user_id: str, data: dict):
    """Update user profile fields."""
    allowed_fields = ["name", "avatar_url"]
    profile_fields = ["bio", "phone", "location", "website", "github_url", "linkedin_url", "target_role", "experience_years", "skills", "preferred_career"]

    user_updates = {k: v for k, v in data.items() if k in allowed_fields}
    profile_updates = {k: v for k, v in data.items() if k in profile_fields}

    if user_updates:
        update_by_id("users", user_id, user_updates)

    if profile_updates:
        update_one("profiles", {"user_id": ObjectId(user_id)}, profile_updates)

    return success_response(message="Profile updated successfully")


def _safe_user(user: dict) -> dict:
    """Remove sensitive fields from user dict."""
    return {k: v for k, v in user.items() if k not in ("password_hash", "reset_token", "reset_token_expires")}


def _log_activity(user_id: str, action: str, resource_id, resource_type: str):
    """Log user activity."""
    try:
        from flask import request
        create_one("activity_logs", {
            "user_id": ObjectId(user_id),
            "action": action,
            "resource_id": ObjectId(resource_id) if resource_id else None,
            "resource_type": resource_type,
            "ip_address": request.remote_addr or "unknown",
            "user_agent": request.headers.get("User-Agent", "")[:200],
            "metadata": {},
        })
    except Exception:
        pass
