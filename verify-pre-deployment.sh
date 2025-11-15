#!/bin/bash

# Skrapper Pre-Deployment Verification Script

echo "🔍 Skrapper Pre-Deployment Verification"
echo "======================================"

# Check 1: Verify index.html has no Supabase references
echo "1. Checking for Supabase references in index.html..."
if grep -q "supabase" index.html; then
    echo "❌ ERROR: Supabase references found in index.html"
    exit 1
else
    echo "✅ No Supabase references found in index.html"
fi

# Check 2: Verify correct JavaScript file is referenced
echo "2. Checking JavaScript file reference..."
if grep -q "main-functional.js" index.html; then
    echo "✅ Correct JavaScript file (main-functional.js) referenced"
else
    echo "❌ ERROR: main-functional.js not found in index.html"
    exit 1
fi

# Check 3: Verify backend Dockerfile exists
echo "3. Checking backend Dockerfile..."
if [ -f "backend/Dockerfile" ]; then
    echo "✅ Backend Dockerfile found"
else
    echo "❌ ERROR: Backend Dockerfile not found"
    exit 1
fi

# Check 4: Verify backend requirements.txt exists
echo "4. Checking backend requirements.txt..."
if [ -f "backend/requirements.txt" ]; then
    echo "✅ Backend requirements.txt found"
else
    echo "❌ ERROR: Backend requirements.txt not found"
    exit 1
fi

# Check 5: Verify backend app.py exists
echo "5. Checking backend app.py..."
if [ -f "backend/app.py" ]; then
    echo "✅ Backend app.py found"
else
    echo "❌ ERROR: Backend app.py not found"
    exit 1
fi

# Check 6: Verify API URL in main-functional.js
echo "6. Checking API URL configuration..."
if grep -q "apiBaseUrl" main-functional.js; then
    current_url=$(grep "apiBaseUrl" main-functional.js | cut -d'"' -f2)
    echo "✅ API URL configured: $current_url"
    echo "   Note: This will need to be updated with actual Render deployment URL"
else
    echo "❌ ERROR: apiBaseUrl not found in main-functional.js"
    exit 1
fi

# Check 7: Verify resources directory exists
echo "7. Checking resources directory..."
if [ -d "resources" ]; then
    echo "✅ Resources directory found"
else
    echo "❌ ERROR: Resources directory not found"
    exit 1
fi

echo ""
echo "🎉 Pre-deployment verification complete!"
echo ""
echo "📋 Deployment Checklist:"
echo "   ✅ Frontend modifications complete"
echo "   ✅ Backend Dockerfile ready"
echo "   ✅ No authentication required"
echo ""
echo "🚀 Ready for deployment:"
echo "   1. Deploy backend to Render (requires API key)"
echo "   2. Update frontend API URL with Render URL"
echo "   3. Deploy frontend to Netlify (requires API key)"
echo ""
echo "📁 Deployment package location: $(pwd)"