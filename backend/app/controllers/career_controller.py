"""
backend/app/controllers/career_controller.py
Career prediction and roadmap controllers.
"""
import os
import sys
from bson import ObjectId
from flask import current_app
from database.crud import find_by_id, create_one, find_one, find_many
from backend.app.middleware.error_handler import success_response, error_response


from ml.career_predictor import career_predictor, INTERVIEW_QUESTIONS


def predict_career(user_id: str, resume_id: str):
    """Predict career from a resume."""
    resume = find_by_id("resumes", resume_id)
    if not resume:
        return error_response("Resume not found", 404)
    if resume.get("user_id") != user_id:
        return error_response("Access denied", 403)

    parsed_data = resume.get("parsed_data") or {}
    if not parsed_data or not parsed_data.get("skills"):
        return error_response("Resume needs to be parsed first. Please re-upload.", 400)

    # Check for existing prediction
    existing = find_one("career_prediction", {"resume_id": ObjectId(resume_id)})
    if existing:
        return success_response(existing, "Cached career prediction retrieved")

    try:
        predictor = career_predictor
        result = predictor.predict(parsed_data)
    except FileNotFoundError:
        return error_response(
            "ML model not trained yet. Please run: python ml/pipeline.py",
            503
        )
    except Exception as e:
        current_app.logger.error(f"Career prediction failed: {e}")
        return error_response("Career prediction failed. Please try again.", 500)

    pred_doc = {
        **result,
        "resume_id": ObjectId(resume_id),
        "user_id": ObjectId(user_id),
    }
    prediction = create_one("career_prediction", pred_doc)

    _log_activity(user_id, "career_predict", resume_id, "resume")

    return success_response(prediction, "Career prediction complete")


def get_roadmap(career: str):
    """Get learning roadmap for a career."""
    if not career or len(career.strip()) < 2:
        return error_response("Career name is required", 400)

    roadmap = find_one("roadmaps", {"career": {"$regex": career.strip(), "$options": "i"}})
    if not roadmap:
        return error_response(f"No roadmap found for career: {career}", 404)

    return success_response(roadmap)


def get_all_roadmaps():
    """Get list of all available roadmaps."""
    roadmaps = find_many(
        "roadmaps",
        {},
        projection={"career": 1, "title": 1, "duration_weeks": 1, "difficulty": 1,
                    "avg_salary": 1, "skills_to_learn": 1},
        sort=[("career", 1)]
    )
    return success_response(roadmaps)


def get_interview_questions(career: str):
    """Get interview questions for a specific career."""
    questions = INTERVIEW_QUESTIONS.get(career, INTERVIEW_QUESTIONS.get("Software Engineer", []))
    return success_response({"career": career, "questions": questions})


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
