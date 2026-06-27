# 📡 Nexora-AI REST API Reference

All requests must be sent to `http://localhost:5000/api` (or customized in `.env`).  
Supported headers for authenticated requests:
```http
Authorization: Bearer <your-access-token>
Content-Type: application/json
```

---

## 🔒 Authentication Blueprint (`/auth`)

### 1. Register User
* **Method**: `POST`
* **Path**: `/auth/register`
* **Request Body**:
  ```json
  {
    "name": "Alex Morgan",
    "email": "alex@example.com",
    "password": "SecurePassword@123"
  }
  ```
* **Success Response (201 Created)**:
  ```json
  {
    "status": "success",
    "message": "User registered successfully",
    "data": {
      "user": {
        "id": "60c72b2f9b1d8e1f84542d12",
        "name": "Alex Morgan",
        "email": "alex@example.com",
        "role": "user"
      },
      "access_token": "eyJhbG...",
      "refresh_token": "eyJhbG..."
    }
  }
  ```

### 2. Login User
* **Method**: `POST`
* **Path**: `/auth/login`
* **Request Body**:
  ```json
  {
    "email": "alex@example.com",
    "password": "SecurePassword@123"
  }
  ```
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Login successful",
    "data": {
      "user": {
        "id": "60c72b2f9b1d8e1f84542d12",
        "name": "Alex Morgan",
        "email": "alex@example.com",
        "role": "user"
      },
      "access_token": "eyJhbG...",
      "refresh_token": "eyJhbG..."
    }
  }
  ```

### 3. Get User Profile
* **Method**: `GET`
* **Path**: `/auth/me`
* **Authentication Required**: Yes
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "data": {
      "user": {
        "id": "60c72b2f9b1d8e1f84542d12",
        "name": "Alex Morgan",
        "email": "alex@example.com",
        "role": "user"
      }
    }
  }
  ```

### 4. Refresh Token
* **Method**: `POST`
* **Path**: `/auth/refresh`
* **Authentication Required**: Yes (using Refresh Token)
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "data": {
      "access_token": "eyJhbG_new_access_token..."
    }
  }
  ```

### 5. Update Profile
* **Method**: `PUT`
* **Path**: `/auth/profile`
* **Authentication Required**: Yes
* **Request Body**:
  ```json
  {
    "name": "Alex J. Morgan",
    "phone": "+1234567890",
    "github": "alexmorgan",
    "linkedin": "alex-morgan-linked"
  }
  ```
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Profile updated successfully",
    "data": {
      "user": {
        "id": "60c72b2f9b1d8e1f84542d12",
        "name": "Alex J. Morgan",
        "email": "alex@example.com"
      }
    }
  }
  ```

---

## 📄 Resume Management Blueprint (`/resume`)

### 1. Upload Resume PDF
* **Method**: `POST`
* **Path**: `/resume/upload`
* **Authentication Required**: Yes
* **Request Body**: Multipart form data with a `file` field containing the PDF document.
* **Success Response (201 Created)**:
  ```json
  {
    "status": "success",
    "message": "Resume uploaded and parsed successfully",
    "data": {
      "id": "60c72b2f9b1d8e1f84542d55",
      "filename": "12345678_resume.pdf",
      "original_name": "my_resume.pdf",
      "status": "parsed",
      "page_count": 2,
      "file_size": 250000
    }
  }
  ```

### 2. Get Resume History
* **Method**: `GET`
* **Path**: `/resume/history`
* **Authentication Required**: Yes
* **Query Parameters**: `page` (default 1), `limit` (default 10)
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "data": {
      "resumes": [
        {
          "id": "60c72b2f9b1d8e1f84542d55",
          "original_name": "my_resume.pdf",
          "status": "analyzed",
          "created_at": "2026-06-27T04:00:00Z"
        }
      ],
      "total": 1,
      "page": 1,
      "limit": 10,
      "pages": 1
    }
  }
  ```

### 3. Get Resume Statistics
* **Method**: `GET`
* **Path**: `/resume/stats`
* **Authentication Required**: Yes
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "data": {
      "total_resumes": 1,
      "analyzed": 1,
      "avg_ats_score": 82.5,
      "recent_scores": [82.5]
    }
  }
  ```

---

## 🧠 ATS Analysis Blueprint (`/analysis`)

### 1. Run ATS Analysis
* **Method**: `POST`
* **Path**: `/analysis/<resume_id>/run`
* **Authentication Required**: Yes
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Analysis completed",
    "data": {
      "overall_score": 82.5,
      "ats_score": 85,
      "formatting_score": 90,
      "keyword_score": 75,
      "experience_score": 80,
      "education_score": 85,
      "projects_score": 80,
      "strengths": ["Clear structure", "Parsed contact links"],
      "weaknesses": ["Low action-verb count", "Formatting mismatch"],
      "suggestions": ["Add more metrics to experience items", "Quantify bullet points"]
    }
  }
  ```

### 2. Match Job Description (JD Match)
* **Method**: `POST`
* **Path**: `/analysis/<resume_id>/jd-match`
* **Authentication Required**: Yes
* **Request Body**:
  ```json
  {
    "jd_text": "We are seeking a senior full stack developer with experience in Python Flask, React, and Tailwind CSS..."
  }
  ```
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "data": {
      "match_score": 81.2,
      "semantic_score": 83.4,
      "keyword_overlap": 79.0,
      "matched_skills": ["Python", "Flask", "React"],
      "missing_skills": ["Tailwind CSS", "Docker"],
      "recommendation": "Try expanding experience items with Tailwind CSS and containerization keywords to match this description."
    }
  }
  ```

### 3. Download PDF Report
* **Method**: `GET`
* **Path**: `/analysis/<resume_id>/report`
* **Authentication Required**: Yes
* **Success Response (200 OK)**: Returns the generated binary PDF report as an attachment download (`application/pdf`).

---

## 💼 Career Blueprint (`/career`)

### 1. Predict Career Path
* **Method**: `POST`
* **Path**: `/career/predict/<resume_id>`
* **Authentication Required**: Yes
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Career prediction complete",
    "data": {
      "predicted_career": "Software Engineer",
      "confidence": 99.9,
      "model_used": "Logistic Regression",
      "top_careers": [
        { "career": "Software Engineer", "probability": 99.9 },
        { "career": "Backend Developer", "probability": 0.1 }
      ],
      "detected_skills": ["Python", "Flask", "React", "MongoDB", "SQL"],
      "skills_gap": ["Docker", "Kubernetes", "AWS"]
    }
  }
  ```

### 2. Get Career Roadmap
* **Method**: `GET`
* **Path**: `/career/roadmap/<career_name>`
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "data": {
      "career": "Software Engineer",
      "title": "Software Engineer Learning Path",
      "duration_weeks": 24,
      "difficulty": "Intermediate",
      "avg_salary": "$115,000",
      "skills_to_learn": ["Data Structures", "Algorithms", "System Design"],
      "phases": [
        {
          "phase": "Foundations",
          "duration": "Weeks 1-4",
          "topics": ["Variables", "Control flow", "Data structures"]
        }
      ]
    }
  }
  ```

---

## 🐙 GitHub Analyzer Blueprint (`/github`)

### 1. Fetch GitHub Metrics
* **Method**: `GET`
* **Path**: `/github/<username>`
* **Authentication Required**: Yes
* **Success Response (200 OK)**:
  ```json
  {
    "status": "success",
    "data": {
      "profile": {
        "name": "Alex Developer",
        "bio": "Building SaaS platforms...",
        "avatar_url": "https://avatars...",
        "html_url": "https://github.com/alexdev"
      },
      "total_repos": 35,
      "followers": 120,
      "total_stars": 45,
      "total_forks": 12,
      "skill_score": 85.0,
      "activity_score": 75.0,
      "languages": {
        "JavaScript": 15,
        "Python": 12,
        "HTML": 5
      },
      "top_repos": [
        {
          "name": "nextjs-saas-template",
          "stars": 25,
          "language": "JavaScript"
        }
      ]
    }
  }
  ```
