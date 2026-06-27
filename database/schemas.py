"""
database/schemas.py
MongoDB collection schemas using JSON Schema validation.
Defines structure for all 8 collections.
"""
from datetime import datetime


# ==========================================
# Collection: users
# ==========================================
USER_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["email", "password_hash", "name", "created_at"],
            "properties": {
                "email": {
                    "bsonType": "string",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                    "description": "Valid email address required"
                },
                "password_hash": {"bsonType": "string"},
                "name": {"bsonType": "string", "minLength": 2, "maxLength": 100},
                "avatar_url": {"bsonType": "string"},
                "is_verified": {"bsonType": "bool"},
                "is_active": {"bsonType": "bool"},
                "role": {"bsonType": "string", "enum": ["user", "admin"]},
                "reset_token": {"bsonType": ["string", "null"]},
                "reset_token_expires": {"bsonType": ["date", "null"]},
                "last_login": {"bsonType": ["date", "null"]},
                "created_at": {"bsonType": "date"},
                "updated_at": {"bsonType": "date"}
            }
        }
    },
    "validationLevel": "moderate",
    "validationAction": "error"
}

# ==========================================
# Collection: profiles
# ==========================================
PROFILE_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "created_at"],
            "properties": {
                "user_id": {"bsonType": "objectId"},
                "bio": {"bsonType": "string", "maxLength": 500},
                "phone": {"bsonType": "string"},
                "location": {"bsonType": "string"},
                "website": {"bsonType": "string"},
                "github_url": {"bsonType": "string"},
                "linkedin_url": {"bsonType": "string"},
                "target_role": {"bsonType": "string"},
                "experience_years": {"bsonType": "int"},
                "skills": {"bsonType": "array", "items": {"bsonType": "string"}},
                "preferred_career": {"bsonType": "string"},
                "created_at": {"bsonType": "date"},
                "updated_at": {"bsonType": "date"}
            }
        }
    },
    "validationLevel": "moderate",
    "validationAction": "warn"
}

# ==========================================
# Collection: resumes
# ==========================================
RESUME_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "filename", "file_path", "created_at"],
            "properties": {
                "user_id": {"bsonType": "objectId"},
                "filename": {"bsonType": "string"},
                "original_name": {"bsonType": "string"},
                "file_path": {"bsonType": "string"},
                "file_size": {"bsonType": "int"},
                "mime_type": {"bsonType": "string"},
                "status": {
                    "bsonType": "string",
                    "enum": ["uploaded", "parsed", "analyzed", "error"]
                },
                "parsed_data": {
                    "bsonType": "object",
                    "properties": {
                        "name": {"bsonType": "string"},
                        "email": {"bsonType": "string"},
                        "phone": {"bsonType": "string"},
                        "github": {"bsonType": "string"},
                        "linkedin": {"bsonType": "string"},
                        "summary": {"bsonType": "string"},
                        "skills": {"bsonType": "array"},
                        "education": {"bsonType": "array"},
                        "experience": {"bsonType": "array"},
                        "projects": {"bsonType": "array"},
                        "certifications": {"bsonType": "array"},
                        "raw_text": {"bsonType": "string"}
                    }
                },
                "page_count": {"bsonType": "int"},
                "created_at": {"bsonType": "date"},
                "updated_at": {"bsonType": "date"}
            }
        }
    },
    "validationLevel": "moderate",
    "validationAction": "warn"
}

# ==========================================
# Collection: analysis
# ==========================================
ANALYSIS_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["resume_id", "user_id", "created_at"],
            "properties": {
                "resume_id": {"bsonType": "objectId"},
                "user_id": {"bsonType": "objectId"},
                "ats_score": {"bsonType": "double", "minimum": 0, "maximum": 100},
                "formatting_score": {"bsonType": "double"},
                "keyword_score": {"bsonType": "double"},
                "projects_score": {"bsonType": "double"},
                "experience_score": {"bsonType": "double"},
                "education_score": {"bsonType": "double"},
                "overall_score": {"bsonType": "double"},
                "suggestions": {"bsonType": "array", "items": {"bsonType": "string"}},
                "missing_sections": {"bsonType": "array"},
                "keyword_matches": {"bsonType": "array"},
                "strengths": {"bsonType": "array"},
                "weaknesses": {"bsonType": "array"},
                "created_at": {"bsonType": "date"}
            }
        }
    },
    "validationLevel": "moderate",
    "validationAction": "warn"
}

# ==========================================
# Collection: career_prediction
# ==========================================
CAREER_PREDICTION_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["resume_id", "user_id", "created_at"],
            "properties": {
                "resume_id": {"bsonType": "objectId"},
                "user_id": {"bsonType": "objectId"},
                "predicted_career": {"bsonType": "string"},
                "confidence": {"bsonType": "double"},
                "top_careers": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "career": {"bsonType": "string"},
                            "probability": {"bsonType": "double"}
                        }
                    }
                },
                "model_used": {"bsonType": "string"},
                "features_used": {"bsonType": "array"},
                "interview_questions": {"bsonType": "array"},
                "created_at": {"bsonType": "date"}
            }
        }
    },
    "validationLevel": "moderate",
    "validationAction": "warn"
}

# ==========================================
# Collection: roadmaps
# ==========================================
ROADMAP_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["career", "created_at"],
            "properties": {
                "career": {"bsonType": "string"},
                "user_id": {"bsonType": ["objectId", "null"]},
                "title": {"bsonType": "string"},
                "description": {"bsonType": "string"},
                "duration_weeks": {"bsonType": "int"},
                "difficulty": {"bsonType": "string", "enum": ["beginner", "intermediate", "advanced"]},
                "phases": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "phase_number": {"bsonType": "int"},
                            "title": {"bsonType": "string"},
                            "duration_weeks": {"bsonType": "int"},
                            "topics": {"bsonType": "array"},
                            "resources": {"bsonType": "array"},
                            "projects": {"bsonType": "array"}
                        }
                    }
                },
                "skills_to_learn": {"bsonType": "array"},
                "certifications": {"bsonType": "array"},
                "job_titles": {"bsonType": "array"},
                "avg_salary": {"bsonType": "string"},
                "created_at": {"bsonType": "date"}
            }
        }
    },
    "validationLevel": "moderate",
    "validationAction": "warn"
}

# ==========================================
# Collection: github_analysis
# ==========================================
GITHUB_ANALYSIS_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "user_id", "created_at"],
            "properties": {
                "username": {"bsonType": "string"},
                "user_id": {"bsonType": "objectId"},
                "profile": {"bsonType": "object"},
                "repos": {"bsonType": "array"},
                "languages": {"bsonType": "object"},
                "total_stars": {"bsonType": "int"},
                "total_forks": {"bsonType": "int"},
                "total_repos": {"bsonType": "int"},
                "followers": {"bsonType": "int"},
                "following": {"bsonType": "int"},
                "contributions": {"bsonType": "int"},
                "top_repos": {"bsonType": "array"},
                "skill_score": {"bsonType": "double"},
                "activity_score": {"bsonType": "double"},
                "created_at": {"bsonType": "date"}
            }
        }
    },
    "validationLevel": "moderate",
    "validationAction": "warn"
}

# ==========================================
# Collection: activity_logs
# ==========================================
ACTIVITY_LOG_SCHEMA = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "action", "created_at"],
            "properties": {
                "user_id": {"bsonType": "objectId"},
                "action": {
                    "bsonType": "string",
                    "enum": [
                        "login", "logout", "signup",
                        "resume_upload", "resume_analyze", "resume_delete",
                        "career_predict", "roadmap_view", "github_analyze",
                        "jd_match", "report_download", "profile_update"
                    ]
                },
                "resource_id": {"bsonType": ["objectId", "null"]},
                "resource_type": {"bsonType": ["string", "null"]},
                "ip_address": {"bsonType": "string"},
                "user_agent": {"bsonType": "string"},
                "metadata": {"bsonType": "object"},
                "created_at": {"bsonType": "date"}
            }
        }
    },
    "validationLevel": "moderate",
    "validationAction": "warn"
}

# Collection name to schema mapping
COLLECTION_SCHEMAS = {
    "users": USER_SCHEMA,
    "profiles": PROFILE_SCHEMA,
    "resumes": RESUME_SCHEMA,
    "analysis": ANALYSIS_SCHEMA,
    "career_prediction": CAREER_PREDICTION_SCHEMA,
    "roadmaps": ROADMAP_SCHEMA,
    "github_analysis": GITHUB_ANALYSIS_SCHEMA,
    "activity_logs": ACTIVITY_LOG_SCHEMA,
}
