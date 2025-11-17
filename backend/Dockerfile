# Use a base image that includes OpenJDK 17 (Eclipse Temurin - Official Replacement)
FROM eclipse-temurin:17-jdk

# Install Python, pip, venv, wget, and git (for cloning Skraper)
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv wget git && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Add venv to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY app.py .

# Clone and build Skraper from source
WORKDIR /tmp
RUN git clone https://github.com/sokomishalov/skraper.git && \
    cd skraper && \
    ./gradlew build --no-daemon && \
    cp build/libs/skraper /usr/local/bin/ && \
    chmod +x /usr/local/bin/skraper && \
    rm -rf /tmp/skraper

WORKDIR /app

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
