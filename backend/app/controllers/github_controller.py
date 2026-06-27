"""
backend/app/controllers/github_controller.py
GitHub profile analysis controller.
"""
import os
from bson import ObjectId
from flask import current_app
from database.crud import create_one, find_one, update_one
from backend.app.middleware.error_handler import success_response, error_response


from backend.app.services.github_service import GitHubService


def analyze_github(user_id: str, username: str):
    """Fetch and analyze a GitHub profile."""
    username = username.strip().lstrip("@")
    if not username:
        return error_response("GitHub username is required", 400)

    # Check cache (less than 24h old)
    from datetime import datetime, timedelta
    cached = find_one("github_analysis", {
        "user_id": ObjectId(user_id),
        "username": username.lower(),
        "created_at": {"$gt": datetime.utcnow() - timedelta(hours=24)}
    })
    if cached:
        return success_response(cached, "GitHub analysis retrieved from cache")

    # Fetch from GitHub API
    try:
        service = GitHubService()
        analysis_data = service.analyze(username)
    except ValueError as e:
        return error_response(str(e), 404)
    except PermissionError as e:
        return error_response(str(e), 401)
    except Exception as e:
        current_app.logger.error(f"GitHub analysis failed: {e}")
        return error_response("Failed to fetch GitHub data. Check username and token.", 500)

    # Save to DB
    doc = {
        **analysis_data,
        "user_id": ObjectId(user_id),
        "username": username.lower(),
    }

    existing = find_one("github_analysis", {"user_id": ObjectId(user_id), "username": username.lower()})
    if existing:
        result = update_one("github_analysis", {"user_id": ObjectId(user_id), "username": username.lower()}, analysis_data)
    else:
        result = create_one("github_analysis", doc)

    _log_activity(user_id, "github_analyze", None, None)
    return success_response(result, "GitHub profile analyzed successfully")


def _log_activity(user_id, action, resource_id, resource_type):
    try:
        from flask import request
        create_one("activity_logs", {
            "user_id": ObjectId(user_id),
            "action": action,
            "resource_id": None,
            "resource_type": None,
            "ip_address": request.remote_addr or "unknown",
            "user_agent": request.headers.get("User-Agent", "")[:200],
            "metadata": {},
        })
    except Exception:
        pass
