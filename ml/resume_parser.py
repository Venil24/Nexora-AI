"""
ml/resume_parser.py
Extracts structured data from PDF resumes using PyMuPDF, spaCy, and regex.
"""
import re
import os
import fitz  # PyMuPDF
import spacy
import nltk
from typing import Dict, List, Optional

# Download required NLTK resources
for resource in ["punkt", "averaged_perceptron_tagger", "stopwords", "maxent_ne_chunker", "words"]:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass

# Load spaCy model (fall back to smaller model if lg not available)
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        from spacy.lang.en import English
        nlp = English()

# ── Regex patterns ─────────────────────────────────────────────────────────────
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_PATTERN = re.compile(r'''
    (?:
        \+?1?[-.\s]?
        (?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})
        |
        \+\d{1,3}[-.\s]?\d{6,12}
    )
''', re.VERBOSE)
GITHUB_PATTERN = re.compile(r'(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9_-]+)', re.IGNORECASE)
LINKEDIN_PATTERN = re.compile(r'(?:https?://)?(?:www\.)?linkedin\.com/in/([a-zA-Z0-9_-]+)', re.IGNORECASE)
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')

# ── Section headers ────────────────────────────────────────────────────────────
SECTION_HEADERS = {
    "education": ["education", "academic", "qualification", "degree", "university", "college"],
    "experience": ["experience", "work history", "employment", "professional experience", "career history"],
    "skills": ["skills", "technical skills", "competencies", "technologies", "expertise", "proficiencies"],
    "projects": ["projects", "personal projects", "academic projects", "portfolio", "work samples"],
    "certifications": ["certification", "certifications", "licenses", "credentials", "courses"],
    "summary": ["summary", "profile", "objective", "about me", "overview", "professional summary"],
    "achievements": ["achievements", "awards", "honors", "accomplishments"],
}

# ── Common skills dictionary ───────────────────────────────────────────────────
KNOWN_SKILLS = {
    # Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "r", "ruby",
    "php", "swift", "kotlin", "go", "rust", "scala", "perl", "matlab",
    # Frontend
    "react", "angular", "vue", "nextjs", "next.js", "svelte", "html", "css",
    "sass", "less", "tailwind", "tailwindcss", "bootstrap", "jquery", "webpack", "vite",
    # Backend
    "node", "nodejs", "node.js", "flask", "django", "fastapi", "spring", "express",
    "laravel", "rails", "asp.net", "graphql", "rest", "grpc",
    # Databases
    "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis", "elasticsearch",
    "cassandra", "dynamodb", "firebase", "supabase", "oracle", "mssql",
    # Cloud & DevOps
    "aws", "gcp", "azure", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "github actions", "ci/cd", "linux", "bash", "shell",
    # ML/AI
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "sklearn", "keras", "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "nlp", "computer vision", "openai", "langchain", "hugging face",
    # Tools
    "git", "github", "gitlab", "jira", "confluence", "figma", "postman",
    "swagger", "vs code", "intellij", "xcode", "android studio",
    # Other
    "agile", "scrum", "devops", "microservices", "kafka", "rabbitmq",
    "spark", "hadoop", "airflow", "tableau", "power bi", "excel",
}

EDUCATION_DEGREES = [
    "bachelor", "b.tech", "b.e", "b.sc", "b.com", "bca", "bba",
    "master", "m.tech", "m.e", "m.sc", "mca", "mba",
    "phd", "ph.d", "doctorate", "associate", "diploma", "high school",
    "b.s.", "m.s.", "b.a.", "m.a.", "b.eng", "m.eng",
]


class ResumeParser:
    """Extracts structured information from PDF resumes."""

    def extract_text_from_pdf(self, file_path: str) -> tuple[str, int]:
        """Extract raw text and page count from PDF."""
        try:
            doc = fitz.open(file_path)
            pages = []
            for page in doc:
                text = page.get_text("text")
                pages.append(text)
            doc.close()
            return "\n".join(pages), len(pages)
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {e}")

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address."""
        matches = EMAIL_PATTERN.findall(text)
        return matches[0] if matches else None

    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number."""
        matches = PHONE_PATTERN.findall(text)
        if matches:
            phone = re.sub(r'[^\d+\-\(\)]', '', matches[0])
            return phone if len(phone) >= 10 else None
        return None

    def extract_github(self, text: str) -> Optional[str]:
        """Extract GitHub profile URL."""
        match = GITHUB_PATTERN.search(text)
        if match:
            return f"https://github.com/{match.group(1)}"
        return None

    def extract_linkedin(self, text: str) -> Optional[str]:
        """Extract LinkedIn profile URL."""
        match = LINKEDIN_PATTERN.search(text)
        if match:
            return f"https://linkedin.com/in/{match.group(1)}"
        return None

    def extract_name(self, text: str) -> Optional[str]:
        """Extract candidate name using spaCy NER."""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if not lines:
            return None

        # Try NER on first 500 chars
        doc = nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                return ent.text.strip()

        # Fallback: use first non-empty line that looks like a name
        for line in lines[:5]:
            clean = re.sub(r'[^a-zA-Z\s]', '', line).strip()
            words = clean.split()
            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                if not any(kw in clean.lower() for kw in ["resume", "cv", "curriculum"]):
                    return clean

        return lines[0][:60] if lines else None

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text."""
        text_lower = text.lower()
        found_skills = set()

        # Match known skills
        for skill in KNOWN_SKILLS:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.add(skill.title())

        # Also try to find skills in the Skills section specifically
        skills_section = self._extract_section(text, "skills")
        if skills_section:
            for skill in KNOWN_SKILLS:
                if skill.lower() in skills_section.lower():
                    found_skills.add(skill.title())

        return sorted(list(found_skills))

    def _identify_sections(self, text: str) -> Dict[str, int]:
        """Identify where each section starts in the text."""
        lines = text.split("\n")
        section_positions = {}

        for i, line in enumerate(lines):
            line_clean = line.strip().lower()
            for section, keywords in SECTION_HEADERS.items():
                if any(kw in line_clean for kw in keywords):
                    if len(line_clean) < 50:  # Header lines are short
                        if section not in section_positions:
                            section_positions[section] = i
        return section_positions

    def _extract_section(self, text: str, section: str) -> str:
        """Extract content of a specific section."""
        lines = text.split("\n")
        positions = self._identify_sections(text)

        if section not in positions:
            return ""

        start = positions[section]
        # Find next section
        sorted_positions = sorted(positions.items(), key=lambda x: x[1])
        end = len(lines)
        for name, pos in sorted_positions:
            if pos > start:
                end = pos
                break

        return "\n".join(lines[start:end])

    def extract_education(self, text: str) -> List[Dict]:
        """Extract education entries."""
        section = self._extract_section(text, "education") or text
        entries = []

        lines = [l.strip() for l in section.split("\n") if l.strip()]

        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(deg in line_lower for deg in EDUCATION_DEGREES):
                entry = {
                    "degree": line[:200],
                    "institution": "",
                    "year": "",
                    "gpa": ""
                }
                # Try to get institution from nearby lines
                if i + 1 < len(lines) and len(lines[i + 1]) > 3:
                    entry["institution"] = lines[i + 1][:200]

                # Extract year
                year_match = re.search(r'\b(19|20)\d{2}\b', line + " ".join(lines[max(0, i-1):i+3]))
                if year_match:
                    entry["year"] = year_match.group()

                # Extract GPA
                gpa_match = re.search(r'(?:gpa|cgpa|grade)[:\s]*([0-9.]+)', line_lower)
                if gpa_match:
                    entry["gpa"] = gpa_match.group(1)

                entries.append(entry)

        return entries[:5]  # Max 5 education entries

    def extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience entries."""
        section = self._extract_section(text, "experience") or ""
        entries = []

        if not section:
            return entries

        blocks = re.split(r'\n{2,}', section)
        for block in blocks[1:]:  # Skip section header
            block = block.strip()
            if not block or len(block) < 20:
                continue

            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if not lines:
                continue

            # Date range detection
            date_pattern = re.search(
                r'((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{4}|'
                r'\d{4})\s*[-–—to]+\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{4}|\d{4}|present|current)',
                block.lower()
            )

            entry = {
                "title": lines[0][:150] if lines else "",
                "company": lines[1][:150] if len(lines) > 1 else "",
                "duration": date_pattern.group(0).title() if date_pattern else "",
                "description": "\n".join(lines[2:5]) if len(lines) > 2 else ""
            }
            entries.append(entry)

        return entries[:10]

    def extract_projects(self, text: str) -> List[Dict]:
        """Extract project entries."""
        section = self._extract_section(text, "projects") or ""
        entries = []

        if not section:
            return entries

        blocks = re.split(r'\n{2,}', section)
        for block in blocks[1:]:
            block = block.strip()
            if not block or len(block) < 15:
                continue
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if lines:
                entry = {
                    "title": lines[0][:150],
                    "description": " ".join(lines[1:4])[:400] if len(lines) > 1 else "",
                    "technologies": [],
                    "url": ""
                }
                # Extract URLs
                url_match = URL_PATTERN.search(block)
                if url_match:
                    entry["url"] = url_match.group()

                # Technologies from line
                for skill in KNOWN_SKILLS:
                    if skill.lower() in block.lower():
                        entry["technologies"].append(skill.title())

                entries.append(entry)

        return entries[:10]

    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications."""
        section = self._extract_section(text, "certifications") or ""
        certs = []

        lines = [l.strip() for l in section.split("\n") if l.strip()]
        for line in lines[1:]:  # Skip header
            if len(line) > 5 and not any(h in line.lower() for h in SECTION_HEADERS.get("certifications", [])):
                certs.append(line[:200])

        return certs[:10]

    def parse(self, file_path: str) -> Dict:
        """
        Parse a resume PDF and return structured data.

        Returns:
            dict with all extracted fields
        """
        raw_text, page_count = self.extract_text_from_pdf(file_path)

        return {
            "name": self.extract_name(raw_text),
            "email": self.extract_email(raw_text),
            "phone": self.extract_phone(raw_text),
            "github": self.extract_github(raw_text),
            "linkedin": self.extract_linkedin(raw_text),
            "summary": self._extract_section(raw_text, "summary")[:600],
            "skills": self.extract_skills(raw_text),
            "education": self.extract_education(raw_text),
            "experience": self.extract_experience(raw_text),
            "projects": self.extract_projects(raw_text),
            "certifications": self.extract_certifications(raw_text),
            "raw_text": raw_text[:10000],
            "page_count": page_count,
        }


# Singleton instance
resume_parser = ResumeParser()
