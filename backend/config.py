"""
backend/config.py
Flask application configuration for all environments.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration shared by all environments."""
    SECRET_KEY = os.getenv("SECRET_KEY", "nexora-dev-secret-key-change-in-prod")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "nexora-jwt-secret-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000)))
    JWT_HEADER_TYPE = "Bearer"

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/nexora_ai")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "nexora_ai")

    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "uploads")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))  # 10 MB
    ALLOWED_EXTENSIONS = {"pdf"}

    ML_MODELS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "trained_models")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_API_BASE = "https://api.github.com"

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "Nexora AI <noreply@nexora.ai>")

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

    BCRYPT_ROUNDS = 12
    PAGE_SIZE = 10


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    BCRYPT_ROUNDS = 14


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    MONGO_DB_NAME = "nexora_ai_test"


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return CONFIG_MAP.get(env, DevelopmentConfig)
