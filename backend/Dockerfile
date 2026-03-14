FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONHASHSEED=0

WORKDIR /app

# Install curl (and clean apt cache to keep image slim)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

WORKDIR /app
# Uvicorn configuration for large file processing:
# - workers=1 (to avoid threading issues with large files)
# - timeout=300s (5 min for chunk processing)
# - graceful-timeout=30s (allow cleanup)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--timeout-keep-alive", "120", "--timeout-graceful-shutdown", "30"]
