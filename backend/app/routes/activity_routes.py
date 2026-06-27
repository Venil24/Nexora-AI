"""
backend/app/routes/activity_routes.py
Activity logs endpoint.
"""
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from backend.app.middleware.auth import jwt_required_custom
from database.crud import find_many, count_documents
from backend.app.middleware.error_handler import success_response
from bson import ObjectId

activity_bp = Blueprint("activity", __name__)


@activity_bp.get("/logs")
@jwt_required_custom
def get_logs():
    """GET /api/activity/logs — Get paginated activity logs for current user."""
    user_id = get_jwt_identity()
    page = int(request.args.get("page", 1))
    limit = min(int(request.args.get("limit", 20)), 50)
    skip = (page - 1) * limit

    query = {"user_id": ObjectId(user_id)}
    logs = find_many(
        "activity_logs",
        query,
        sort=[("created_at", -1)],
        skip=skip,
        limit=limit
    )
    total = count_documents("activity_logs", query)

    return success_response({
        "logs": logs,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    })
