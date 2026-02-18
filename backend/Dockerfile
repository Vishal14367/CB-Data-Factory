# Backend Dockerfile - Production Ready
FROM python:3.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=10000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY assets/ ./assets/

# Setup application
RUN mkdir -p output && \
    touch src/__init__.py

# Expose port (Render overrides this with its own PORT env var)
EXPOSE 10000

# Run application - uses $PORT env var (Render sets this to 10000 by default)
CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-10000}
