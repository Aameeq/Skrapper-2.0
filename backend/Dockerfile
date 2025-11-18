# Use a base image that includes OpenJDK 17 (Eclipse Temurin - Official Replacement)
FROM eclipse-temurin:17-jdk

# Install Python, pip, venv, and wget (required for the backend and downloading skraper)
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv wget && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Create a virtual environment and install dependencies within it
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Make sure the virtual environment's Python and pip are used
ENV PATH="/opt/venv/bin:"

# Copy application code
COPY app.py .

# Install Skraper CLI tool (Download pre-built binary)
RUN wget -O /usr/local/bin/skraper https://github.com/sokomishalov/skraper/releases/download/0.13.0/skraper   \
    && chmod +x /usr/local/bin/skraper

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
