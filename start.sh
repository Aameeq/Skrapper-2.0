#!/bin/bash
# Startup script for cloud deployment

echo "Starting Skraper Web Backend..."

# Set port from environment or default
PORT=${PORT:-5000}

# Check if we're in development or production
if [ "$FLASK_ENV" = "production" ]; then
    echo "Running in production mode"
    gunicorn --bind 0.0.0.0:$PORT --workers 4 app_enhanced:app
else
    echo "Running in development mode"
    python app_enhanced.py
fi