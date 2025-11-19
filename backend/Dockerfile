# Use a base image that includes OpenJDK 17 (Eclipse Temurin - Official Replacement)
FROM eclipse-temurin:17-jdk

# Install Python, pip, venv, wget, git, and yt-dlp (required for the backend)
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv wget git yt-dlp && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Create a virtual environment and install dependencies within it
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Make sure the virtual environment's Python and pip are used
# CRITICAL FIX: Prepend venv bin to existing PATH
ENV PATH="/opt/venv/bin:"

# Copy application code
COPY app.py .

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
