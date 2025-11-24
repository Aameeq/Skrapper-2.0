# Use a standard Python slim base image
FROM python:3.10-slim

# Install yt-dlp, bash, wget, git, and ensure python3-pip/python3-venv are available
# We no longer need Java as we are using yt-dlp
RUN apt-get update && \
    apt-get install -y wget git yt-dlp bash python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Create a virtual environment and install dependencies within it
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Make sure the virtual environment's Python and pip are used
# CRITICAL FIX: Prepend venv bin to existing PATH, don't replace it
ENV PATH="/opt/venv/bin:"

# Copy application code
COPY app.py .
COPY app_enhanced.py .

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application using exec form (should default to /bin/sh)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app_enhanced:app"]
