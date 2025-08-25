FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy both api and tests directories
COPY --chown=appuser:appuser api/ ./api/
COPY --chown=appuser:appuser tests/ ./tests/

# Create pytest cache directory with proper permissions
RUN mkdir -p /app/.pytest_cache && chown -R appuser:appuser /app/.pytest_cache

# Ensure appuser owns the entire /app directory
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
