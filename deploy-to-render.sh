#!/bin/bash
# Quick deployment script for Render.com

echo "🚀 Skraper Web Deployment to Render.com"
echo "======================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
fi

# Create proper directory structure
mkdir -p backend frontend

# Move files to proper locations
cp app_enhanced.py backend/app.py 2>/dev/null || echo "Backend app not found, using existing"
cp requirements.txt backend/ 2>/dev/null || echo "Requirements file not found"
cp main-functional.js frontend/main.js 2>/dev/null || echo "Main JS file not found"
cp index-api.html frontend/index.html 2>/dev/null || echo "Index HTML not found"

# Create render.yaml for easy deployment
cat > render.yaml << 'EOF'
services:
  - type: web
    name: skraper-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: PORT
        value: 10000
      - key: FLASK_ENV
        value: production
EOF

# Create deployment instructions
cat > DEPLOYMENT_INSTRUCTIONS.txt << 'EOF'
🚀 SKRAPER WEB DEPLOYMENT INSTRUCTIONS
=====================================

STEP 1: Deploy Backend to Render.com
------------------------------------
1. Go to https://render.com and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub account
4. Select this repository
5. Configure:
   - Name: skraper-backend
   - Environment: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: python app.py
   - Instance Type: Free
6. Click "Create Web Service"

STEP 2: Get Backend URL
-----------------------
After deployment, copy your backend URL:
https://skraper-backend-xxxxx.onrender.com

STEP 3: Update Frontend
-----------------------
1. Edit frontend/main.js
2. Replace API URL with your backend URL:
   this.apiBaseUrl = 'https://skraper-backend-xxxxx.onrender.com/api';

STEP 4: Deploy Frontend
-----------------------
Option A: Netlify
1. Go to https://netlify.com
2. Connect your GitHub repository
3. Deploy the frontend folder

Option B: Vercel
1. Go to https://vercel.com
2. Connect your GitHub repository
3. Deploy the frontend folder

STEP 5: Test
------------
1. Open your frontend URL
2. Try scraping: https://facebook.com/nike
3. Check if results appear

🎯 SUCCESS INDICATORS:
- Backend shows "healthy" status
- Frontend shows "API Connected"
- Scraping returns JSON data
- No "Failed to fetch" errors

📞 TROUBLESHOOTING:
- Backend not responding? Check Render dashboard logs
- CORS errors? Backend is configured for CORS
- Scraping failed? Check URL format and platform support
- Still issues? Check DEPLOYMENT_GUIDE.md for detailed help

🎉 When everything works, you'll have:
- Functional backend API
- Working frontend interface
- Real social media scraping
- Enhanced JSON data for AI agents
EOF

# Create a simple test script
cat > test-backend.sh << 'EOF'
#!/bin/bash
echo "🧪 Testing Backend Functionality"
echo "==============================="

# Test health endpoint
echo "1. Testing health endpoint..."
curl -s http://localhost:5000/health | jq . 2>/dev/null || curl -s http://localhost:5000/health

echo ""
echo "2. Testing platform endpoint..."
curl -s http://localhost:5000/api/platforms | jq . 2>/dev/null || curl -s http://localhost:5000/api/platforms

echo ""
echo "3. Testing scraping with mock data..."
curl -s -X POST http://localhost:5000/api/scrape/enhanced \
  -H "Content-Type: application/json" \
  -d '{"url": "https://facebook.com/nike", "limit": 5}' | jq . 2>/dev/null || echo "Backend not running locally"

echo ""
echo "🎯 If backend tests pass, you're ready for cloud deployment!"
echo "📋 Follow the instructions in DEPLOYMENT_INSTRUCTIONS.txt"
EOF

chmod +x test-backend.sh

# Add all files to git
echo "📁 Adding files to Git..."
git add .
git add backend/ frontend/ 2>/dev/null || true

# Create initial commit if needed
if git status --porcelain | grep -q .; then
    echo "💾 Creating initial commit..."
    git commit -m "Initial Skraper Web deployment"
else
    echo "✅ Git repository ready"
fi

echo ""
echo "🎉 DEPLOYMENT PREPARATION COMPLETE!"
echo "==================================="
echo ""
echo "📋 Next Steps:"
echo "1. Push this repository to GitHub"
echo "2. Follow instructions in DEPLOYMENT_INSTRUCTIONS.txt"
echo "3. Deploy backend to Render.com"
echo "4. Update frontend with backend URL"
echo "5. Deploy frontend to Netlify/Vercel"
echo ""
echo "📁 Files created:"
echo "- render.yaml (Render deployment config)"
echo "- DEPLOYMENT_INSTRUCTIONS.txt (Step-by-step guide)"
echo "- test-backend.sh (Backend testing script)"
echo ""
echo "🚀 Ready to deploy! Follow the instructions above."
echo "❓ Need help? Check COMPLETE_DEPLOYMENT_GUIDE.md"