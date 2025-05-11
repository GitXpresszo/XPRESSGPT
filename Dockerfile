# Use minimal Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Create volume for persistent database
VOLUME ["/data"]
ENV DB_PATH=/data/users.db

# ✅ OPTIONAL: .env fallback - only if it exists locally (for local dev)
# This will not fail if .env is missing in HF Space
# Don't COPY it — read env vars directly inside app.py instead

# Streamlit settings for healthcheck
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the app
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
