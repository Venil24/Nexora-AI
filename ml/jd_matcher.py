"""
ml/jd_matcher.py
Job Description matching using Sentence Transformers for semantic similarity.
Computes similarity score, matched skills, missing skills, and keyword gaps.
"""
import re
from typing import Dict, List, Tuple, Optional
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Lazy-loaded model
_sentence_model = None

def get_sentence_model():
    """Lazy-load the sentence transformer model."""
    global _sentence_model
    if _sentence_model is None:
        _sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _sentence_model


# Common technical skills for extraction
TECH_SKILLS_PATTERNS = [
    r'\b(?:python|java|javascript|typescript|c\+\+|c#|golang|rust|ruby|php|scala|kotlin|swift|r)\b',
    r'\b(?:react|angular|vue|next\.?js|svelte|html5?|css3?|sass|tailwind|bootstrap|jquery)\b',
    r'\b(?:node\.?js|flask|django|fastapi|spring|express|laravel|rails|fastify|nestjs)\b',
    r'\b(?:sql|mysql|postgresql|sqlite|mongodb|redis|elasticsearch|cassandra|dynamodb|firebase)\b',
    r'\b(?:aws|gcp|azure|docker|kubernetes|terraform|ansible|jenkins|ci\/cd|github actions)\b',
    r'\b(?:machine learning|deep learning|tensorflow|pytorch|scikit-learn|pandas|numpy|nlp)\b',
    r'\b(?:git|github|gitlab|jira|agile|scrum|devops|microservices|rest api|graphql)\b',
    r'\b(?:linux|bash|shell|powershell|networking|security|oauth|jwt|ssl|tls)\b',
]

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "shall", "you", "we", "our",
    "their", "this", "that", "these", "those", "it", "its", "they", "them",
    "your", "his", "her", "he", "she", "who", "which", "what", "when", "where",
    "how", "why", "not", "no", "nor", "so", "yet", "both", "either", "neither",
    "each", "few", "more", "most", "other", "some", "such", "than", "too",
    "very", "just", "also", "about", "above", "after", "before", "during",
    "between", "through", "under", "over", "into", "onto", "upon",
    "experience", "ability", "skills", "knowledge", "understanding",
    "candidate", "position", "role", "opportunity", "team", "work",
    "job", "responsibilities", "requirements", "qualifications",
}


def extract_skills_from_text(text: str) -> List[str]:
    """Extract technical skills from text using regex patterns."""
    text_lower = text.lower()
    found = set()
    for pattern in TECH_SKILLS_PATTERNS:
        matches = re.findall(pattern, text_lower)
        found.update(matches)
    return list(found)


def extract_keywords(text: str, top_n: int = 30) -> List[str]:
    """Extract important keywords from text (non-stopwords, length > 2)."""
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.]*\b', text.lower())
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 2]

    # Frequency-based ranking
    freq = {}
    for w in keywords:
        freq[w] = freq.get(w, 0) + 1

    sorted_kw = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_kw[:top_n]]


class JDMatcher:
    """Matches resume against job description using semantic similarity."""

    def compute_similarity(self, resume_text: str, jd_text: str) -> float:
        """Compute cosine similarity between resume and JD using sentence transformers."""
        model = get_sentence_model()

        # Encode both texts
        resume_embedding = model.encode(resume_text[:2000], convert_to_tensor=True)
        jd_embedding = model.encode(jd_text[:2000], convert_to_tensor=True)

        similarity = util.cos_sim(resume_embedding, jd_embedding).item()
        # Convert to percentage (0-100)
        return round(max(0.0, min(100.0, similarity * 100)), 1)

    def analyze_skill_gap(
        self,
        resume_skills: List[str],
        jd_text: str
    ) -> Tuple[List[str], List[str]]:
        """
        Compare resume skills vs JD required skills.
        Returns (matched_skills, missing_skills).
        """
        resume_skills_lower = {s.lower() for s in resume_skills}
        jd_skills = extract_skills_from_text(jd_text)

        matched = []
        missing = []

        for skill in jd_skills:
            skill_lower = skill.lower()
            # Check if resume contains this skill or a variant
            if skill_lower in resume_skills_lower or any(
                skill_lower in rs or rs in skill_lower
                for rs in resume_skills_lower
            ):
                matched.append(skill.title())
            else:
                missing.append(skill.title())

        return sorted(set(matched)), sorted(set(missing))

    def match(self, resume_data: Dict, jd_text: str) -> Dict:
        """
        Full JD matching analysis.

        Args:
            resume_data: Parsed resume data dict
            jd_text: Raw job description text

        Returns:
            dict with similarity score, matched skills, missing skills, keywords
        """
        if not jd_text or not jd_text.strip():
            return {
                "similarity_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "jd_keywords": [],
                "resume_keywords": [],
                "recommendation": "Please provide a job description to analyze.",
            }

        resume_text = resume_data.get("raw_text", "")
        resume_skills = resume_data.get("skills", [])

        # Semantic similarity
        similarity = self.compute_similarity(resume_text, jd_text)

        # Skill gap analysis
        matched_skills, missing_skills = self.analyze_skill_gap(resume_skills, jd_text)

        # Keyword extraction
        jd_keywords = extract_keywords(jd_text, top_n=20)
        resume_keywords = extract_keywords(resume_text, top_n=20)

        # Generate recommendation
        if similarity >= 80:
            recommendation = "Excellent match! Your resume strongly aligns with this job description."
        elif similarity >= 60:
            recommendation = "Good match. Consider adding the missing skills to strengthen your application."
        elif similarity >= 40:
            recommendation = "Moderate match. Work on gaining and showcasing the required skills listed below."
        else:
            recommendation = "Low match. Significantly upskill in the required areas before applying."

        # Skill match percentage
        total_jd_skills = len(matched_skills) + len(missing_skills)
        skill_match_pct = round(
            (len(matched_skills) / total_jd_skills * 100) if total_jd_skills > 0 else 0,
            1
        )

        return {
            "similarity_score": similarity,
            "skill_match_percentage": skill_match_pct,
            "matched_skills": matched_skills[:20],
            "missing_skills": missing_skills[:20],
            "jd_keywords": jd_keywords[:15],
            "resume_keywords": resume_keywords[:15],
            "recommendation": recommendation,
            "total_jd_skills": total_jd_skills,
            "matched_count": len(matched_skills),
            "missing_count": len(missing_skills),
        }


# Singleton instance
jd_matcher = JDMatcher()
