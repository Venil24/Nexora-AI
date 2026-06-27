# Nexora-AI Project Progress

## Current Status
- **Status**: 🟢 Backend Completed & ML Models Trained
- **Database**: Schemas, Indexes, and Seed Script Created
- **ML Pipeline**: dataset generated, models trained, comparison evaluated, and best model saved
- **Flask API**: Scaffolding, Controllers, Routes, Services, Middlewares completed

---

## Folder Structure
```
Nexora-AI/
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   │   ├── analysis_controller.py
│   │   │   ├── auth_controller.py
│   │   │   ├── career_controller.py
│   │   │   ├── github_controller.py
│   │   │   └── resume_controller.py
│   │   ├── middleware/
│   │   │   ├── auth.py
│   │   │   └── error_handler.py
│   │   ├── routes/
│   │   │   ├── activity_routes.py
│   │   │   ├── analysis_routes.py
│   │   │   ├── auth_routes.py
│   │   │   ├── career_routes.py
│   │   │   ├── github_routes.py
│   │   │   └── resume_routes.py
│   │   ├── services/
│   │   │   ├── email_service.py
│   │   │   ├── github_service.py
│   │   │   └── report_service.py
│   │   └── __init__.py
│   ├── config.py
│   └── run.py
├── database/
│   ├── connection.py
│   ├── crud.py
│   ├── indexes.py
│   ├── schemas.py
│   └── seed.py
├── ml/
│   ├── datasets/
│   │   └── career_dataset.csv
│   ├── trained_models/
│   │   ├── best_model.joblib
│   │   ├── decision_tree.joblib
│   │   ├── evaluation_report.json
│   │   ├── logistic_regression.joblib
│   │   └── random_forest.joblib
│   ├── ats_scorer.py
│   ├── career_predictor.py
│   ├── jd_matcher.py
│   ├── pipeline.py
│   └── resume_parser.py
├── requirements.txt
├── .gitignore
├── .env.example
└── docker-compose.yml
```

---

## Completed Features
- **Scaffolding**: Setup full configuration, `.gitignore`, `.env.example`, `requirements.txt`, `docker-compose.yml`.
- **Database Layer**: Implemented thread-safe connection pooling, index setup, JSON validator schemas, generic and helper CRUD operations, and seeding logic.
- **ML Pipeline**: Created dataset generator, training/evaluation pipeline, resume parser (PyMuPDF + spaCy), ATS score calculator, Job Description semantic matcher, and career predictor.
- **Flask REST API**: Implemented full backend endpoints with modular controllers and routes.
  - JWT auth (Login, Register, Refresh, Forgot/Reset Password, Update Profile).
  - Resume upload and management APIs.
  - ATS scoring, Suggestions, and Job Description matching.
  - Career prediction & roadmap access.
  - GitHub profile fetching & metric evaluation.
  - PDF Report downloading (ReportLab).
  - User activity log tracking.

---

## Database Collections (MongoDB)
- `users`: Core authentication data
- `profiles`: Expanded user bio, skills, targets
- `resumes`: Metadata and parsed resume output
- `analysis`: ATS score breakdown and suggestions
- `career_prediction`: ML model predicted pathways
- `roadmaps`: Interactive path steps
- `github_analysis`: Pulled indicators
- `activity_logs`: User security/audit trails

---

## ML Models
- **Logistic Regression**: Trained (99.9% accuracy) - **Selected as Best Model**
- **Random Forest**: Trained (99.8% accuracy)
- **Decision Tree**: Trained (88.39% accuracy)

---

## APIs
All backend API routes registered under `/api/...`:
- **Auth**: `POST /register`, `POST /login`, `GET /me`, `POST /refresh`, `POST /forgot-password`, `POST /reset-password`, `PUT /profile`
- **Resume**: `POST /upload`, `GET /history`, `GET /stats`, `GET /<resume_id>`, `DELETE /<resume_id>`
- **Analysis**: `POST /<resume_id>/run`, `GET /<resume_id>`, `POST /<resume_id>/jd-match`, `GET /<resume_id>/report`
- **Career**: `POST /predict/<resume_id>`, `GET /roadmaps`, `GET /roadmap/<career>`, `GET /interview-questions/<career>`
- **GitHub**: `GET /<username>`
- **Activity**: `GET /logs`

---

## Pending Tasks
- **Phase 5 — React Frontend**: Scaffold frontend and build components, store, hooks, API integration, and pages.
- **Phase 6 — Final Documentation**: Finalize README.md, SETUP_GUIDE.md, and test integration.
