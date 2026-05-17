FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn==21.2.0

# Copy project files
COPY ./backend /app/backend
COPY ./docker /app/docker
COPY ./research /app/research

# Create static directory
RUN mkdir -p /app/backend/server/static

# Make entrypoint script executable
RUN chmod +x /app/docker/backend/wsgi-entrypoint.sh
