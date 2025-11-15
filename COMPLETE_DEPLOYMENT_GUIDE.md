# Complete Deployment Guide - Make Skraper Web Functional

## 🚨 **Current Issue**

Your backend is not properly connected, causing "Failed to fetch" errors. This guide will help you deploy a **fully functional** version.

## 🎯 **Solution Overview**

We need to:
1. ✅ **Deploy backend** to a cloud service (Render, Heroku, etc.)
2. ✅ **Update frontend** to point to the cloud backend
3. ✅ **Test with Facebook** and other platforms
4. ✅ **Verify everything works**

## 🚀 **Quick Deployment Options**

### **Option 1: Render.com (Recommended - Free)**

#### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up for free account
3. Verify your email

#### Step 2: Deploy Backend
1. Create a GitHub repository with your backend files
2. In Render dashboard, click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `skraper-backend`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app_enhanced.py`
   - **Instance Type**: Free
5. Click "Create Web Service"

#### Step 3: Get Backend URL
- After deployment, you'll get a URL like: `https://skraper-api.onrender.com`
- Copy this URL

#### Step 4: Update Frontend
Edit `main-functional.js` and update the API URL:
```javascript
this.apiBaseUrl = 'https://skraper-api.onrender.com/api';
```

### **Option 2: Heroku (Free)**

#### Step 1: Create Heroku Account
1. Go to [heroku.com](https://heroku.com)
2. Sign up for free account

#### Step 2: Deploy Backend
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-skraper-api

# Deploy
git add .
git commit -m "Deploy backend"
git push heroku main
```

#### Step 3: Update Frontend
```javascript
this.apiBaseUrl = 'https://your-skraper-api.herokuapp.com/api';
```

### **Option 3: Netlify Functions (Serverless)**

#### Step 1: Create Netlify Account
1. Go to [netlify.com](https://netlify.com)
2. Sign up for free account

#### Step 2: Create Serverless Function
Create `netlify/functions/scraper.js`:
```javascript
const { exec } = require('child_process');

exports.handler = async (event, context) => {
    // Your scraping logic here
    return {
        statusCode: 200,
        body: JSON.stringify({ success: true })
    };
};
```

#### Step 3: Deploy
1. Connect your GitHub repository
2. Netlify will auto-deploy

## 🛠 **Manual Backend Setup (If Cloud Fails)**

### **Step 1: Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### **Step 2: Install Skraper CLI**
```bash
# Download Skraper (you may need to build from source)
wget -O /usr/local/bin/skraper https://github.com/sokomishalov/skraper/releases/download/0.13.0/skraper
chmod +x /usr/local/bin/skraper
```

### **Step 3: Run Backend**
```bash
python app_enhanced.py
```

## 🔄 **Frontend Updates**

### **Update API URL**
Replace in `main-functional.js`:
```javascript
// Before
this.apiBaseUrl = 'http://localhost:5000/api';

// After (your cloud backend URL)
this.apiBaseUrl = 'https://your-backend-url.com/api';
```

### **Deploy Frontend**
1. **Netlify** (Recommended):
   - Connect GitHub repo
   - Auto-deploy on push
   - Set build command: `npm run build` (if using build tools)

2. **Vercel**:
   - Connect repository
   - Auto-deploy

3. **GitHub Pages**:
   - Push to `gh-pages` branch
   - Enable Pages in repository settings

## 📋 **Testing Facebook Scraping**

### **Test URLs:**
- `https://facebook.com/nike`
- `https://facebook.com/cocacola`
- `https://facebook.com/adidas`

### **Expected Results:**
- JSON data with posts
- Brand voice analysis
- Engagement patterns
- Content recommendations

## 🔍 **Troubleshooting**

### **"Backend not connected"**
1. Check backend URL in frontend code
2. Verify backend is running
3. Check CORS settings
4. Test API endpoints directly

### **"Failed to fetch"**
1. Backend URL incorrect
2. Backend not running
3. CORS blocked
4. Network issues

### **"Scraping failed"**
1. URL format incorrect
2. Platform not supported
3. Skraper CLI not installed
4. Rate limiting

## 🚀 **Production Deployment**

### **Environment Variables:**
```bash
# Backend
PORT=5000
FLASK_ENV=production
DATABASE_URL=your_database_url
REDIS_URL=your_redis_url

# Frontend
REACT_APP_API_URL=https://your-backend.com/api
```

### **Security Considerations:**
1. **Rate limiting** (implement in backend)
2. **API authentication** (if needed)
3. **HTTPS only**
4. **Input validation**
5. **Error handling** (don't expose sensitive info)

### **Performance Optimization:**
1. **Caching** (Redis, database)
2. **CDN** for static assets
3. **Load balancing** (for high traffic)
4. **Database optimization**

## 📊 **Monitoring**

### **Backend Health:**
```bash
curl https://your-backend.com/health
```

### **API Status:**
```bash
curl https://your-backend.com/api/scrape/status
```

### **Logs:**
- Render: Dashboard → Logs
- Heroku: `heroku logs --tail`
- Netlify: Dashboard → Functions → Logs

## 🎯 **Success Verification**

### **Test 1: Backend Health**
```bash
curl https://your-backend.com/health
```
Should return: `{"status": "healthy", ...}`

### **Test 2: Platform Support**
```bash
curl https://your-backend.com/api/platforms
```
Should return list of supported platforms

### **Test 3: Facebook Scraping**
```bash
curl -X POST https://your-backend.com/api/scrape/enhanced \
  -H "Content-Type: application/json" \
  -d '{"url": "https://facebook.com/nike", "limit": 10}'
```
Should return enhanced JSON data

## 🎉 **Expected Result**

After deployment, you should have:
- ✅ **Working backend** on cloud service
- ✅ **Updated frontend** pointing to cloud backend
- ✅ **Functional scraping** for Facebook and other platforms
- ✅ **Enhanced JSON data** for your AI agent
- ✅ **No more "backend not connected" errors**

## 📞 **Support**

If you encounter issues:
1. Check backend logs
2. Verify API endpoints
3. Test with curl
4. Check network tab in browser
5. Verify CORS settings

**Need help?** Provide:
- Backend URL
- Error messages
- Platform you're testing
- Expected vs actual results

---

**Ready to deploy?** Follow the Render.com option for the easiest setup!