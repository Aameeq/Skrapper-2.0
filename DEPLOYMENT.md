# Skraper Web - Complete Deployment Guide

## Overview

This guide will help you deploy a fully functional Skraper Web application that actually integrates with the Skraper library, replacing the mock data with real social media scraping capabilities.

## Architecture

```
Frontend (HTML/JS) → Backend API (Flask/Python) → Skraper CLI → Social Media Platforms
```

## Prerequisites

- **Docker** (recommended) or Python 3.8+
- **Java Runtime Environment (JRE) 11+** (required for Skraper)
- **Git** for cloning the repository
- **Internet connection** for downloading dependencies

## Quick Deployment (Docker - Recommended)

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Deploy with Docker
```bash
./deploy.sh
```

This will:
- Build a Docker image with all dependencies
- Install Skraper CLI tool
- Start the backend API on port 5000

### Step 3: Test the Backend
```bash
curl http://localhost:5000/health
```

You should see a JSON response indicating the service status.

### Step 4: Update Frontend
Replace `index.html` with `index-api.html` and `main.js` with `main-api.js`:
```bash
cp index-api.html index.html
cp main-api.js main.js
```

### Step 5: Access the Application
Open your browser and navigate to your deployed frontend URL.

## Manual Deployment

### Backend Setup

#### Step 1: Install Skraper CLI
```bash
# Download Skraper CLI
wget -O /usr/local/bin/skraper https://github.com/sokomishalov/skraper/releases/download/0.13.0/skraper

# Make it executable
chmod +x /usr/local/bin/skraper

# Test installation
skraper --help
```

#### Step 2: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Step 3: Run the Backend
```bash
python app.py
```

The backend will start on `http://localhost:5000`

#### Step 4: Test the API
```bash
curl http://localhost:5000/api/platforms
```

### Frontend Setup

#### Step 1: Update API URL
Edit `main-api.js` and update the API base URL if needed:
```javascript
this.apiBaseUrl = 'http://localhost:5000/api'; // Change if different port/host
```

#### Step 2: Deploy Frontend
Use any static hosting service:
- Netlify
- Vercel
- GitHub Pages
- Apache/Nginx

## Cloud Deployment Options

### Option 1: Heroku (Free Tier)

#### Backend Deployment
```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-skraper-api

# Deploy
git add .
git commit -m "Deploy backend"
git push heroku main
```

#### Frontend Deployment
Use Netlify or Vercel for the frontend, updating the API URL to point to your Heroku backend.

### Option 2: AWS/GCP/Azure

#### Using Docker
```bash
# Build image
docker build -t skraper-backend .

# Deploy to cloud container service
# AWS ECS, Google Cloud Run, Azure Container Instances
```

### Option 3: VPS (DigitalOcean, Linode)

#### Install on Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Java
sudo apt install openjdk-17-jre-headless -y

# Install Python and pip
sudo apt install python3-pip -y

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone and deploy
git clone <your-repo-url>
cd skraper-web/backend
./deploy.sh
```

## API Endpoints

### Health Check
```
GET /health
```
Returns service status and Skraper availability.

### Get Supported Platforms
```
GET /api/platforms
```
Returns list of supported social media platforms.

### Scrape Data
```
POST /api/scrape
Content-Type: application/json

{
    "url": "https://instagram.com/username",
    "content_type": "posts",
    "limit": 50,
    "output_format": "json"
}
```

### Check Scraping Status
```
GET /api/scrape/status
```
Returns backend and Skraper status.

## Configuration

### Environment Variables

- `PORT`: Backend port (default: 5000)
- `FLASK_ENV`: Environment (development/production)

### Frontend Configuration

Update the API base URL in `main-api.js`:
```javascript
this.apiBaseUrl = 'https://your-backend-url.com/api';
```

## Troubleshooting

### Common Issues

#### 1. Skraper Not Found
```bash
# Check if skraper is in PATH
which skraper

# If not found, add to PATH
export PATH=$PATH:/usr/local/bin
```

#### 2. Java Not Found
```bash
# Install Java
sudo apt install openjdk-17-jre-headless  # Ubuntu/Debian
brew install openjdk@17                   # macOS
```

#### 3. CORS Issues
Ensure the backend has CORS enabled for your frontend domain.

#### 4. Rate Limiting
The backend includes basic rate limiting. For production, consider:
- Implementing API keys
- Adding request throttling
- Using a reverse proxy

#### 5. Memory Issues
Skraper can be memory-intensive. For large deployments:
- Use a server with at least 2GB RAM
- Monitor memory usage
- Implement request queuing

## Security Considerations

1. **Input Validation**: The backend validates all inputs
2. **Rate Limiting**: Basic protection against abuse
3. **Error Handling**: Doesn't expose sensitive information
4. **CORS**: Configured for cross-origin requests

For production:
- Add authentication
- Implement HTTPS
- Use environment variables for secrets
- Add logging and monitoring

## Performance Optimization

1. **Caching**: Implement result caching
2. **Async Processing**: Use background tasks for long scrapes
3. **Load Balancing**: Distribute requests across multiple instances
4. **CDN**: Use CDN for static assets

## Monitoring

### Health Checks
```bash
# Backend health
curl http://localhost:5000/health

# API status
curl http://localhost:5000/api/scrape/status
```

### Logs
```bash
# View Docker logs
docker logs skraper-backend

# View application logs
tail -f /var/log/skraper-api.log
```

## Scaling

### Horizontal Scaling
- Deploy multiple backend instances
- Use a load balancer
- Share cache/storage

### Vertical Scaling
- Increase server resources
- Optimize Skraper configuration
- Use faster storage

## Cost Estimates

### Development (Free)
- Local development: $0
- Heroku free tier: $0
- Netlify/Vercel free: $0

### Production (Basic)
- VPS (2GB RAM): $10-20/month
- Domain: $10-15/year
- CDN: $5-20/month

### Production (Enterprise)
- Load balancer: $20-50/month
- Multiple servers: $50-200/month
- Monitoring: $20-100/month
- Backup/storage: $10-50/month

## Support

For issues:
1. Check the troubleshooting section
2. Review application logs
3. Test API endpoints directly
4. Verify Skraper CLI installation
5. Check network connectivity

## Next Steps

1. **Deploy the backend** using your preferred method
2. **Update the frontend** to use the real API
3. **Test with different platforms** and URLs
4. **Monitor performance** and usage
5. **Scale as needed** based on demand

## Example Usage

Once deployed, you can test with these URLs:
- Instagram: `https://instagram.com/natgeo`
- TikTok: `https://tiktok.com/@charlidamelio`
- Twitter: `https://twitter.com/elonmusk`
- YouTube: `https://youtube.com/c/MrBeast`

The application will extract real data from these platforms and provide structured JSON output for analysis and export.