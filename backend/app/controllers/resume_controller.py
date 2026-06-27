"""
backend/app/controllers/resume_controller.py
Resume upload, retrieval, and management logic.
"""
import os
import uuid
from datetime import datetime
from bson import ObjectId
from flask import current_app, send_file
from werkzeug.utils import secure_filename
from database.crud import (
    create_one, find_by_id, find_many, count_documents,
    update_by_id, delete_by_id, get_user_resumes
)
from backend.app.middleware.error_handler import success_response, error_response

from ml.resume_parser import resume_parser


def allowed_file(filename: str) -> bool:
    allowed = current_app.config.get("ALLOWED_EXTENSIONS", {"pdf"})
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


def upload_resume(user_id: str, file):
    """Handle resume PDF upload and initial parsing."""
    if not file or file.filename == "":
        return error_response("No file provided", 400)

    if not allowed_file(file.filename):
        return error_response("Only PDF files are allowed", 400)

    # Generate safe unique filename
    original_name = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_name}"
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(upload_folder, unique_filename)

    file.save(file_path)
    file_size = os.path.getsize(file_path)

    # Parse resume
    try:
        parser = resume_parser
        parsed_data = parser.parse(file_path)
        status = "parsed"
    except Exception as e:
        current_app.logger.warning(f"Parse failed: {e}")
        parsed_data = {}
        status = "uploaded"

    resume_doc = {
        "user_id": ObjectId(user_id),
        "filename": unique_filename,
        "original_name": original_name,
        "file_path": file_path,
        "file_size": file_size,
        "mime_type": "application/pdf",
        "status": status,
        "parsed_data": parsed_data,
        "page_count": parsed_data.get("page_count", 0),
    }

    resume = create_one("resumes", resume_doc)

    _log_activity(user_id, "resume_upload", resume["id"], "resume")

    return success_response(resume, "Resume uploaded and parsed successfully", 201)


def get_resume_history(user_id: str, page: int = 1, limit: int = 10):
    """Get paginated list of user's resumes."""
    skip = (page - 1) * limit
    resumes, total = get_user_resumes(user_id, skip=skip, limit=limit)

    return success_response({
        "resumes": resumes,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
    })


def get_resume(user_id: str, resume_id: str):
    """Get single resume with analysis data."""
    from database.crud import get_resume_with_analysis
    resume = get_resume_with_analysis(resume_id)

    if not resume:
        return error_response("Resume not found", 404)

    # Ownership check
    if resume.get("user_id") != user_id:
        return error_response("Access denied", 403)

    return success_response(resume)


def delete_resume(user_id: str, resume_id: str):
    """Delete a resume and its associated file."""
    resume = find_by_id("resumes", resume_id)
    if not resume:
        return error_response("Resume not found", 404)
    if resume.get("user_id") != user_id:
        return error_response("Access denied", 403)

    # Delete physical file
    file_path = resume.get("file_path", "")
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass

    delete_by_id("resumes", resume_id)
    _log_activity(user_id, "resume_delete", resume_id, "resume")

    return success_response(message="Resume deleted successfully")


def get_resume_stats(user_id: str):
    """Get dashboard stats for a user's resumes."""
    from database.connection import get_collection
    from bson import ObjectId as OID
    pipeline = [
        {"$match": {"user_id": OID(user_id)}},
        {"$group": {
            "_id": None,
            "total_resumes": {"$sum": 1},
            "analyzed": {"$sum": {"$cond": [{"$eq": ["$status", "analyzed"]}, 1, 0]}},
        }}
    ]
    col = get_collection("resumes")
    result = list(col.aggregate(pipeline))

    analysis_col = get_collection("analysis")
    scores = list(analysis_col.find(
        {"user_id": OID(user_id)},
        {"overall_score": 1}
    ).sort("created_at", -1).limit(5))

    avg_score = round(
        sum(s.get("overall_score", 0) for s in scores) / len(scores), 1
    ) if scores else 0

    stats = result[0] if result else {"total_resumes": 0, "analyzed": 0}
    return success_response({
        "total_resumes": stats.get("total_resumes", 0),
        "analyzed": stats.get("analyzed", 0),
        "avg_ats_score": avg_score,
        "recent_scores": [s.get("overall_score", 0) for s in scores],
    })


def _log_activity(user_id, action, resource_id, resource_type):
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
