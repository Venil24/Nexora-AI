# backend/Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy models and NLTK databases
RUN python -m spacy download en_core_web_sm \
    && python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Copy backend files and ML engine
COPY . .

EXPOSE 5000

# Gunicorn start script
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
