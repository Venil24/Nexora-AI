# 🧠 Nexora-AI — AI Resume Analyzer & Career Roadmap

Nexora AI is a production-ready, full-stack SaaS platform designed to parse resumes, analyze ATS compatibility across multiple dimensions, predict career trajectories using ML models, construct tailored roadmap guides, and evaluate developer profiles via GitHub APIs.

---

## 🎨 Premium Features

- 🔐 **Secure Session Auth**: JWT validation including auto-refresh tokens.
- 📄 **Deep Resume Parser**: Text, links, and Name Entity Recognition extraction using PyMuPDF and spaCy models.
- 🛡️ **ATS Optimization Reviewer**: Checks spacing, formats, section labels, action verb usage, and highlights keyword discrepancies.
- 🤝 **Job Description Matcher**: Utilizes NLP similarity matching to score alignment vs specific JD postings.
- 🎯 **ML Career Predictor**: Deploys a trained Logistic Regression classifier (99.9% accuracy) comparing skills to identify ideal matching developer tracks.
- 🗺️ **Learning Path Roadmaps**: Renders interactive, week-by-week roadmaps complete with reference resources and learning materials.
- 🐙 **GitHub Metric Calculator**: Gathers profile data, repository stars, forks, and language statistics to generate skills ratings.
- 📈 **Audits & Logging**: Records security metrics, login IPs, user agents, and transaction logs.
- 📥 **PDF Report Generator**: Compiles metrics and lists into high-quality PDF report downloads using ReportLab templates.

---

## 💻 Technology Stack

### Backend
- **Core**: Python 3.10+, Flask 3.0+
- **Database**: MongoDB Atlas, PyMongo
- **NLP & Parser**: spaCy (`en_core_web_sm`), NLTK, PyMuPDF
- **ML Engine**: Scikit-learn, Pandas, NumPy, Joblib
- **Report Engine**: ReportLab PDF
- **Security**: Flask-JWT-Extended, BCrypt, CORS

### Frontend
- **Framework**: React 19, Vite 8, React Router v6
- **Styling**: Tailwind CSS v3, PostCSS, Lucide Icons
- **State Management**: Zustand
- **Animations**: Framer Motion
- **Visual Charts**: Chart.js (`react-chartjs-2`)
- **Client**: Axios

---

## 🚀 Fast Setup

Ensure Python 3.10+ and Node.js 18+ are installed. For step-by-step guidance on creating a free MongoDB cluster and setting up environment parameters, review the [SETUP_GUIDE.md](file:///c:/Users/SHAH%20VENIL/Downloads/devfusion/Nexora-AI/SETUP_GUIDE.md).

### 1. Initialize Configuration
```bash
copy .env.example .env
# Edit .env with your MongoDB cluster URI & GITHUB_TOKEN
```

### 2. Backend Installation & Startup
```bash
# Create and activate environment
python -m venv venv
venv\Scripts\activate

# Install libraries & download model databases
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Train Career Prediction ML Models
python -X utf8 ml/pipeline.py

# Seed initial collections
python -X utf8 database/seed.py

# Start Server
cd backend
python -X utf8 run.py
```
*Backend is listening at:* http://localhost:5000

---

### 3. Frontend Installation & Startup
```bash
# In a new command prompt
cd Nexora-AI/frontend
npm install
npm run dev
```
*Frontend is listening at:* http://localhost:5173

---

## 📄 Key Files Reference

- **[SETUP_GUIDE.md](file:///c:/Users/SHAH%20VENIL/Downloads/devfusion/Nexora-AI/SETUP_GUIDE.md)**: Extended setup manual, screenshots, and common issue resolutions.
- **[PROJECT_PROGRESS.md](file:///c:/Users/SHAH%20VENIL/Downloads/devfusion/Nexora-AI/docs/PROJECT_PROGRESS.md)**: Features completed tracker and directory maps.
- **[API_REFERENCE.md](file:///c:/Users/SHAH%20VENIL/Downloads/devfusion/Nexora-AI/docs/API_REFERENCE.md)**: Comprehensive JSON routes document listing body shapes.
