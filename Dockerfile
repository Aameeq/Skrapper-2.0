FROM python:3.11-slim

# Install Java (required for Skraper)
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Skraper CLI tool
RUN wget -O /usr/local/bin/skraper https://github.com/sokomishalov/skraper/releases/download/0.13.0/skraper \
    && chmod +x /usr/local/bin/skraper

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]