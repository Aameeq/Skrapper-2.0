# Use a base image that includes OpenJDK 17 (Eclipse Temurin - Official Replacement)
FROM eclipse-temurin:17-jdk

# Install Python and pip, then install Python dependencies in a single RUN command
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application code
COPY app.py .

# Install Skraper CLI tool
RUN wget -O /usr/local/bin/skraper https://github.com/sokomishalov/skraper/releases/download/0.13.0/skraper   \
    && chmod +x /usr/local/bin/skraper

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
