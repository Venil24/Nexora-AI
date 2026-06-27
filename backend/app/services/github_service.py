"""
backend/app/services/github_service.py
GitHub API integration for profile analysis.
"""
import os
import requests
from typing import Dict, List, Any
from collections import Counter
from flask import current_app


class GitHubService:
    """Fetches and analyzes GitHub profile data via GitHub REST API."""

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", "").strip()
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        # Ignore placeholder values
        if self.token and not self.token.startswith("ghp_your_github"):
            self.headers["Authorization"] = f"Bearer {self.token}"

    def _get(self, endpoint: str, params: dict = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        resp = requests.get(url, headers=self.headers, params=params or {}, timeout=10)
        if resp.status_code == 401:
            raise PermissionError("GitHub token in .env is invalid or unauthorized")
        if resp.status_code == 404:
            raise ValueError(f"GitHub user not found")
        if resp.status_code == 403:
            raise PermissionError("GitHub API rate limit exceeded or token invalid")
        resp.raise_for_status()
        return resp.json()

    def get_user_profile(self, username: str) -> Dict:
        return self._get(f"/users/{username}")

    def get_user_repos(self, username: str) -> List[Dict]:
        all_repos = []
        page = 1
        while page <= 5:  # Max 5 pages (500 repos)
            repos = self._get(f"/users/{username}/repos", {
                "per_page": 100,
                "page": page,
                "sort": "updated",
                "direction": "desc"
            })
            if not repos:
                break
            all_repos.extend(repos)
            if len(repos) < 100:
                break
            page += 1
        return all_repos

    def calculate_language_distribution(self, repos: List[Dict]) -> Dict[str, int]:
        lang_counter = Counter()
        for repo in repos:
            if repo.get("language"):
                lang_counter[repo["language"]] += 1
        return dict(lang_counter.most_common(10))

    def calculate_scores(self, profile: Dict, repos: List[Dict]) -> tuple:
        """Calculate skill and activity scores based on profile data."""
        followers = profile.get("followers", 0)
        public_repos = profile.get("public_repos", 0)
        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        total_forks = sum(r.get("forks_count", 0) for r in repos)

        # Skill score (based on repos, stars, languages)
        languages = set(r.get("language") for r in repos if r.get("language"))
        skill_score = min(100, (
            len(languages) * 5 +
            min(public_repos * 2, 40) +
            min(total_stars * 2, 30) +
            min(followers * 0.5, 20)
        ))

        # Activity score (based on recent activity)
        recent_repos = [r for r in repos if r.get("pushed_at", "")[:4] == "2024" or r.get("pushed_at", "")[:4] == "2025"]
        activity_score = min(100, (
            len(recent_repos) * 10 +
            min(public_repos, 30) +
            min(followers * 2, 40)
        ))

        return round(skill_score, 1), round(activity_score, 1)

    def analyze(self, username: str) -> Dict:
        """Analyze a GitHub profile and return structured data."""
        profile = self.get_user_profile(username)
        repos = self.get_user_repos(username)

        languages = self.calculate_language_distribution(repos)
        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        total_forks = sum(r.get("forks_count", 0) for r in repos)

        # Top repos by stars
        top_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:6]
        top_repos_data = [
            {
                "name": r.get("name"),
                "description": r.get("description", ""),
                "language": r.get("language"),
                "stars": r.get("stargazers_count", 0),
                "forks": r.get("forks_count", 0),
                "url": r.get("html_url"),
                "topics": r.get("topics", []),
            }
            for r in top_repos
        ]

        skill_score, activity_score = self.calculate_scores(profile, repos)

        return {
            "profile": {
                "name": profile.get("name"),
                "bio": profile.get("bio"),
                "avatar_url": profile.get("avatar_url"),
                "html_url": profile.get("html_url"),
                "company": profile.get("company"),
                "location": profile.get("location"),
                "blog": profile.get("blog"),
                "created_at": profile.get("created_at"),
            },
            "total_repos": profile.get("public_repos", 0),
            "followers": profile.get("followers", 0),
            "following": profile.get("following", 0),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "languages": languages,
            "top_repos": top_repos_data,
            "skill_score": skill_score,
            "activity_score": activity_score,
            "contributions": 0,  # Would require GraphQL API
        }
