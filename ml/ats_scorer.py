"""
ml/ats_scorer.py
ATS (Applicant Tracking System) resume scoring engine.
Scores resumes across 6 dimensions and provides actionable suggestions.
"""
import re
from typing import Dict, List, Tuple, Optional


# ── Scoring weights ────────────────────────────────────────────────────────────
WEIGHTS = {
    "ats": 0.25,
    "formatting": 0.15,
    "keywords": 0.20,
    "experience": 0.20,
    "education": 0.10,
    "projects": 0.10,
}

# ── ATS-Friendly checks ────────────────────────────────────────────────────────
ATS_KEYWORDS = [
    "results", "achieved", "improved", "managed", "developed", "designed",
    "implemented", "led", "increased", "reduced", "delivered", "collaborated",
    "optimized", "automated", "built", "created", "launched", "maintained",
]

REQUIRED_SECTIONS = ["email", "phone", "education", "experience", "skills"]

POWER_VERBS = {
    "leadership": ["led", "managed", "directed", "supervised", "coordinated", "guided"],
    "technical": ["developed", "built", "implemented", "designed", "engineered", "architected"],
    "impact": ["improved", "increased", "reduced", "optimized", "accelerated", "scaled"],
    "collaboration": ["collaborated", "partnered", "mentored", "trained", "supported"],
}

FORMATTING_RED_FLAGS = [
    "table", "textbox", "text box", "header", "footer",
    "watermark", "image", "photo", "picture", "graphic",
]

QUANTIFIED_PATTERN = re.compile(r'\b\d+[\+%x]?\s*(?:users|clients|customers|engineers|team|members|projects|years|months|weeks|hours|dollars|million|thousand|k)\b', re.IGNORECASE)


class ATSScorer:
    """Scores resumes on multiple dimensions for ATS compatibility."""

    def score_ats_compatibility(self, parsed_data: Dict, raw_text: str) -> Tuple[float, List[str]]:
        """Score ATS compatibility (parsing friendliness)."""
        score = 100.0
        issues = []
        raw_lower = raw_text.lower()

        # Check for required contact info
        if not parsed_data.get("email"):
            score -= 15
            issues.append("Missing email address — critical for ATS contact parsing")
        if not parsed_data.get("phone"):
            score -= 10
            issues.append("Missing phone number — required for recruiter follow-up")
        if not parsed_data.get("name"):
            score -= 15
            issues.append("Name not detected at top of resume")

        # Check for required sections
        if not parsed_data.get("experience"):
            score -= 15
            issues.append("Work experience section missing or not recognized")
        if not parsed_data.get("education"):
            score -= 10
            issues.append("Education section missing or not recognized")
        if not parsed_data.get("skills"):
            score -= 15
            issues.append("Skills section missing — ATS systems heavily rely on skills keywords")

        # Check file length (ATS prefers 1-2 pages)
        page_count = parsed_data.get("page_count", 1)
        if page_count > 2:
            score -= 5
            issues.append(f"Resume is {page_count} pages — keep it to 1-2 pages for ATS")
        elif page_count == 0:
            score -= 20
            issues.append("Could not read resume pages — check PDF format")

        # Check for formatting red flags in text
        for flag in FORMATTING_RED_FLAGS:
            if flag in raw_lower[:200]:
                score -= 3
                issues.append(f"Possible complex formatting detected ('{flag}') — may confuse ATS")
                break

        # Bonus for LinkedIn/GitHub
        if parsed_data.get("linkedin"):
            score = min(100, score + 3)
        if parsed_data.get("github"):
            score = min(100, score + 2)

        return max(0.0, round(score, 1)), issues

    def score_formatting(self, parsed_data: Dict, raw_text: str) -> Tuple[float, List[str]]:
        """Score resume formatting quality."""
        score = 70.0
        suggestions = []

        # Action verbs / power verbs
        raw_lower = raw_text.lower()
        found_power_verbs = 0
        for category, verbs in POWER_VERBS.items():
            if any(re.search(r'\b' + v + r'\b', raw_lower) for v in verbs):
                found_power_verbs += 1

        if found_power_verbs >= 3:
            score += 15
        elif found_power_verbs >= 1:
            score += 8
        else:
            suggestions.append("Use strong action verbs (led, built, improved, designed) to start bullet points")

        # Quantified achievements
        quantified = QUANTIFIED_PATTERN.findall(raw_text)
        if len(quantified) >= 4:
            score += 15
            score = min(score, 100)
        elif len(quantified) >= 2:
            score += 8
        else:
            suggestions.append("Quantify your achievements with numbers (e.g., 'Improved load time by 40%', 'Led team of 5')")

        # Summary presence
        if parsed_data.get("summary"):
            score = min(100, score + 5)
        else:
            suggestions.append("Add a professional summary/objective at the top of your resume")

        # Consistent formatting check (check for uniform bullet points)
        bullet_chars = len(re.findall(r'^[•\-*✓▸→►]', raw_text, re.MULTILINE))
        if bullet_chars >= 5:
            score = min(100, score + 5)
        else:
            suggestions.append("Use consistent bullet points (•, -, *) for experience and project descriptions")

        return max(0.0, min(100.0, round(score, 1))), suggestions

    def score_keywords(self, parsed_data: Dict, raw_text: str) -> Tuple[float, List[str]]:
        """Score keyword density and relevance."""
        score = 50.0
        suggestions = []
        raw_lower = raw_text.lower()

        # Count ATS keywords
        found_keywords = [kw for kw in ATS_KEYWORDS if re.search(r'\b' + kw + r'\b', raw_lower)]
        keyword_ratio = len(found_keywords) / len(ATS_KEYWORDS)
        score += keyword_ratio * 30

        # Skills count bonus
        skills = parsed_data.get("skills", [])
        if len(skills) >= 15:
            score += 20
        elif len(skills) >= 10:
            score += 15
        elif len(skills) >= 5:
            score += 8
        else:
            suggestions.append("Add more relevant technical skills to your Skills section")

        if len(skills) < 10:
            suggestions.append(f"List at least 10-15 skills. Currently detected: {len(skills)}")

        if keyword_ratio < 0.3:
            suggestions.append("Use more action verbs like: achieved, implemented, developed, optimized")

        return max(0.0, min(100.0, round(score, 1))), suggestions

    def score_experience(self, parsed_data: Dict, raw_text: str) -> Tuple[float, List[str]]:
        """Score work experience quality."""
        score = 30.0
        suggestions = []

        experience = parsed_data.get("experience", [])
        exp_count = len(experience)

        if exp_count >= 3:
            score += 40
        elif exp_count == 2:
            score += 30
        elif exp_count == 1:
            score += 20
        else:
            score += 0
            suggestions.append("Add your work experience with job titles, company names, and dates")

        # Check for dates in experience
        has_dates = any(e.get("duration") for e in experience)
        if has_dates:
            score += 15
        else:
            suggestions.append("Add date ranges to each experience entry (e.g., Jan 2022 - Present)")

        # Descriptions quality
        has_descriptions = any(e.get("description") for e in experience)
        if has_descriptions:
            score += 15
        else:
            suggestions.append("Add bullet-point descriptions for each role describing your responsibilities and achievements")

        # Quantified impact
        raw_lower = raw_text.lower()
        if re.search(r'\d+\s*(?:%|percent|million|thousand|k)', raw_lower):
            score = min(100, score + 10)
        else:
            suggestions.append("Include quantifiable impact in your experience (%, $, numbers)")

        return max(0.0, min(100.0, round(score, 1))), suggestions

    def score_education(self, parsed_data: Dict) -> Tuple[float, List[str]]:
        """Score education section."""
        score = 30.0
        suggestions = []

        education = parsed_data.get("education", [])

        if not education:
            suggestions.append("Add your education section with degree, institution, and graduation year")
            return score, suggestions

        score += 40  # Has education

        for edu in education:
            if edu.get("year"):
                score = min(100, score + 10)
                break
        else:
            suggestions.append("Add graduation year to your education entries")

        for edu in education:
            if edu.get("institution"):
                score = min(100, score + 10)
                break

        # GPA bonus
        for edu in education:
            if edu.get("gpa"):
                score = min(100, score + 10)
                break

        return max(0.0, min(100.0, round(score, 1))), suggestions

    def score_projects(self, parsed_data: Dict) -> Tuple[float, List[str]]:
        """Score projects section."""
        score = 20.0
        suggestions = []

        projects = parsed_data.get("projects", [])
        proj_count = len(projects)

        if proj_count >= 4:
            score += 60
        elif proj_count == 3:
            score += 50
        elif proj_count == 2:
            score += 35
        elif proj_count == 1:
            score += 20
        else:
            suggestions.append("Add 2-4 notable projects with titles, tech stack, and links")
            return score, suggestions

        # Projects with URLs
        with_urls = sum(1 for p in projects if p.get("url"))
        if with_urls >= 2:
            score = min(100, score + 20)
        elif with_urls == 1:
            score = min(100, score + 10)
        else:
            suggestions.append("Add GitHub or live links to your projects for verification")

        # Projects with tech
        with_tech = sum(1 for p in projects if p.get("technologies"))
        if with_tech < proj_count:
            suggestions.append("List the technologies used for each project")

        return max(0.0, min(100.0, round(score, 1))), suggestions

    def generate_strengths_weaknesses(self, scores: Dict) -> Tuple[List[str], List[str]]:
        """Generate strengths and weaknesses based on scores."""
        strengths = []
        weaknesses = []

        thresholds = {
            "ats": ("ATS-compatible format", "Poor ATS compatibility — many ATS may reject this resume"),
            "formatting": ("Well-formatted with strong action verbs", "Weak formatting — missing quantification and structure"),
            "keywords": ("Strong keyword optimization", "Low keyword density — add more relevant technical terms"),
            "experience": ("Strong work experience section", "Work experience needs improvement"),
            "education": ("Clear education background", "Education section incomplete"),
            "projects": ("Good project portfolio", "Limited project showcase"),
        }

        for key, (strength_msg, weakness_msg) in thresholds.items():
            if scores.get(key, 0) >= 70:
                strengths.append(strength_msg)
            elif scores.get(key, 0) < 50:
                weaknesses.append(weakness_msg)

        return strengths, weaknesses

    def score(self, parsed_data: Dict, raw_text: str = "") -> Dict:
        """
        Run full ATS scoring on a parsed resume.

        Returns:
            dict with all scores, suggestions, strengths, weaknesses
        """
        raw_text = raw_text or parsed_data.get("raw_text", "")

        ats_score, ats_issues = self.score_ats_compatibility(parsed_data, raw_text)
        fmt_score, fmt_suggestions = self.score_formatting(parsed_data, raw_text)
        kw_score, kw_suggestions = self.score_keywords(parsed_data, raw_text)
        exp_score, exp_suggestions = self.score_experience(parsed_data, raw_text)
        edu_score, edu_suggestions = self.score_education(parsed_data)
        proj_score, proj_suggestions = self.score_projects(parsed_data)

        scores = {
            "ats": ats_score,
            "formatting": fmt_score,
            "keywords": kw_score,
            "experience": exp_score,
            "education": edu_score,
            "projects": proj_score,
        }

        overall = round(
            sum(scores[k] * WEIGHTS[k] for k in WEIGHTS),
            1
        )

        all_suggestions = ats_issues + fmt_suggestions + kw_suggestions + exp_suggestions + edu_suggestions + proj_suggestions
        # Deduplicate and limit
        seen = set()
        unique_suggestions = []
        for s in all_suggestions:
            if s not in seen:
                seen.add(s)
                unique_suggestions.append(s)

        strengths, weaknesses = self.generate_strengths_weaknesses(scores)

        return {
            "ats_score": ats_score,
            "formatting_score": fmt_score,
            "keyword_score": kw_score,
            "experience_score": exp_score,
            "education_score": edu_score,
            "projects_score": proj_score,
            "overall_score": overall,
            "suggestions": unique_suggestions[:15],
            "strengths": strengths,
            "weaknesses": weaknesses,
        }


# Singleton instance
ats_scorer = ATSScorer()
