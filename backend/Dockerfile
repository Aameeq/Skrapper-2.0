# Use a base image that includes OpenJDK 17 (Eclipse Temurin - Official Replacement)
FROM eclipse-temurin:17-jdk

# Install Python, pip, venv, wget, git, yt-dlp, and bash (required for the backend and potential runtime)
# bash is included to mitigate potential /usr/bin/env: 'bash': No such file or directory errors
# Although /bin/sh should be sufficient for the exec form CMD, this covers potential edge cases.
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv wget git yt-dlp bash && \
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

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application using explicit /bin/sh -c command.
# This ensures the command runs under the standard POSIX shell (/bin/sh), not bash.
# The 'exec form' CMD ["gunicorn", ...] *should* do this, but this format guarantees it.
CMD ["/bin/sh", "-c", "exec gunicorn --bind 0.0.0.0:5000 --workers 4 app:app"]
