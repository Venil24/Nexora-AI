"""
ml/career_predictor.py
Career prediction using trained ML models.
Loads the best saved model and returns top career predictions.
"""
import os
import re
import json
import joblib
import numpy as np
from typing import Dict, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "trained_models")
BEST_MODEL_PATH = os.path.join(MODELS_DIR, "best_model.joblib")

# Interview questions per career
INTERVIEW_QUESTIONS = {
    "Software Engineer": [
        "Explain the difference between process and thread.",
        "What is time complexity and how do you optimize algorithms?",
        "Describe the SOLID principles and give examples.",
        "How does garbage collection work in your preferred language?",
        "Explain RESTful API design principles.",
        "What is the CAP theorem?",
        "How do you approach debugging a production issue?",
        "Describe your experience with version control and branching strategies.",
        "What is dependency injection and why is it useful?",
        "How would you design a URL shortening service?",
    ],
    "Data Scientist": [
        "Explain the bias-variance tradeoff.",
        "When would you use Random Forest over Gradient Boosting?",
        "How do you handle class imbalance in a dataset?",
        "What is regularization and why is it important?",
        "Explain precision vs recall — when do you prioritize each?",
        "How do you detect and handle outliers?",
        "What is cross-validation and why do we use it?",
        "Describe the steps in a complete ML project pipeline.",
        "How would you explain p-value to a non-technical stakeholder?",
        "What is feature selection and what methods do you use?",
    ],
    "Machine Learning Engineer": [
        "How do you deploy a machine learning model to production?",
        "Explain the difference between batch and online learning.",
        "What is model drift and how do you monitor for it?",
        "How would you design an A/B test for an ML feature?",
        "Explain feature stores and when to use them.",
        "What is data versioning and why does it matter?",
        "How do you scale model inference to millions of requests?",
        "Describe your experience with ML frameworks (TF, PyTorch, etc.).",
        "What metrics do you use to monitor model performance in production?",
        "How do you handle model rollback in production?",
    ],
    "Frontend Developer": [
        "What is the Virtual DOM and how does React use it?",
        "Explain the difference between useEffect and useLayoutEffect.",
        "What is CSS specificity and how is it calculated?",
        "How do you optimize a React application's performance?",
        "What is CORS and how do you handle it?",
        "Explain the difference between localStorage, sessionStorage, and cookies.",
        "What are React hooks and what problem do they solve?",
        "How do you ensure your application is accessible (a11y)?",
        "What is code splitting and how do you implement it?",
        "Describe the Critical Rendering Path.",
    ],
    "Backend Developer": [
        "How do you design a RESTful API?",
        "What is the difference between SQL and NoSQL databases?",
        "How do you handle database migrations in production?",
        "Explain authentication vs authorization.",
        "What is connection pooling and why is it important?",
        "How do you implement rate limiting?",
        "Describe your approach to API versioning.",
        "What is an index in a database and when should you use one?",
        "How do you secure sensitive data like passwords?",
        "What is eventual consistency in distributed systems?",
    ],
    "Full Stack Developer": [
        "How do you structure a full-stack project?",
        "Explain the flow from a browser request to a database query and back.",
        "What is server-side rendering vs client-side rendering?",
        "How do you manage state in a large React application?",
        "What is the role of a CDN?",
        "How do you handle real-time features (WebSockets, SSE)?",
        "What CI/CD practices do you follow for web projects?",
        "How do you approach cross-browser compatibility?",
        "Describe your experience with API integration.",
        "How do you handle errors on both frontend and backend?",
    ],
    "DevOps Engineer": [
        "What is Infrastructure as Code (IaC) and what tools have you used?",
        "Explain the difference between Docker and virtual machines.",
        "How do Kubernetes pods, deployments, and services relate?",
        "What is a CI/CD pipeline and how do you design one?",
        "How do you approach monitoring and alerting?",
        "What is blue-green deployment?",
        "Explain the 12-factor app methodology.",
        "How do you handle secrets management?",
        "What is service mesh and when would you use it?",
        "How do you design for high availability and fault tolerance?",
    ],
    "Data Analyst": [
        "How do you handle missing data in a dataset?",
        "What SQL window functions do you use most often?",
        "Explain the difference between INNER JOIN and LEFT JOIN.",
        "How do you identify trends in time-series data?",
        "What visualization would you use for a KPI dashboard?",
        "How do you validate your analysis results?",
        "Describe a situation where your data analysis changed a business decision.",
        "What is cohort analysis?",
        "How do you communicate complex findings to non-technical stakeholders?",
        "What is A/B testing and how do you analyze results?",
    ],
    "Cybersecurity Engineer": [
        "What is the CIA triad in cybersecurity?",
        "Explain SQL injection and how to prevent it.",
        "What is a man-in-the-middle attack?",
        "How does TLS/SSL work?",
        "What is penetration testing and what methodology do you follow?",
        "How do you implement least-privilege access?",
        "Explain the OWASP Top 10.",
        "What is a DDoS attack and how do you mitigate it?",
        "How do you approach incident response?",
        "What is zero-trust security architecture?",
    ],
    "Mobile Developer": [
        "What is the difference between native, hybrid, and cross-platform apps?",
        "How do you handle background tasks on iOS/Android?",
        "What is app state persistence and how do you implement it?",
        "How do you optimize mobile app performance?",
        "Explain the mobile app lifecycle.",
        "How do you handle push notifications?",
        "What is the difference between Flutter's stateful and stateless widgets?",
        "How do you approach testing on mobile?",
        "What are common security considerations for mobile apps?",
        "How do you submit an app to the App Store/Play Store?",
    ],
    "Cloud Architect": [
        "How do you choose between IaaS, PaaS, and SaaS for a solution?",
        "What is a multi-region deployment strategy?",
        "How do you design for cost optimization in the cloud?",
        "Explain the shared responsibility model.",
        "What is auto-scaling and how do you configure it?",
        "How do you design disaster recovery in the cloud?",
        "What is a VPC and how do you design network segmentation?",
        "Explain idempotency in cloud architectures.",
        "How do you approach cloud migration?",
        "What are cloud-native design patterns?",
    ],
    "Database Administrator": [
        "How do you optimize a slow SQL query?",
        "What is database normalization and what are the normal forms?",
        "How do you set up database replication?",
        "What is a deadlock and how do you resolve it?",
        "How do you design a backup and recovery strategy?",
        "What are stored procedures and when should you use them?",
        "Explain ACID properties.",
        "How do you monitor database performance?",
        "What is database partitioning and when is it useful?",
        "How do you handle database upgrades with zero downtime?",
    ],
}


class CareerPredictor:
    """Predicts career paths from resume data using trained ML models."""

    def __init__(self):
        self._model_data = None

    def _load_model(self):
        """Lazy-load the trained model."""
        if self._model_data is not None:
            return

        if not os.path.exists(BEST_MODEL_PATH):
            raise FileNotFoundError(
                f"Trained model not found at {BEST_MODEL_PATH}. "
                "Please run: python ml/pipeline.py"
            )
        self._model_data = joblib.load(BEST_MODEL_PATH)

    def _build_feature_vector(self, parsed_data: Dict) -> np.ndarray:
        """Convert parsed resume data to feature vector."""
        self._load_model()
        feature_cols = self._model_data["feature_cols"]
        all_skills = self._model_data.get("all_skills", [])

        skills_lower = [s.lower().replace(" ", "_") for s in parsed_data.get("skills", [])]

        feature_vec = {}
        for col in feature_cols:
            if col in all_skills:
                feature_vec[col] = 1 if col in skills_lower else 0
            elif col == "experience_years":
                feature_vec[col] = len(parsed_data.get("experience", []))
            elif col == "education_level":
                edu = parsed_data.get("education", [])
                level = 0
                if edu:
                    degree_text = edu[0].get("degree", "").lower()
                    if "phd" in degree_text or "doctorate" in degree_text:
                        level = 3
                    elif "master" in degree_text or "m.tech" in degree_text:
                        level = 2
                    elif "bachelor" in degree_text or "b.tech" in degree_text or "b.e" in degree_text:
                        level = 1
                feature_vec[col] = level
            elif col == "num_projects":
                feature_vec[col] = len(parsed_data.get("projects", []))
            elif col == "num_certifications":
                feature_vec[col] = len(parsed_data.get("certifications", []))
            else:
                feature_vec[col] = 0

        return np.array([[feature_vec.get(col, 0) for col in feature_cols]])

    def predict(self, parsed_data: Dict) -> Dict:
        """
        Predict career from parsed resume data.

        Returns:
            dict with predicted_career, confidence, top_careers, interview_questions
        """
        self._load_model()
        model = self._model_data["model"]
        scaler = self._model_data.get("scaler")
        label_encoder = self._model_data["label_encoder"]

        X = self._build_feature_vector(parsed_data)

        if scaler is not None:
            X = scaler.transform(X)

        # Probabilities
        probabilities = model.predict_proba(X)[0]
        classes = label_encoder.classes_

        top_indices = np.argsort(probabilities)[::-1][:5]
        top_careers = [
            {
                "career": classes[i],
                "probability": round(float(probabilities[i]) * 100, 2)
            }
            for i in top_indices
        ]

        predicted_career = top_careers[0]["career"]
        confidence = top_careers[0]["probability"]

        # Get interview questions
        questions = INTERVIEW_QUESTIONS.get(predicted_career, INTERVIEW_QUESTIONS["Software Engineer"])

        return {
            "predicted_career": predicted_career,
            "confidence": confidence,
            "top_careers": top_careers,
            "model_used": self._model_data.get("model_name", "Random Forest"),
            "features_used": self._model_data.get("feature_cols", []),
            "interview_questions": questions,
        }


# Singleton instance
career_predictor = CareerPredictor()
