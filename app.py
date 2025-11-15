#!/usr/bin/env python3
"""
Skraper Web Backend - Flask API Service
Integrates with Skraper CLI tool to provide web scraping functionality
"""

import os
import json
import subprocess
import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import asyncio
from datetime import datetime
import re
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Supported platforms mapping
SUPPORTED_PLATFORMS = {
    'instagram': 'instagram',
    'tiktok': 'tiktok', 
    'twitter': 'twitter',
    'youtube': 'youtube',
    'facebook': 'facebook',
    'reddit': 'reddit',
    'pinterest': 'pinterest',
    'flickr': 'flickr',
    'tumblr': 'tumblr',
    'telegram': 'telegram',
    'twitch': 'twitch',
    'vimeo': 'vimeo',
    'vk': 'vk',
    '9gag': '9gag',
    'ifunny': 'ifunny',
    'coub': 'coub',
    'odnoklassniki': 'odnoklassniki',
    'pikabu': 'pikabu'
}

class SkraperService:
    """Service class to handle Skraper operations"""
    
    def __init__(self):
        self.skraper_path = self._find_skraper_executable()
    
    def _find_skraper_executable(self):
        """Find the skraper executable"""
        # Try common installation paths
        possible_paths = [
            '/usr/local/bin/skraper',
            '/usr/bin/skraper',
            os.path.expanduser('~/.local/bin/skraper'),
            os.path.join(os.getcwd(), 'skraper'),
            'skraper'  # Assume in PATH
        ]
        
        for path in possible_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
        
        # Check if skraper is in PATH
        try:
            result = subprocess.run(['which', 'skraper'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
            
        return None
    
    def detect_platform(self, url):
        """Detect social media platform from URL"""
        patterns = {
            'instagram': r'(?:instagram\.com|instagr\.am)',
            'tiktok': r'tiktok\.com',
            'twitter': r'(?:twitter\.com|x\.com)',
            'youtube': r'(?:youtube\.com|youtu\.be)',
            'facebook': r'facebook\.com',
            'reddit': r'reddit\.com',
            'pinterest': r'pinterest\.com',
            'flickr': r'flickr\.com',
            'tumblr': r'tumblr\.com',
            'telegram': r't\.me',
            'twitch': r'twitch\.tv',
            'vimeo': r'vimeo\.com',
            'vk': r'vk\.com',
            '9gag': r'9gag\.com',
            'ifunny': r'ifunny\.co',
            'coub': r'coub\.com',
            'odnoklassniki': r'odnoklassniki\.ru',
            'pikabu': r'pikabu\.ru'
        }
        
        for platform, pattern in patterns.items():
            if re.search(pattern, url, re.IGNORECASE):
                return platform
        
        return None
    
    def extract_path_from_url(self, url, platform):
        """Extract the path component needed by Skraper"""
        # Remove protocol and domain, keep the path
        path = re.sub(r'^https?://[^/]+', '', url)
        
        # Platform-specific path extraction
        if platform == 'instagram':
            # Extract username or path
            match = re.search(r'/([^/?]+)', path)
            return match.group(1) if match else path
        elif platform == 'tiktok':
            # Extract @username
            match = re.search(r'/@([^/?]+)', path)
            return f"/@{match.group(1)}" if match else path
        elif platform == 'twitter':
            # Extract username
            match = re.search(r'/([^/?]+)', path)
            return match.group(1) if match else path
        elif platform == 'youtube':
            # Extract channel/user path
            return path  # Keep full path for YouTube
        
        return path
    
    def scrape_data(self, url, content_type='posts', limit=50, output_format='json'):
        """Scrape data using Skraper CLI"""
        
        if not self.skraper_path:
            raise Exception("Skraper executable not found. Please install Skraper CLI tool.")
        
        # Detect platform
        platform = self.detect_platform(url)
        if not platform:
            raise Exception(f"Unsupported platform for URL: {url}")
        
        # Extract path
        path = self.extract_path_from_url(url, platform)
        
        # Build command
        cmd = [
            self.skraper_path,
            platform,
            path,
            '-n', str(limit),
            '-t', output_format
        ]
        
        if content_type == 'media-only':
            cmd.append('-m')
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        try:
            # Run skraper command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Skraper error: {result.stderr}")
                raise Exception(f"Scraping failed: {result.stderr}")
            
            # Parse the output
            if output_format == 'json':
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON output: {result.stdout[:500]}")
                    raise Exception("Invalid response format from Skraper")
            else:
                return {"raw_output": result.stdout}
                
        except subprocess.TimeoutExpired:
            raise Exception("Scraping timeout - operation took too long")
        except Exception as e:
            logger.error(f"Error running skraper: {str(e)}")
            raise
    
    def format_results_for_web(self, raw_data, url, platform, limit):
        """Format skraper results for web frontend"""
        
        # Create metadata
        metadata = {
            "url": url,
            "platform": platform,
            "scraped_at": datetime.utcnow().isoformat() + "Z",
            "content_type": "posts",
            "output_format": "json",
            "limit": limit
        }
        
        # Format data based on platform and response format
        formatted_data = []
        
        if isinstance(raw_data, list):
            # Direct list of posts
            for i, item in enumerate(raw_data[:limit]):
                formatted_post = self.format_post_item(item, platform, i)
                formatted_data.append(formatted_post)
        elif isinstance(raw_data, dict):
            # Structured response
            if 'posts' in raw_data:
                posts = raw_data['posts']
            elif 'data' in raw_data:
                posts = raw_data['data']
            else:
                posts = [raw_data]
            
            for i, item in enumerate(posts[:limit]):
                formatted_post = self.format_post_item(item, platform, i)
                formatted_data.append(formatted_post)
        
        # Calculate statistics
        total_likes = sum(post.get('likes', 0) for post in formatted_data)
        total_comments = sum(post.get('comments', 0) for post in formatted_data)
        total_shares = sum(post.get('shares', 0) for post in formatted_data)
        
        statistics = {
            "total_posts": len(formatted_data),
            "media_items": len([p for p in formatted_data if p.get('media_url')]),
            "engagement_metrics": {
                "total_likes": total_likes,
                "total_comments": total_comments,
                "total_shares": total_shares
            }
        }
        
        return {
            "metadata": metadata,
            "data": formatted_data,
            "statistics": statistics
        }
    
    def format_post_item(self, item, platform, index):
        """Format a single post item"""
        
        # Handle different response formats from different platforms
        if isinstance(item, dict):
            # Direct post object
            return {
                "id": item.get('id', f"post_{index + 1}"),
                "username": item.get('username', 'unknown'),
                "content": item.get('content', item.get('text', item.get('caption', ''))),
                "timestamp": item.get('timestamp', item.get('created_at', datetime.utcnow().isoformat())),
                "likes": item.get('likes', item.get('like_count', 0)),
                "comments": item.get('comments', item.get('comment_count', 0)),
                "shares": item.get('shares', item.get('share_count', 0)),
                "media_url": item.get('media_url', item.get('image_url', item.get('video_url', '')),
                "caption": item.get('caption', ''),
                "hashtags": item.get('hashtags', []),
                "mentions": item.get('mentions', [])
            }
        else:
            # String content
            return {
                "id": f"post_{index + 1}",
                "username": "unknown",
                "content": str(item),
                "timestamp": datetime.utcnow().isoformat(),
                "likes": 0,
                "comments": 0,
                "shares": 0,
                "media_url": "",
                "caption": "",
                "hashtags": [],
                "mentions": []
            }

# Initialize service
skraper_service = SkraperService()

@app.route('/')
def index():
    """Root endpoint with API information"""
    return jsonify({
        "name": "Skraper Web API",
        "version": "1.0.0",
        "description": "Web API for social media scraping using Skraper library",
        "endpoints": {
            "GET /health": "Health check",
            "POST /api/scrape": "Scrape social media data",
            "GET /api/platforms": "Get supported platforms"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "skraper_available": skraper_service.skraper_path is not None
    })

@app.route('/api/platforms')
def get_platforms():
    """Get supported platforms"""
    return jsonify({
        "platforms": list(SUPPORTED_PLATFORMS.keys()),
        "count": len(SUPPORTED_PLATFORMS)
    })

@app.route('/api/scrape', methods=['POST'])
def scrape_endpoint():
    """Main scraping endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        url = data.get('url')
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Optional parameters
        content_type = data.get('content_type', 'posts')
        limit = min(int(data.get('limit', 50)), 100)  # Max 100 posts
        output_format = data.get('output_format', 'json')
        
        # Scrape data
        raw_data = skraper_service.scrape_data(
            url=url,
            content_type=content_type,
            limit=limit,
            output_format=output_format
        )
        
        # Format results
        platform = skraper_service.detect_platform(url)
        formatted_results = skraper_service.format_results_for_web(
            raw_data, url, platform, limit
        )
        
        return jsonify(formatted_results)
        
    except Exception as e:
        logger.error(f"Scraping error: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@app.route('/api/scrape/status')
def scrape_status():
    """Check scraping service status"""
    return jsonify({
        "skraper_available": skraper_service.skraper_path is not None,
        "skraper_path": skraper_service.skraper_path,
        "supported_platforms": len(SUPPORTED_PLATFORMS),
        "timestamp": datetime.utcnow().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Check if skraper is available
    if not skraper_service.skraper_path:
        logger.warning("Skraper executable not found. Please install Skraper CLI tool.")
        logger.info("Installation instructions: https://github.com/sokomishalov/skraper")
    else:
        logger.info(f"Skraper executable found at: {skraper_service.skraper_path}")
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)