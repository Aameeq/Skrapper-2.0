#!/usr/bin/env python3
"""
Skraper Web Backend - Flask API Service (Modified to use yt-dlp)
Integrates with yt-dlp to provide web scraping functionality
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

# Supported platforms mapping (may need adjustment for yt-dlp)
SUPPORTED_PLATFORMS = {
    'instagram': 'instagram',
    'tiktok': 'tiktok',
    'twitter': 'twitter', # X
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
    """Service class to handle yt-dlp operations (was Skraper)"""

    def __init__(self):
        # yt-dlp is installed system-wide, so we just need to call it
        # No need to find a specific executable path like Skraper
        self.yt_dlp_path = "yt-dlp" # Assumes yt-dlp is in PATH

    def detect_platform(self, url):
        """Detect social media platform from URL (basic pattern matching)"""
        # This is a simplified detector, yt-dlp handles many more internally
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

    def scrape_data(self, url, content_type='posts', limit=50, output_format='json'):
        """Scrape data using yt-dlp"""

        # yt-dlp often works directly with the full URL
        # It handles platform detection internally
        # Limiting posts might require playlist options, which vary by site
        # For now, focus on getting metadata for the URL provided

        # Build command for yt-dlp to dump JSON metadata
        cmd = [
            self.yt_dlp_path,
            '--dump-json',  # Output metadata in JSON format
            '--no-playlist', # Only info for the item itself, not a playlist/channel (if applicable)
            # '--playlist-start', '1', # Example if limiting items within a playlist
            # '--playlist-end', str(limit), # Example if limiting items within a playlist
            '--extractor-args', 'youtube:player_client=default', # Sometimes helps with YouTube
            url
        ]

        logger.info(f"Running command: {' '.join(cmd)}")

        try:
            # Run yt-dlp command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode != 0:
                logger.error(f"Yt-dlp error: {result.stderr}")
                raise Exception(f"Scraping failed: {result.stderr}")

            # yt-dlp --dump-json outputs one JSON object per line for each video/file found
            # If the URL points to a single post/video, it should output one line.
            # If it's a user profile or playlist, it might output multiple lines.
            output_lines = result.stdout.strip().split('\n')

            if not output_lines or output_lines == ['']:
                 raise Exception("Yt-dlp returned no output.")

            # Attempt to parse the first line as JSON (often the primary item)
            # For more complex scenarios (playlists), you'd iterate through lines
            try:
                raw_data = json.loads(output_lines[0])
                logger.info("Successfully parsed yt-dlp output as JSON")
                return raw_data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON output from yt-dlp: {e}")
                logger.debug(f"Raw yt-dlp output (first 500 chars): {result.stdout[:500]}")
                raise Exception("Invalid JSON response format from yt-dlp")

        except subprocess.TimeoutExpired:
            raise Exception("Scraping timeout - operation took too long")
        except Exception as e:
            logger.error(f"Error running yt-dlp: {str(e)}")
            raise

    def format_results_for_web(self, raw_data, url, platform, limit):
        """Format yt-dlp results for web frontend (Adapted from Skraper formatting)"""
        # This is a basic adaptation. yt-dlp's JSON schema differs from Skraper's.
        # You'll need to map fields from aw_data (yt-dlp output) to your desired web format.

        # Create metadata
        metadata = {
            "url": url,
            "platform": platform, # Detected platform
            "scraped_at": datetime.utcnow().isoformat() + "Z",
            "content_type": "posts", # Or adapt based on yt-dlp output
            "output_format": "json",
            "limit": limit # Applied limit (if applicable)
        }

        # Example of mapping common fields from yt-dlp output
        # yt-dlp fields might include: id, title, description, uploader, upload_date, duration, view_count, like_count, thumbnail, formats, etc.
        formatted_data = []

        # Assuming aw_data is a single item's metadata dict from yt-dlp
        if isinstance(raw_data, dict):
            formatted_post = self.format_post_item_ytdlp(raw_data, platform, 0) # Index 0 for single item
            formatted_data.append(formatted_post)
        # If aw_data was a list (e.g., from a playlist), iterate through it.
        # elif isinstance(raw_data, list):
        #    for i, item in enumerate(raw_data[:limit]): # Apply limit here if needed
        #        formatted_post = self.format_post_item_ytdlp(item, platform, i)
        #        formatted_data.append(formatted_post)

        # Calculate statistics (example based on common yt-dlp fields)
        total_likes = sum(post.get('likes', 0) for post in formatted_data)
        total_comments = sum(post.get('comments', 0) for post in formatted_data)
        # Note: yt-dlp doesn't always get comment counts, unlike Skraper potentially parsing HTML
        total_shares = 0 # Shares are rarely available via public API scraping

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

    def format_post_item_ytdlp(self, item, platform, index):
        """Format a single item from yt-dlp output"""
        # Map yt-dlp fields to your desired schema
        # Example mapping - adjust based on actual yt-dlp output and your frontend needs
        return {
            "id": item.get('id', f"item_{index + 1}"), # Use yt-dlp's ID or generate one
            "username": item.get('uploader', 'unknown'), # Often 'uploader'
            "content": item.get('description', item.get('title', '')), # Description or title as content
            "timestamp": self._convert_ytdlp_date(item.get('upload_date')), # Convert date format
            "likes": item.get('like_count', 0), # Use like_count if available
            "comments": item.get('comment_count', 0), # Use comment_count if available
            "shares": 0, # Shares usually not available via yt-dlp
            "media_url": item.get('thumbnail', ''), # Thumbnail URL, or primary video/audio URL from 'formats'
            "caption": item.get('description', ''), # Description often serves as caption
            "hashtags": [], # yt-dlp rarely extracts hashtags directly
            "mentions": [], # yt-dlp rarely extracts mentions directly
            "duration": item.get('duration'), # Duration in seconds
            "view_count": item.get('view_count', 0) # View count if available
        }

    def _convert_ytdlp_date(self, ytdlp_date_str):
        """Convert yt-dlp date string (YYYYMMDD) to ISO format"""
        if ytdlp_date_str and len(ytdlp_date_str) == 8:
            try:
                year = int(ytdlp_date_str[0:4])
                month = int(ytdlp_date_str[4:6])
                day = int(ytdlp_date_str[6:8])
                dt = datetime(year, month, day)
                return dt.isoformat() + "Z"
            except (ValueError, IndexError):
                pass # Return original string or None if conversion fails
        return ytdlp_date_str # Return original if format is unexpected


# Initialize service
skraper_service = SkraperService()

@app.route('/')
def index():
    """Root endpoint with API information"""
    return jsonify({
        "name": "Skraper Web API (using yt-dlp)",
        "version": "1.0.0",
        "description": "Web API for social media scraping using yt-dlp library",
        "endpoints": {
            "GET /health": "Health check",
            "POST /api/scrape": "Scrape social media data",
            "GET /api/platforms": "Get supported platforms"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    # Check if yt-dlp is available by running a simple command
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, timeout=10)
        yt_dlp_available = result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        yt_dlp_available = False

    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "yt_dlp_available": yt_dlp_available
    })

@app.route('/api/platforms')
def get_platforms():
    """Get supported platforms"""
    return jsonify({
        "platforms": list(SUPPORTED_PLATFORMS.keys()), # Use the list from SUPPORTED_PLATFORMS
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
        limit = min(int(data.get('limit', 50)), 100)  # Max 100 posts (adjust as needed)
        output_format = data.get('output_format', 'json')

        # Scrape data using yt-dlp
        raw_data = skraper_service.scrape_data(
            url=url,
            content_type=content_type,
            limit=limit,
            output_format=output_format
        )

        # Format results using the adapted formatter
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
    # Check if yt-dlp is available
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, timeout=10)
        yt_dlp_available = result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        yt_dlp_available = False

    return jsonify({
        "yt_dlp_available": yt_dlp_available,
        "yt_dlp_path": "yt-dlp", # Path is system-wide
        "supported_platforms": len(SUPPORTED_PLATFORMS), # Approximation
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
    # Check if yt-dlp is available (optional startup check)
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info("Yt-dlp executable found and accessible.")
        else:
            logger.warning("Yt-dlp executable not found or not accessible via 'yt-dlp' command.")
    except FileNotFoundError:
        logger.warning("Yt-dlp executable not found. Please install yt-dlp.")
    except subprocess.TimeoutExpired:
        logger.warning("Yt-dlp version check timed out.")

    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

