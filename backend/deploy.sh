#!/bin/bash

# Skraper Web Backend Deployment Script

echo "🚀 Skraper Web Backend Deployment"
echo "================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Build Docker image
echo "📦 Building Docker image..."
docker build -t skraper-web-backend .

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    # Run the container
    echo "🐳 Running Docker container..."
    docker run -d -p 5000:5000 --name skraper-backend skraper-web-backend
    
    if [ $? -eq 0 ]; then
        echo "✅ Container started successfully!"
        echo ""
        echo "🌐 Backend API is running at: http://localhost:5000"
        echo "🔍 Health check: http://localhost:5000/health"
        echo "📋 API status: http://localhost:5000/api/scrape/status"
        echo ""
        echo "To stop the container: docker stop skraper-backend"
        echo "To remove the container: docker rm skraper-backend"
    else
        echo "❌ Failed to start container"
        exit 1
    fi
else
    echo "❌ Failed to build Docker image"
    exit 1
fi