"""
backend/app/routes/resume_routes.py
Resume management endpoints.
"""
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from backend.app.middleware.auth import jwt_required_custom
from backend.app.controllers.resume_controller import (
    upload_resume, get_resume_history, get_resume,
    delete_resume, get_resume_stats
)

resume_bp = Blueprint("resume", __name__)


@resume_bp.post("/upload")
@jwt_required_custom
def upload():
    """POST /api/resume/upload — Upload PDF resume."""
    user_id = get_jwt_identity()
    file = request.files.get("file")
    return upload_resume(user_id, file)


@resume_bp.get("/history")
@jwt_required_custom
def history():
    """GET /api/resume/history — Get paginated resume history."""
    user_id = get_jwt_identity()
    page = int(request.args.get("page", 1))
    limit = min(int(request.args.get("limit", 10)), 50)
    return get_resume_history(user_id, page, limit)


@resume_bp.get("/stats")
@jwt_required_custom
def stats():
    """GET /api/resume/stats — Get resume dashboard statistics."""
    user_id = get_jwt_identity()
    return get_resume_stats(user_id)


@resume_bp.get("/<resume_id>")
@jwt_required_custom
def get_single(resume_id):
    """GET /api/resume/:id — Get single resume with analysis."""
    user_id = get_jwt_identity()
    return get_resume(user_id, resume_id)


@resume_bp.delete("/<resume_id>")
@jwt_required_custom
def delete(resume_id):
    """DELETE /api/resume/:id — Delete a resume."""
    user_id = get_jwt_identity()
    return delete_resume(user_id, resume_id)
