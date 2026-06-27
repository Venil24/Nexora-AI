"""
database/seed.py
Seed script for Nexora-AI database.
Creates collections, applies schemas/indexes, and inserts sample data.
Run: python database/seed.py
"""
import os
import sys
import bcrypt
from datetime import datetime, timedelta
from bson import ObjectId
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from database.connection import get_db
from database.schemas import COLLECTION_SCHEMAS
from database.indexes import create_all_indexes


def setup_collections(db):
    """Create collections with schema validation."""
    existing = db.list_collection_names()
    for name, schema in COLLECTION_SCHEMAS.items():
        if name not in existing:
            db.create_collection(name, **schema)
            print(f"  Created collection: {name}")
        else:
            db.command("collMod", name, **schema)
            print(f"  Updated schema for: {name}")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_users(db) -> list:
    """Insert sample users."""
    users_col = db["users"]
    users_col.delete_many({})  # Clear existing for clean seed

    user_ids = [ObjectId(), ObjectId(), ObjectId()]
    now = datetime.utcnow()

    users = [
        {
            "_id": user_ids[0],
            "email": "admin@nexora.ai",
            "password_hash": hash_password("Admin@123"),
            "name": "Alex Morgan",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex",
            "is_verified": True,
            "is_active": True,
            "role": "admin",
            "reset_token": None,
            "reset_token_expires": None,
            "last_login": now,
            "created_at": now - timedelta(days=30),
            "updated_at": now,
        },
        {
            "_id": user_ids[1],
            "email": "john@example.com",
            "password_hash": hash_password("Test@123"),
            "name": "John Doe",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=John",
            "is_verified": True,
            "is_active": True,
            "role": "user",
            "reset_token": None,
            "reset_token_expires": None,
            "last_login": now - timedelta(hours=2),
            "created_at": now - timedelta(days=15),
            "updated_at": now,
        },
        {
            "_id": user_ids[2],
            "email": "jane@example.com",
            "password_hash": hash_password("Test@123"),
            "name": "Jane Smith",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Jane",
            "is_verified": True,
            "is_active": True,
            "role": "user",
            "reset_token": None,
            "reset_token_expires": None,
            "last_login": now - timedelta(days=1),
            "created_at": now - timedelta(days=10),
            "updated_at": now,
        }
    ]
    users_col.insert_many(users)
    print(f"  Inserted {len(users)} users")
    return user_ids


def seed_profiles(db, user_ids: list):
    """Insert sample user profiles."""
    profiles_col = db["profiles"]
    profiles_col.delete_many({})
    now = datetime.utcnow()

    profiles = [
        {
            "user_id": user_ids[0],
            "bio": "Full-stack engineer with 8 years of experience building scalable SaaS products.",
            "phone": "+1-555-0100",
            "location": "San Francisco, CA",
            "website": "https://alexmorgan.dev",
            "github_url": "https://github.com/alexmorgan",
            "linkedin_url": "https://linkedin.com/in/alexmorgan",
            "target_role": "Engineering Manager",
            "experience_years": 8,
            "skills": ["Python", "React", "AWS", "MongoDB", "Docker", "Kubernetes"],
            "preferred_career": "Software Engineer",
            "created_at": now,
            "updated_at": now,
        },
        {
            "user_id": user_ids[1],
            "bio": "Data enthusiast passionate about ML and AI. Building intelligent systems.",
            "phone": "+1-555-0101",
            "location": "New York, NY",
            "website": "",
            "github_url": "https://github.com/johndoe",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "target_role": "Data Scientist",
            "experience_years": 3,
            "skills": ["Python", "TensorFlow", "Pandas", "SQL", "Scikit-learn", "R"],
            "preferred_career": "Data Scientist",
            "created_at": now,
            "updated_at": now,
        },
        {
            "user_id": user_ids[2],
            "bio": "Frontend developer creating beautiful and accessible web experiences.",
            "phone": "+1-555-0102",
            "location": "Austin, TX",
            "website": "https://janesmith.io",
            "github_url": "https://github.com/janesmith",
            "linkedin_url": "https://linkedin.com/in/janesmith",
            "target_role": "Senior Frontend Developer",
            "experience_years": 5,
            "skills": ["React", "TypeScript", "CSS", "Next.js", "GraphQL", "Figma"],
            "preferred_career": "Frontend Developer",
            "created_at": now,
            "updated_at": now,
        }
    ]
    profiles_col.insert_many(profiles)
    print(f"  Inserted {len(profiles)} profiles")


def seed_roadmaps(db):
    """Insert learning roadmap data for popular career paths."""
    roadmaps_col = db["roadmaps"]
    roadmaps_col.delete_many({})
    now = datetime.utcnow()

    roadmaps = [
        {
            "career": "Data Scientist",
            "title": "Data Science Career Roadmap",
            "description": "Master data science from fundamentals to advanced ML techniques.",
            "duration_weeks": 24,
            "difficulty": "intermediate",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Python & Math Foundations",
                    "duration_weeks": 4,
                    "topics": ["Python basics", "NumPy", "Pandas", "Statistics", "Linear Algebra", "Probability"],
                    "resources": [
                        {"type": "course", "title": "Python for Everybody", "url": "https://coursera.org/specializations/python"},
                        {"type": "book", "title": "Python Data Science Handbook", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/"},
                    ],
                    "projects": ["Data cleaning pipeline", "EDA on Kaggle dataset"]
                },
                {
                    "phase_number": 2,
                    "title": "Machine Learning Core",
                    "duration_weeks": 6,
                    "topics": ["Supervised Learning", "Unsupervised Learning", "Scikit-learn", "Model Evaluation", "Feature Engineering"],
                    "resources": [
                        {"type": "course", "title": "Machine Learning by Andrew Ng", "url": "https://coursera.org/learn/machine-learning"},
                        {"type": "book", "title": "Hands-On ML with Scikit-Learn", "url": "https://oreilly.com/library/view/hands-on-machine-learning/"},
                    ],
                    "projects": ["Prediction model", "Classification challenge"]
                },
                {
                    "phase_number": 3,
                    "title": "Deep Learning & NLP",
                    "duration_weeks": 6,
                    "topics": ["Neural Networks", "TensorFlow/PyTorch", "NLP basics", "Text Classification", "Transfer Learning"],
                    "resources": [
                        {"type": "course", "title": "Deep Learning Specialization", "url": "https://coursera.org/specializations/deep-learning"},
                    ],
                    "projects": ["Sentiment analyzer", "Image classifier"]
                },
                {
                    "phase_number": 4,
                    "title": "MLOps & Deployment",
                    "duration_weeks": 4,
                    "topics": ["MLflow", "Docker", "FastAPI", "Model monitoring", "CI/CD for ML"],
                    "resources": [
                        {"type": "course", "title": "MLOps Specialization", "url": "https://coursera.org/specializations/machine-learning-engineering-for-production-mlops"},
                    ],
                    "projects": ["End-to-end ML pipeline", "Deployed model API"]
                },
                {
                    "phase_number": 5,
                    "title": "Portfolio & Job Prep",
                    "duration_weeks": 4,
                    "topics": ["Portfolio projects", "Kaggle competitions", "Interview prep", "System design"],
                    "resources": [],
                    "projects": ["Capstone project", "Kaggle competition submission"]
                }
            ],
            "skills_to_learn": ["Python", "SQL", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Tableau", "Spark"],
            "certifications": ["Google Professional Data Engineer", "AWS Certified ML Specialty", "IBM Data Science Professional"],
            "job_titles": ["Data Scientist", "ML Engineer", "Research Scientist", "Data Analyst"],
            "avg_salary": "$110,000 - $160,000/year",
            "created_at": now
        },
        {
            "career": "Software Engineer",
            "title": "Software Engineering Career Roadmap",
            "description": "Become a full-stack software engineer with industry-ready skills.",
            "duration_weeks": 20,
            "difficulty": "intermediate",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Programming Fundamentals",
                    "duration_weeks": 4,
                    "topics": ["Data Structures", "Algorithms", "OOP", "Git", "Linux basics"],
                    "resources": [
                        {"type": "book", "title": "Clean Code", "url": "https://amazon.com"},
                        {"type": "platform", "title": "LeetCode", "url": "https://leetcode.com"},
                    ],
                    "projects": ["Algorithm practice", "CLI tool"]
                },
                {
                    "phase_number": 2,
                    "title": "Backend Development",
                    "duration_weeks": 5,
                    "topics": ["REST APIs", "Node.js/Python", "Databases", "Authentication", "Testing"],
                    "resources": [
                        {"type": "course", "title": "The Odin Project", "url": "https://theodinproject.com"},
                    ],
                    "projects": ["REST API", "Auth system"]
                },
                {
                    "phase_number": 3,
                    "title": "Frontend Development",
                    "duration_weeks": 5,
                    "topics": ["React", "TypeScript", "State Management", "Testing", "Performance"],
                    "resources": [
                        {"type": "course", "title": "React Documentation", "url": "https://react.dev"},
                    ],
                    "projects": ["Full-stack app", "UI component library"]
                },
                {
                    "phase_number": 4,
                    "title": "DevOps & Cloud",
                    "duration_weeks": 3,
                    "topics": ["Docker", "AWS/GCP", "CI/CD", "Kubernetes basics", "Monitoring"],
                    "resources": [],
                    "projects": ["Dockerized app", "Cloud deployment"]
                },
                {
                    "phase_number": 5,
                    "title": "Interview Preparation",
                    "duration_weeks": 3,
                    "topics": ["System Design", "Behavioral interviews", "DSA practice", "Portfolio"],
                    "resources": [
                        {"type": "book", "title": "Designing Data-Intensive Applications", "url": "https://amazon.com"},
                    ],
                    "projects": ["Portfolio website", "Capstone project"]
                }
            ],
            "skills_to_learn": ["Python/JavaScript", "React", "Node.js", "SQL/NoSQL", "Docker", "AWS", "Git", "System Design"],
            "certifications": ["AWS Solutions Architect", "Google Cloud Professional", "Azure Developer"],
            "job_titles": ["Software Engineer", "Full Stack Developer", "Backend Engineer", "Senior Developer"],
            "avg_salary": "$95,000 - $150,000/year",
            "created_at": now
        },
        {
            "career": "Machine Learning Engineer",
            "title": "ML Engineering Career Roadmap",
            "description": "Build production ML systems that scale.",
            "duration_weeks": 28,
            "difficulty": "advanced",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "ML Fundamentals",
                    "duration_weeks": 6,
                    "topics": ["Supervised/Unsupervised Learning", "Deep Learning", "Mathematics", "Python ML stack"],
                    "resources": [],
                    "projects": ["End-to-end ML model"]
                },
                {
                    "phase_number": 2,
                    "title": "Software Engineering for ML",
                    "duration_weeks": 6,
                    "topics": ["Clean code", "Testing", "APIs", "Databases", "Docker"],
                    "resources": [],
                    "projects": ["ML API service"]
                },
                {
                    "phase_number": 3,
                    "title": "MLOps & Production",
                    "duration_weeks": 8,
                    "topics": ["MLflow", "Kubeflow", "Feature stores", "Model monitoring", "A/B testing"],
                    "resources": [],
                    "projects": ["MLOps pipeline"]
                },
                {
                    "phase_number": 4,
                    "title": "Specialization",
                    "duration_weeks": 4,
                    "topics": ["LLMs", "Computer Vision", "Recommendation Systems", "Real-time ML"],
                    "resources": [],
                    "projects": ["Specialized ML system"]
                },
                {
                    "phase_number": 5,
                    "title": "Career Preparation",
                    "duration_weeks": 4,
                    "topics": ["ML System Design", "Research papers", "Open source contributions"],
                    "resources": [],
                    "projects": ["OSS contribution", "Technical blog posts"]
                }
            ],
            "skills_to_learn": ["Python", "TensorFlow/PyTorch", "MLflow", "Spark", "Kubernetes", "SQL", "Docker"],
            "certifications": ["AWS ML Specialty", "GCP Professional ML Engineer", "TensorFlow Developer"],
            "job_titles": ["ML Engineer", "AI Engineer", "Research Engineer", "Applied Scientist"],
            "avg_salary": "$130,000 - $200,000/year",
            "created_at": now
        },
        {
            "career": "Frontend Developer",
            "title": "Frontend Development Career Roadmap",
            "description": "Master modern frontend development and build stunning user interfaces.",
            "duration_weeks": 16,
            "difficulty": "beginner",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Web Fundamentals",
                    "duration_weeks": 3,
                    "topics": ["HTML5", "CSS3", "JavaScript ES6+", "Responsive Design", "Accessibility"],
                    "resources": [
                        {"type": "platform", "title": "freeCodeCamp", "url": "https://freecodecamp.org"},
                        {"type": "platform", "title": "MDN Web Docs", "url": "https://developer.mozilla.org"},
                    ],
                    "projects": ["Portfolio website", "Landing page"]
                },
                {
                    "phase_number": 2,
                    "title": "React Ecosystem",
                    "duration_weeks": 5,
                    "topics": ["React", "TypeScript", "React Router", "State Management", "Custom Hooks"],
                    "resources": [
                        {"type": "course", "title": "React - The Complete Guide", "url": "https://udemy.com"},
                    ],
                    "projects": ["React todo app", "Dashboard UI"]
                },
                {
                    "phase_number": 3,
                    "title": "Advanced Frontend",
                    "duration_weeks": 4,
                    "topics": ["Performance", "Testing", "Webpack/Vite", "PWA", "Animation"],
                    "resources": [],
                    "projects": ["Performance-optimized app", "PWA"]
                },
                {
                    "phase_number": 4,
                    "title": "Job Readiness",
                    "duration_weeks": 4,
                    "topics": ["Portfolio polish", "GitHub", "Interview prep", "Open source"],
                    "resources": [],
                    "projects": ["Capstone project", "Contribute to OSS"]
                }
            ],
            "skills_to_learn": ["HTML/CSS", "JavaScript", "React", "TypeScript", "Next.js", "Testing", "Git"],
            "certifications": ["Meta Front-End Developer", "Google UX Design"],
            "job_titles": ["Frontend Developer", "React Developer", "UI Developer", "Web Developer"],
            "avg_salary": "$75,000 - $120,000/year",
            "created_at": now
        },
        {
            "career": "DevOps Engineer",
            "title": "DevOps Engineering Career Roadmap",
            "description": "Learn to build, deploy, and scale infrastructure like a pro.",
            "duration_weeks": 22,
            "difficulty": "advanced",
            "phases": [
                {
                    "phase_number": 1,
                    "title": "Linux & Networking",
                    "duration_weeks": 4,
                    "topics": ["Linux administration", "Shell scripting", "Networking", "Security basics"],
                    "resources": [],
                    "projects": ["Automated backup script", "Server hardening"]
                },
                {
                    "phase_number": 2,
                    "title": "Containers & Orchestration",
                    "duration_weeks": 5,
                    "topics": ["Docker", "Kubernetes", "Helm", "Service Mesh"],
                    "resources": [],
                    "projects": ["Dockerized microservices", "K8s deployment"]
                },
                {
                    "phase_number": 3,
                    "title": "CI/CD & Automation",
                    "duration_weeks": 5,
                    "topics": ["GitHub Actions", "Jenkins", "Terraform", "Ansible", "GitOps"],
                    "resources": [],
                    "projects": ["Full CI/CD pipeline", "IaC with Terraform"]
                },
                {
                    "phase_number": 4,
                    "title": "Cloud Platforms",
                    "duration_weeks": 5,
                    "topics": ["AWS/GCP/Azure", "Cloud Architecture", "Cost optimization", "Disaster recovery"],
                    "resources": [],
                    "projects": ["Multi-cloud setup", "Cost optimization report"]
                },
                {
                    "phase_number": 5,
                    "title": "Monitoring & SRE",
                    "duration_weeks": 3,
                    "topics": ["Prometheus", "Grafana", "ELK Stack", "SRE practices", "Incident response"],
                    "resources": [],
                    "projects": ["Monitoring dashboard", "Runbook"]
                }
            ],
            "skills_to_learn": ["Linux", "Docker", "Kubernetes", "Terraform", "AWS", "CI/CD", "Python/Bash", "Monitoring"],
            "certifications": ["CKA", "AWS Solutions Architect", "HashiCorp Terraform"],
            "job_titles": ["DevOps Engineer", "Site Reliability Engineer", "Platform Engineer", "Cloud Engineer"],
            "avg_salary": "$110,000 - $170,000/year",
            "created_at": now
        },
    ]

    roadmaps_col.insert_many(roadmaps)
    print(f"  Inserted {len(roadmaps)} roadmaps")


def main():
    print("Starting Nexora-AI Database Seed Script...")
    print("=" * 50)

    db = get_db()

    print("\nSetting up collections with schema validation...")
    setup_collections(db)

    print("\nCreating indexes...")
    create_all_indexes()

    print("\nSeeding users...")
    user_ids = seed_users(db)

    print("\nSeeding profiles...")
    seed_profiles(db, user_ids)

    print("\nSeeding roadmaps...")
    seed_roadmaps(db)

    print("\n" + "=" * 50)
    print("Database seeded successfully!")
    print("\nSample Login Credentials:")
    print("  Admin: admin@nexora.ai / Admin@123")
    print("  User 1: john@example.com / Test@123")
    print("  User 2: jane@example.com / Test@123")


if __name__ == "__main__":
    main()
