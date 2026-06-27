"""
database/indexes.py
MongoDB index definitions for all collections.
Optimizes query performance for all API endpoints.
"""
from pymongo import ASCENDING, DESCENDING, TEXT
from database.connection import get_db


def create_all_indexes():
    """Create all MongoDB indexes for the application."""
    db = get_db()
    results = {}

    # ---- users collection ----
    users = db["users"]
    results["users"] = [
        users.create_index([("email", ASCENDING)], unique=True, name="email_unique"),
        users.create_index([("reset_token", ASCENDING)], sparse=True, name="reset_token_idx"),
        users.create_index([("created_at", DESCENDING)], name="created_at_idx"),
        users.create_index([("is_active", ASCENDING)], name="is_active_idx"),
    ]

    # ---- profiles collection ----
    profiles = db["profiles"]
    results["profiles"] = [
        profiles.create_index([("user_id", ASCENDING)], unique=True, name="user_id_unique"),
        profiles.create_index([("preferred_career", ASCENDING)], sparse=True, name="career_idx"),
    ]

    # ---- resumes collection ----
    resumes = db["resumes"]
    results["resumes"] = [
        resumes.create_index([("user_id", ASCENDING)], name="user_id_idx"),
        resumes.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)], name="user_date_idx"),
        resumes.create_index([("status", ASCENDING)], name="status_idx"),
        resumes.create_index([("created_at", DESCENDING)], name="created_at_idx"),
    ]

    # ---- analysis collection ----
    analysis = db["analysis"]
    results["analysis"] = [
        analysis.create_index([("resume_id", ASCENDING)], unique=True, name="resume_id_unique"),
        analysis.create_index([("user_id", ASCENDING)], name="user_id_idx"),
        analysis.create_index([("overall_score", DESCENDING)], name="score_idx"),
        analysis.create_index([("created_at", DESCENDING)], name="created_at_idx"),
    ]

    # ---- career_prediction collection ----
    career = db["career_prediction"]
    results["career_prediction"] = [
        career.create_index([("resume_id", ASCENDING)], unique=True, name="resume_id_unique"),
        career.create_index([("user_id", ASCENDING)], name="user_id_idx"),
        career.create_index([("predicted_career", ASCENDING)], name="career_idx"),
    ]

    # ---- roadmaps collection ----
    roadmaps = db["roadmaps"]
    results["roadmaps"] = [
        roadmaps.create_index([("career", ASCENDING)], name="career_idx"),
        roadmaps.create_index([("career", ASCENDING), ("difficulty", ASCENDING)], name="career_diff_idx"),
        roadmaps.create_index([("career", TEXT)], name="career_text_idx"),
    ]

    # ---- github_analysis collection ----
    github = db["github_analysis"]
    results["github_analysis"] = [
        github.create_index([("user_id", ASCENDING), ("username", ASCENDING)], unique=True, name="user_github_unique"),
        github.create_index([("username", ASCENDING)], name="username_idx"),
        github.create_index([("created_at", DESCENDING)], name="created_at_idx"),
    ]

    # ---- activity_logs collection ----
    logs = db["activity_logs"]
    results["activity_logs"] = [
        logs.create_index([("user_id", ASCENDING)], name="user_id_idx"),
        logs.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)], name="user_date_idx"),
        logs.create_index([("action", ASCENDING)], name="action_idx"),
        logs.create_index([("created_at", DESCENDING)], name="created_at_idx"),
        # TTL index: auto-delete logs older than 90 days
        logs.create_index(
            [("created_at", ASCENDING)],
            expireAfterSeconds=7776000,
            name="ttl_90days"
        ),
    ]

    print("All MongoDB indexes created successfully")
    return results


def drop_all_indexes():
    """Drop all custom indexes (for re-creation during maintenance)."""
    db = get_db()
    collections = [
        "users", "profiles", "resumes", "analysis",
        "career_prediction", "roadmaps", "github_analysis", "activity_logs"
    ]
    for col_name in collections:
        col = db[col_name]
        col.drop_indexes()
    print("All indexes dropped")


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    create_all_indexes()
