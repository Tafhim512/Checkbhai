# Use official Python image with pip
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend code
COPY . /app

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Start the app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
