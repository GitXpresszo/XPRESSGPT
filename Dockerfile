# Use minimal Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY src/ ./src/

# Create persistent volume for database
RUN mkdir -p /data && chmod 777 /data
ENV DB_PATH=/data/users.db
VOLUME ["/data"]

# Healthcheck on HF default port 7860
EXPOSE 7860
HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health || exit 1

# Run Streamlit on HF-compatible port 7860
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]
