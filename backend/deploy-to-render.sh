#!/bin/bash

# Render Deployment Script for Skrapper Backend

set -e

# Render API configuration
RENDER_API_KEY="rnd_ESzsaUZi2N0mD4h50NmFhp5JOXqE"
RENDER_API_URL="https://api.render.com/v1"
SERVICE_NAME="skraper-backend"

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"

echo "🚀 Deploying Skrapper Backend to Render..."
echo "======================================="

# Check if service already exists
echo "1. Checking for existing service..."
EXISTING_SERVICE=$(curl -s -X GET "$RENDER_API_URL/services" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" | grep -o '"name":"'$SERVICE_NAME'"' || echo "")

if [ -n "$EXISTING_SERVICE" ]; then
    echo "   Service exists, updating..."
    # Update existing service
    RESPONSE=$(curl -s -X PATCH "$RENDER_API_URL/services/$SERVICE_NAME" \
      -H "Authorization: Bearer $RENDER_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "type": "web",
        "env": "docker",
        "dockerfilePath": "./Dockerfile",
        "autoDeploy": true
      }')
else
    echo "   Creating new service..."
    # Create new service
    RESPONSE=$(curl -s -X POST "$RENDER_API_URL/services" \
      -H "Authorization: Bearer $RENDER_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "'$SERVICE_NAME'",
        "type": "web",
        "env": "docker",
        "dockerfilePath": "./Dockerfile",
        "autoDeploy": true,
        "serviceDetails": {
          "dockerCommand": "",
          "dockerContext": ".",
          "registryCredentialId": ""
        },
        "envVars": [
          {
            "key": "PORT",
            "value": "5000"
          },
          {
            "key": "FLASK_ENV", 
            "value": "production"
          }
        ]
      }')
fi

echo "2. Deployment initiated..."
echo "   Response: $RESPONSE"

# Extract service details
SERVICE_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
if [ -n "$SERVICE_ID" ]; then
    echo "   Service ID: $SERVICE_ID"
    
    # Get service URL
    SERVICE_URL=$(curl -s -X GET "$RENDER_API_URL/services/$SERVICE_ID" \
      -H "Authorization: Bearer $RENDER_API_KEY" \
      -H "Content-Type: application/json" | grep -o '"serviceDetails":{"url":"[^"]*"' | cut -d'"' -f6)
    
    if [ -n "$SERVICE_URL" ]; then
        echo "   Service URL: $SERVICE_URL"
        echo ""
        echo "✅ Backend deployment initiated!"
        echo "   Backend URL: $SERVICE_URL"
        echo "   Note: It may take 2-3 minutes for the service to be fully deployed."
        
        # Save the URL for frontend configuration
        echo "$SERVICE_URL" > "../backend_url.txt"
    else
        echo "⚠️  Service created but URL not yet available. Check Render dashboard."
    fi
else
    echo "❌ Failed to create/deploy service"
    echo "   Error response: $RESPONSE"
    exit 1
fi

echo ""
echo "🔄 Next steps:"
echo "   1. Check deployment status in Render dashboard"
echo "   2. Wait for service to be fully deployed"
echo "   3. Update frontend API URL with the backend URL"
echo "   4. Deploy frontend to Netlify"