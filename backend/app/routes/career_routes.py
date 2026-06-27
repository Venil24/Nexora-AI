"""
backend/app/routes/career_routes.py
Career prediction and roadmap endpoints.
"""
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from backend.app.middleware.auth import jwt_required_custom
from backend.app.controllers.career_controller import (
    predict_career, get_roadmap, get_all_roadmaps, get_interview_questions
)

career_bp = Blueprint("career", __name__)


@career_bp.post("/predict/<resume_id>")
@jwt_required_custom
def predict(resume_id):
    """POST /api/career/predict/:resumeId — Predict career from resume."""
    user_id = get_jwt_identity()
    return predict_career(user_id, resume_id)


@career_bp.get("/roadmaps")
def roadmaps_list():
    """GET /api/career/roadmaps — List all available career roadmaps."""
    return get_all_roadmaps()


@career_bp.get("/roadmap/<path:career>")
def roadmap(career):
    """GET /api/career/roadmap/:career — Get roadmap for a specific career."""
    return get_roadmap(career)


@career_bp.get("/interview-questions/<path:career>")
def interview_questions(career):
    """GET /api/career/interview-questions/:career — Get interview questions."""
    return get_interview_questions(career)
