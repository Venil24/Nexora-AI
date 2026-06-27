# 🚀 Nexora-AI — Complete Setup Guide

> **AI Resume Analyzer & Career Roadmap** — Production-ready Full Stack SaaS  
> Stack: React + Vite + TailwindCSS | Python Flask | MongoDB Atlas | Scikit-learn + spaCy

---

## 📋 Prerequisites — What You Need to Download

### 1. Python 3.10+
- **Download**: https://www.python.org/downloads/
- Choose `Windows Installer (64-bit)` for Python 3.10.x or newer
- ✅ During install, check **"Add Python to PATH"**
- Verify: `python --version`

### 2. Node.js 18+ (LTS)
- **Download**: https://nodejs.org/en/download/
- Choose the **LTS** version (18.x or 20.x)
- ✅ npm is bundled automatically
- Verify: `node --version` and `npm --version`

### 3. Git
- **Download**: https://git-scm.com/download/win
- Use default install settings
- Verify: `git --version`

### 4. MongoDB Atlas (Cloud — Free Tier)
- **Sign Up**: https://www.mongodb.com/cloud/atlas/register
- Create a **Free Shared Cluster (M0)**
- Steps:
  1. Create account → Create Organization → Create Project
  2. Click **"Build a Database"** → Select **Free M0** → Choose cloud provider region
  3. Create a **Database User** (username + password)
  4. Under **Network Access** → Add IP Address → **"Allow access from anywhere"** (0.0.0.0/0)
  5. Click **Connect** → **Connect your application** → Copy the connection string
  6. It looks like: `mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/nexora_ai`

### 5. GitHub Personal Access Token (Optional — for GitHub Analyzer)
- Go to: https://github.com/settings/tokens
- Click **"Generate new token (classic)"**
- Select scopes: `read:user`, `repo` (public_repo)
- Copy the token — it starts with `ghp_`

---

## 📁 Project Structure

```
Nexora-AI/
├── backend/                  # Flask REST API
│   ├── app/
│   │   ├── controllers/      # Business logic
│   │   ├── middleware/       # JWT auth, error handling
│   │   ├── routes/           # API route blueprints
│   │   └── services/         # Email, GitHub, PDF report
│   ├── config.py
│   └── run.py
├── database/                 # MongoDB connection & schemas
├── docs/                     # Documentation
├── frontend/                 # React + Vite app
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Full page views
│   │   ├── services/         # Axios API calls
│   │   ├── store/            # Zustand state (auth, theme)
│   │   └── hooks/            # Custom React hooks
│   └── package.json
├── ml/                       # Machine learning pipeline
│   ├── trained_models/       # Saved ML model files
│   ├── datasets/             # Training data
│   ├── pipeline.py           # Train models
│   ├── resume_parser.py      # PDF extraction + NER
│   ├── ats_scorer.py         # ATS score calculator
│   ├── career_predictor.py   # Career ML predictor
│   └── jd_matcher.py         # JD semantic matcher
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── docker-compose.yml        # Docker deployment config
```

---

## ⚙️ Setup Instructions

### Step 1 — Clone / Navigate to the Project

```bash
# If cloning from git:
git clone <your-repo-url>
cd Nexora-AI

# Or if you already have the project:
cd path/to/Nexora-AI
```

---

### Step 2 — Configure Environment Variables

```bash
# Copy the example file
copy .env.example .env
```

Open `.env` in any text editor and fill in:

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
SECRET_KEY=my-super-secret-key-change-me-in-production-32chars

# JWT
JWT_SECRET_KEY=my-jwt-secret-key-change-me-in-production-32chars
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# MongoDB Atlas (paste your connection string here)
MONGO_URI=mongodb+srv://myuser:mypassword@cluster0.abcde.mongodb.net/nexora_ai?retryWrites=true&w=majority
MONGO_DB_NAME=nexora_ai

# GitHub (optional)
GITHUB_TOKEN=ghp_your_token_here

# Email (optional — for password reset emails)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_gmail@gmail.com
MAIL_PASSWORD=your_gmail_app_password

# Frontend
FRONTEND_URL=http://localhost:5173
```

> **Gmail App Password**: Go to https://myaccount.google.com/apppasswords, enable 2FA first, then generate an app password for "Mail".

---

### Step 3 — Backend Setup (Python)

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install all Python dependencies
pip install -r requirements.txt

# Download spaCy English model (for resume NER parsing)
python -m spacy download en_core_web_sm

# Download NLTK data (stopwords)
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

---

### Step 4 — Train ML Models

```bash
# From the project root (Nexora-AI/)
# Make sure venv is active

python -X utf8 ml/pipeline.py
```

This will:
- ✅ Generate a synthetic training dataset (`ml/datasets/career_dataset.csv`)
- ✅ Train 3 models: Random Forest, Decision Tree, Logistic Regression
- ✅ Evaluate and compare all models
- ✅ Save the best model to `ml/trained_models/best_model.joblib`

Expected output:
```
Nexora-AI Career Prediction ML Pipeline
Step 1: Loading dataset...
Step 2: Preparing features...
Step 3: Splitting data (80/20)...
Step 4: Training models...
  Random Forest: Accuracy=99.80%
  Decision Tree: Accuracy=88.39%
  Logistic Regression: Accuracy=99.90%
Step 5: Best model saved: Logistic Regression (99.9%)
```

---

### Step 5 — Seed the Database (Optional but Recommended)

```bash
# Seeds the database with sample roadmaps, career paths, and test user
python -X utf8 database/seed.py
```

This populates all 8 MongoDB collections with sample data.

---

### Step 6 — Start the Flask Backend

```bash
# Navigate to backend directory
cd backend

# Start the server (make sure venv is still active)
python run.py
```

Backend runs at: **http://localhost:5000**

Health check: http://localhost:5000/api/health

```json
{ "status": "ok", "service": "Nexora-AI API", "version": "1.0.0" }
```

> Leave this terminal running. Open a second terminal for the frontend.

---

### Step 7 — Frontend Setup (React + Vite)

Open a **new terminal**:

```bash
# Navigate to frontend
cd Nexora-AI/frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

Frontend runs at: **http://localhost:5173**

---

## ✅ Verification Checklist

After completing setup, verify everything works:

| Check | URL | Expected |
|-------|-----|----------|
| Backend Health | http://localhost:5000/api/health | `{"status": "ok"}` |
| Frontend App | http://localhost:5173 | Nexora AI login page |
| Register User | POST /api/auth/register | Returns JWT tokens |
| Upload Resume | POST /api/resume/upload | Resume parsed |
| ATS Analysis | POST /api/analysis/{id}/run | Score returned |

---

## 🧪 Quick API Test (using curl)

```bash
# Register a new user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Test User\", \"email\": \"test@test.com\", \"password\": \"Test@1234\"}"

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"test@test.com\", \"password\": \"Test@1234\"}"
```

---

## 🐳 Docker Setup (Alternative — Full Stack in One Command)

Requires **Docker Desktop**: https://www.docker.com/products/docker-desktop/

```bash
# From project root — starts backend, frontend, MongoDB
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:5000

---

## 🔧 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `FLASK_ENV` | ✅ | `development` or `production` |
| `SECRET_KEY` | ✅ | Flask session secret (32+ chars) |
| `JWT_SECRET_KEY` | ✅ | JWT signing secret (32+ chars) |
| `MONGO_URI` | ✅ | MongoDB Atlas connection string |
| `MONGO_DB_NAME` | ✅ | Database name (e.g. `nexora_ai`) |
| `GITHUB_TOKEN` | ⚠️ Optional | GitHub PAT for GitHub Analyzer |
| `MAIL_SERVER` | ⚠️ Optional | SMTP server (for reset emails) |
| `MAIL_USERNAME` | ⚠️ Optional | SMTP email address |
| `MAIL_PASSWORD` | ⚠️ Optional | SMTP app password |
| `FRONTEND_URL` | ✅ | Frontend base URL for CORS |

---

## 🛠️ Common Issues & Fixes

### ❌ `MONGO_URI not set` warning
**Fix**: Make sure you created `.env` from `.env.example` and filled in your MongoDB Atlas connection string. The backend starts anyway but DB operations will fail.

### ❌ `ModuleNotFoundError: No module named 'spacy'`
**Fix**: Virtual environment is not activated. Run `venv\Scripts\activate` first.

### ❌ `UnicodeEncodeError` on Windows when running pipeline.py
**Fix**: Use `python -X utf8 ml/pipeline.py` instead of `python ml/pipeline.py`

### ❌ `en_core_web_sm not found`
**Fix**: Run `python -m spacy download en_core_web_sm`

### ❌ Frontend `CORS` errors in browser console
**Fix**: Ensure Flask backend is running on port 5000. Check `.env` has `FRONTEND_URL=http://localhost:5173`

### ❌ MongoDB Atlas connection refused
**Fix**: In Atlas → Network Access → Add your IP or use `0.0.0.0/0` for open access. Check your username/password in the URI.

---

## 📦 Tech Stack Reference

| Layer | Technology |
|-------|------------|
| Frontend | React 19, Vite 8, TailwindCSS 3, Framer Motion, Chart.js, Zustand |
| Backend | Python 3.10, Flask 3.0, Flask-JWT-Extended, Flask-CORS |
| Database | MongoDB Atlas (Cloud), PyMongo |
| ML | Scikit-learn, spaCy, NLTK, PyMuPDF, Sentence Transformers |
| Report | ReportLab (PDF generation) |
| Auth | JWT (access + refresh tokens), bcrypt |

---

## 📞 Support

If you encounter any issues not covered above, check:
1. `backend/app/` — Flask logs in terminal
2. `ml/trained_models/evaluation_report.json` — ML model metrics
3. Browser DevTools Console — Frontend errors
