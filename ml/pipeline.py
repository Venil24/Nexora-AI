"""
ml/pipeline.py
Complete ML training pipeline for career prediction.
Trains Random Forest, Decision Tree, and Logistic Regression models.
Compares accuracy and saves the best model.

Usage: python ml/pipeline.py
"""
import os
import sys
import json
import warnings
import numpy as np
import pandas as pd
import joblib
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, f1_score
)
from sklearn.pipeline import Pipeline

warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "datasets", "career_dataset.csv")
MODELS_DIR = os.path.join(BASE_DIR, "trained_models")
os.makedirs(MODELS_DIR, exist_ok=True)

# ── All skills used as features ────────────────────────────────────────────────
ALL_SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala", "go", "rust",
    "react", "angular", "vue", "nextjs", "html", "css", "tailwind",
    "node", "flask", "django", "fastapi", "spring", "express",
    "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    "docker", "kubernetes", "terraform", "ansible", "jenkins", "github_actions",
    "aws", "gcp", "azure", "linux",
    "machine_learning", "deep_learning", "tensorflow", "pytorch", "sklearn",
    "pandas", "numpy", "matplotlib", "seaborn", "tableau", "power_bi",
    "nlp", "computer_vision", "generative_ai", "llm",
    "git", "agile", "scrum", "jira", "figma", "photoshop",
    "excel", "hadoop", "spark", "kafka", "airflow",
    "cybersecurity", "networking", "penetration_testing",
    "ios", "android", "flutter", "react_native",
    "devops", "sre", "ci_cd", "monitoring",
]

CAREERS = [
    "Software Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Data Analyst",
    "Cybersecurity Engineer",
    "Mobile Developer",
    "Cloud Architect",
    "Database Administrator",
]

# Map career → typical skills (used for synthetic dataset generation)
CAREER_SKILL_MAP = {
    "Software Engineer": ["python", "java", "c++", "git", "sql", "docker", "agile", "linux", "mongodb", "postgresql"],
    "Data Scientist": ["python", "machine_learning", "deep_learning", "sklearn", "pandas", "numpy", "r", "tensorflow", "tableau", "sql", "spark"],
    "Machine Learning Engineer": ["python", "machine_learning", "deep_learning", "tensorflow", "pytorch", "sklearn", "pandas", "numpy", "docker", "kubernetes", "aws", "mlflow"],
    "Frontend Developer": ["javascript", "typescript", "react", "vue", "angular", "html", "css", "tailwind", "nextjs", "figma", "git"],
    "Backend Developer": ["python", "java", "node", "flask", "django", "fastapi", "spring", "sql", "postgresql", "mongodb", "redis", "docker", "git"],
    "Full Stack Developer": ["javascript", "typescript", "react", "node", "python", "sql", "mongodb", "html", "css", "docker", "git", "aws"],
    "DevOps Engineer": ["docker", "kubernetes", "terraform", "ansible", "jenkins", "github_actions", "aws", "gcp", "azure", "linux", "ci_cd", "monitoring", "python", "devops"],
    "Data Analyst": ["sql", "excel", "python", "pandas", "tableau", "power_bi", "r", "matplotlib", "seaborn"],
    "Cybersecurity Engineer": ["cybersecurity", "networking", "penetration_testing", "linux", "python", "c++", "sql"],
    "Mobile Developer": ["ios", "android", "flutter", "react_native", "javascript", "swift", "kotlin", "git"],
    "Cloud Architect": ["aws", "gcp", "azure", "docker", "kubernetes", "terraform", "networking", "linux", "python", "devops", "ci_cd"],
    "Database Administrator": ["sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "python", "linux", "backup"],
}


def generate_dataset(n_samples: int = 5000) -> pd.DataFrame:
    """Generate a synthetic career prediction dataset."""
    np.random.seed(42)
    records = []

    samples_per_career = n_samples // len(CAREERS)

    for career in CAREERS:
        core_skills = CAREER_SKILL_MAP[career]
        for _ in range(samples_per_career):
            # Each sample: random subset of career skills + some noise skills
            n_core = np.random.randint(max(2, len(core_skills) - 3), len(core_skills) + 1)
            selected_core = np.random.choice(core_skills, size=min(n_core, len(core_skills)), replace=False).tolist()

            # Add 0-4 random noise skills
            noise_pool = [s for s in ALL_SKILLS if s not in core_skills]
            n_noise = np.random.randint(0, 5)
            noise_skills = np.random.choice(noise_pool, size=n_noise, replace=False).tolist()

            skills = selected_core + noise_skills

            # Feature vector
            row = {skill: 1 if skill in skills else 0 for skill in ALL_SKILLS}
            row["experience_years"] = np.random.randint(0, 15)
            row["education_level"] = np.random.choice([0, 1, 2, 3], p=[0.05, 0.35, 0.45, 0.15])
            row["num_projects"] = np.random.randint(0, 20)
            row["num_certifications"] = np.random.randint(0, 8)
            row["career"] = career
            records.append(row)

    df = pd.DataFrame(records)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def load_or_generate_dataset() -> pd.DataFrame:
    """Load dataset from CSV or generate synthetic one."""
    if os.path.exists(DATASET_PATH):
        print(f"📂 Loading dataset from: {DATASET_PATH}")
        df = pd.read_csv(DATASET_PATH)
    else:
        print("🔧 Generating synthetic dataset...")
        df = generate_dataset(5000)
        os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
        df.to_csv(DATASET_PATH, index=False)
        print(f"💾 Dataset saved to: {DATASET_PATH}")
    return df


def prepare_features(df: pd.DataFrame):
    """Prepare feature matrix X and encoded label vector y."""
    feature_cols = ALL_SKILLS + ["experience_years", "education_level", "num_projects", "num_certifications"]
    # Only keep columns that exist in df
    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols].fillna(0)
    le = LabelEncoder()
    y = le.fit_transform(df["career"])

    return X, y, le, feature_cols


def train_models(X_train, y_train, X_test, y_test, label_encoder):
    """Train all three models, evaluate, and return results."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=4,
            class_weight="balanced",
            random_state=42
        ),
        "Logistic Regression": LogisticRegression(
            C=1.0,
            max_iter=1000,
            class_weight="balanced",
            random_state=42,
            multi_class="multinomial",
            solver="lbfgs"
        )
    }

    results = {}
    for name, model in models.items():
        print(f"\n  🔄 Training {name}...")
        use_scaled = name == "Logistic Regression"
        Xtr = X_train_scaled if use_scaled else X_train
        Xte = X_test_scaled if use_scaled else X_test

        model.fit(Xtr, y_train)
        y_pred = model.predict(Xte)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        cv_scores = cross_val_score(model, Xtr, y_train, cv=5, scoring="accuracy", n_jobs=-1)

        results[name] = {
            "model": model,
            "scaler": scaler if use_scaled else None,
            "accuracy": round(acc * 100, 2),
            "f1_score": round(f1, 4),
            "cv_mean": round(cv_scores.mean() * 100, 2),
            "cv_std": round(cv_scores.std() * 100, 2),
            "report": classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True)
        }
        print(f"  ✅ {name}: Accuracy={acc*100:.2f}%, CV={cv_scores.mean()*100:.2f}%±{cv_scores.std()*100:.2f}%")

    return results


def save_models(results, feature_cols, label_encoder):
    """Save all trained models and the best model with metadata."""
    best_name = max(results, key=lambda k: results[k]["accuracy"])
    best = results[best_name]

    # Save each model individually
    for name, data in results.items():
        safe_name = name.lower().replace(" ", "_")
        model_path = os.path.join(MODELS_DIR, f"{safe_name}.joblib")
        payload = {
            "model": data["model"],
            "scaler": data.get("scaler"),
            "feature_cols": feature_cols,
            "label_encoder": label_encoder,
            "accuracy": data["accuracy"],
            "f1_score": data["f1_score"],
        }
        joblib.dump(payload, model_path)
        print(f"  💾 Saved: {model_path}")

    # Save best model as `best_model.joblib`
    best_path = os.path.join(MODELS_DIR, "best_model.joblib")
    best_payload = {
        "model": best["model"],
        "scaler": best.get("scaler"),
        "feature_cols": feature_cols,
        "label_encoder": label_encoder,
        "model_name": best_name,
        "accuracy": best["accuracy"],
        "f1_score": best["f1_score"],
        "trained_at": datetime.utcnow().isoformat(),
        "careers": list(label_encoder.classes_),
        "all_skills": ALL_SKILLS,
    }
    joblib.dump(best_payload, best_path)
    print(f"  🏆 Best model saved: {best_path} ({best_name}, {best['accuracy']}%)")

    # Save evaluation report as JSON
    report_data = {
        "trained_at": datetime.utcnow().isoformat(),
        "best_model": best_name,
        "models": {
            name: {k: v for k, v in data.items() if k not in ("model", "scaler")}
            for name, data in results.items()
        }
    }
    report_path = os.path.join(MODELS_DIR, "evaluation_report.json")
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=2)
    print(f"  Evaluation report saved: {report_path}")


def main():
    print("=" * 60)
    print("   Nexora-AI Career Prediction ML Pipeline")
    print("=" * 60)

    print("\nStep 1: Loading dataset...")
    df = load_or_generate_dataset()
    print(f"  Dataset shape: {df.shape}")
    print(f"  Career distribution:\n{df['career'].value_counts().to_string()}")

    print("\nStep 2: Preparing features...")
    X, y, label_encoder, feature_cols = prepare_features(df)
    print(f"  Features: {len(feature_cols)}")
    print(f"  Classes: {len(label_encoder.classes_)}")

    print("\nStep 3: Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

    print("\nStep 4: Training models...")
    results = train_models(X_train, y_train, X_test, y_test, label_encoder)

    print("\nStep 5: Model Comparison:")
    print(f"  {'Model':<25} {'Accuracy':>10} {'F1 Score':>10} {'CV Mean':>10}")
    print("  " + "-" * 57)
    for name, data in results.items():
        print(f"  {name:<25} {data['accuracy']:>9.2f}% {data['f1_score']:>10.4f} {data['cv_mean']:>9.2f}%")

    print("\nStep 6: Saving models...")
    save_models(results, feature_cols, label_encoder)

    best = max(results, key=lambda k: results[k]["accuracy"])
    print(f"\nTraining complete! Best model: {best} ({results[best]['accuracy']}%)")
    print("=" * 60)


if __name__ == "__main__":
    main()
