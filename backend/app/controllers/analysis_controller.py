"""
backend/app/controllers/analysis_controller.py
ATS analysis, JD matching, and report generation controllers.
"""
import os
import sys
from datetime import datetime
from bson import ObjectId
from flask import current_app, send_file
from database.crud import (
    find_by_id, create_one, update_by_id, find_one
)
from backend.app.middleware.error_handler import success_response, error_response


from ml.ats_scorer import ats_scorer
from ml.jd_matcher import jd_matcher
from backend.app.services.report_service import generate_pdf_report


def analyze_resume(user_id: str, resume_id: str):
    """Run ATS analysis on a resume."""
    resume = find_by_id("resumes", resume_id)
    if not resume:
        return error_response("Resume not found", 404)
    if resume.get("user_id") != user_id:
        return error_response("Access denied", 403)

    parsed_data = resume.get("parsed_data") or {}
    if not parsed_data:
        return error_response("Resume has not been parsed yet", 400)

    # Run ATS scoring
    try:
        scorer = ats_scorer
        result = scorer.score(parsed_data, parsed_data.get("raw_text", ""))
    except Exception as e:
        current_app.logger.error(f"ATS scoring failed: {e}")
        return error_response("Analysis failed. Please try again.", 500)

    # Check if analysis already exists
    existing = find_one("analysis", {"resume_id": ObjectId(resume_id)})

    analysis_doc = {
        **result,
        "resume_id": ObjectId(resume_id),
        "user_id": ObjectId(user_id),
    }

    if existing:
        analysis = update_by_id("analysis", existing["id"], result)
    else:
        analysis = create_one("analysis", analysis_doc)

    # Update resume status
    update_by_id("resumes", resume_id, {"status": "analyzed"})

    _log_activity(user_id, "resume_analyze", resume_id, "resume")

    return success_response(analysis, "Analysis completed")


def get_analysis(user_id: str, resume_id: str):
    """Get existing analysis for a resume."""
    resume = find_by_id("resumes", resume_id)
    if not resume:
        return error_response("Resume not found", 404)
    if resume.get("user_id") != user_id:
        return error_response("Access denied", 403)

    analysis = find_one("analysis", {"resume_id": ObjectId(resume_id)})
    if not analysis:
        return error_response("No analysis found. Please run analysis first.", 404)

    return success_response(analysis)


def match_job_description(user_id: str, resume_id: str, jd_text: str):
    """Match resume against a job description."""
    if not jd_text or len(jd_text.strip()) < 50:
        return error_response("Please provide a job description (minimum 50 characters)", 400)

    resume = find_by_id("resumes", resume_id)
    if not resume:
        return error_response("Resume not found", 404)
    if resume.get("user_id") != user_id:
        return error_response("Access denied", 403)

    parsed_data = resume.get("parsed_data") or {}
    if not parsed_data:
        return error_response("Resume not parsed. Please re-upload.", 400)

    try:
        matcher = jd_matcher
        result = matcher.match(parsed_data, jd_text)
    except Exception as e:
        current_app.logger.error(f"JD matching failed: {e}")
        return error_response("JD matching failed. Please try again.", 500)

    _log_activity(user_id, "jd_match", resume_id, "resume")
    return success_response(result)


def download_report(user_id: str, resume_id: str):
    """Generate and download PDF analysis report."""
    resume = find_by_id("resumes", resume_id)
    if not resume:
        return error_response("Resume not found", 404)
    if resume.get("user_id") != user_id:
        return error_response("Access denied", 403)

    analysis = find_one("analysis", {"resume_id": ObjectId(resume_id)})
    if not analysis:
        return error_response("Please run analysis before downloading report", 400)

    career_pred = find_one("career_prediction", {"resume_id": ObjectId(resume_id)})

    try:
        pdf_path = generate_pdf_report(resume, analysis, career_pred)
    except Exception as e:
        current_app.logger.error(f"Report generation failed: {e}")
        return error_response("Report generation failed", 500)

    _log_activity(user_id, "report_download", resume_id, "resume")

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"nexora_report_{resume_id[:8]}.pdf",
        mimetype="application/pdf"
    )


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
