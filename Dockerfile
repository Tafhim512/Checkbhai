# Multi-stage Dockerfile for CheckBhai Backend (Root Context)
# This allows Railway to build from the project root without changing settings

FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
# Copy from checkbhai-backend folder since we are in root context
COPY checkbhai-backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code from checkbhai-backend folder
COPY checkbhai-backend/app/ ./app/

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Create models directory
RUN mkdir -p app/models

# Expose port (document only)
EXPOSE 8000

# Run application using shell to expand PORT variable
# This ensures we listen on the port Railway assigns (fixes 503 Service Unavailable)
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
