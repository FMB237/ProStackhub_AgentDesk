# syntax=docker/dockerfile:1
# Multi-stage build for AgentDesk
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 bruce

# Copy installed packages from builder
COPY --from=builder /root/.local /home/bruce/.local
ENV PATH=/home/bruce/.local/bin:$PATH

# Copy application code
COPY --chown=bruce:bruce . .

# Ensure static folder exists
RUN mkdir -p static

# Switch to non-root
USER bruce

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
