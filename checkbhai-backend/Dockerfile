# Multi-stage Dockerfile for CheckBhai Backend

FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app/ ./app/

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Create models directory
RUN mkdir -p app/models

# Train AI model on startup (will be saved to app/models/)
# This happens during build so the model is baked into the image

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app/start.py"]
