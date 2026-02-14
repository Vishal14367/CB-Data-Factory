# Backend Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system dependencies
# Added more comprehensive libs for common Python package build failures
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    libmagic1 \
    libffi-dev \
    libssl-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Ensure src is treated as a package (though Python 3.3+ doesn't strictly need it)
RUN touch src/__init__.py

# Create output directory for sessions and reports
RUN mkdir -p output

# Expose the port (Render will override this, but good for local)
EXPOSE 8000

# Command to run the application using the PORT env var
# Using shell form to allow environment variable expansion
CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT}
