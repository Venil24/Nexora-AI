"""
backend/app/routes/analysis_routes.py
Analysis endpoints: ATS score, JD match, report download.
"""
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from backend.app.middleware.auth import jwt_required_custom
from backend.app.controllers.analysis_controller import (
    analyze_resume, get_analysis, match_job_description, download_report
)

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.post("/<resume_id>/run")
@jwt_required_custom
def run_analysis(resume_id):
    """POST /api/analysis/:id/run — Run ATS analysis on resume."""
    user_id = get_jwt_identity()
    return analyze_resume(user_id, resume_id)


@analysis_bp.get("/<resume_id>")
@jwt_required_custom
def get_analysis_route(resume_id):
    """GET /api/analysis/:id — Get existing analysis results."""
    user_id = get_jwt_identity()
    return get_analysis(user_id, resume_id)


@analysis_bp.post("/<resume_id>/jd-match")
@jwt_required_custom
def jd_match(resume_id):
    """POST /api/analysis/:id/jd-match — Match resume against job description."""
    user_id = get_jwt_identity()
    body = request.get_json(silent=True) or {}
    jd_text = body.get("jd_text", "")
    return match_job_description(user_id, resume_id, jd_text)


@analysis_bp.get("/<resume_id>/report")
@jwt_required_custom
def report(resume_id):
    """GET /api/analysis/:id/report — Download PDF analysis report."""
    user_id = get_jwt_identity()
    return download_report(user_id, resume_id)
