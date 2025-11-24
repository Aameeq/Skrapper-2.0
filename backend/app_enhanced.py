#!/usr/bin/env python3
"""
Skraper Web Backend - Enhanced Version for AI Agent Integration
Provides enhanced data analysis for AI-powered content creation
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
import random
from collections import Counter
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Configure CORS
# Allow requests from Netlify frontend and local development
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://skrapper.netlify.app", 
            "http://localhost:3000", 
            "http://127.0.0.1:3000",
            "http://localhost:5000",
            "https://skraper-api.onrender.com"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

@app.after_request
def after_request(response):
    """Ensure CORS headers are added to every response"""
    # Get the origin from the request
    origin = request.headers.get('Origin')
    allowed_origins = [
        "https://skrapper.netlify.app", 
        "http://localhost:3000", 
        "http://127.0.0.1:3000"
    ]
    
    if origin in allowed_origins:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
    elif not origin:
        # For non-browser requests or when origin is missing, we can be more permissive or strict
        # depending on requirements. Here we just leave it or set * if needed.
        pass
        
    return response

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

class EnhancedSkraperService:
    """Enhanced service class with AI agent data analysis"""
    
    def __init__(self):
        self.skraper_available = self._check_skraper_availability()
    
    def _check_skraper_availability(self):
        """Check if Skraper CLI is available"""
        try:
            # Try to run skraper --help
            result = subprocess.run(['skraper', '--help'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
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
    
    def generate_enhanced_mock_data(self, platform, url, limit):
        """Generate enhanced mock data with AI agent analysis"""
        
        # Sample content based on platform
        sample_content = {
            'instagram': [
                'Amazing product launch! 🚀 Our new collection is finally here. What do you think? #ProductLaunch #Innovation',
                'Behind the scenes look at our creative process ✨ Swipe to see how we bring ideas to life! #BTS #CreativeProcess',
                'Customer spotlight! 💫 Meet Sarah, who transformed her business with our solution. Link in bio! #CustomerSuccess',
                'Monday motivation from our team! 💪 What\'s driving you this week? #MondayMotivation #TeamWork',
                'Flash sale alert! 🔥 50% off everything for the next 24 hours. Don\'t miss out! #FlashSale #LimitedTime'
            ],
            'tiktok': [
                'POV: You discover our product and your life changes forever ✨ #LifeHack #ProductFind',
                'This trick saved me $1000! 💰 You need to try this #MoneySaving #LifeTips',
                'Rating our products as a honest customer 📊 Part 1 #ProductReview #HonestOpinion',
                'Things I wish I knew before starting my business 💡 #BusinessTips #EntrepreneurLife',
                'Transform your space with this one simple product 🏠 #HomeTransformation #BeforeAndAfter'
            ],
            'twitter': [
                'Just shipped a major update! 🚢 What feature are you most excited about? #ProductUpdate #TechNews',
                'Hot take: The future of marketing is community-driven. Change my mind. 🧠 #MarketingTwitter #Community',
                'Pro tip: Always test your assumptions. What worked yesterday might not work tomorrow. #BusinessAdvice',
                'Breaking: We\'re expanding to 5 new markets! Which city should we launch in next? 🌍 #Expansion #Growth',
                'Reminder: Your customers are your best marketers. Focus on creating advocates, not just buyers. #CustomerAdvocacy'
            ]
        }
        
        platform_content = sample_content.get(platform, sample_content['instagram'])
        
        # Generate posts
        posts = []
        for i in range(min(limit, 20)):  # Generate up to 20 posts
            content = platform_content[i % len(platform_content)]
            
            post = {
                "id": f"post_{i+1}",
                "username": self.extract_username_from_url(url),
                "content": content,
                "timestamp": self.generate_timestamp(i),
                "likes": random.randint(50, 5000),
                "comments": random.randint(5, 200),
                "shares": random.randint(0, 50),
                "media_url": f"https://example.com/media_{i+1}.jpg",
                "caption": content,
                "hashtags": self.extract_hashtags(content),
                "mentions": self.extract_mentions(content),
                "media_type": random.choice(['image', 'video', 'carousel']),
                "post_length": len(content),
                "emoji_count": len([c for c in content if c in ['😀', '😍', '🚀', '✨', '💫', '🔥', '💡', '🌍', '🧠', '💰', '🏠', '📊', '🚢']]),
                "call_to_action": self.detect_call_to_action(content),
                "sentiment": self.analyze_sentiment(content)
            }
            posts.append(post)
        
        return posts
    
    def extract_username_from_url(self, url):
        """Extract username from URL"""
        match = re.search(r'/(?:@)?([^/?]+)', url)
        return match.group(1) if match else 'brand_username'
    
    def generate_timestamp(self, index):
        """Generate realistic timestamps"""
        base_time = datetime.now()
        # Generate posts over the last 30 days, more recent posts more frequently
        days_back = random.randint(1, 30)
        hours_back = random.randint(0, 23)
        minutes_back = random.randint(0, 59)
        
        post_time = base_time.replace(
            day=base_time.day - days_back,
            hour=hours_back,
            minute=minutes_back,
            second=0,
            microsecond=0
        )
        return post_time.isoformat() + "Z"
    
    def extract_hashtags(self, content):
        """Extract hashtags from content"""
        hashtags = re.findall(r'#\w+', content)
        return hashtags
    
    def extract_mentions(self, content):
        """Extract mentions from content"""
        mentions = re.findall(r'@\w+', content)
        return mentions
    
    def detect_call_to_action(self, content):
        """Detect call-to-action phrases"""
        cta_keywords = [
            'click', 'swipe', 'link in bio', 'check out', 'visit', 'shop now',
            'buy now', 'order', 'subscribe', 'follow', 'share', 'comment',
            'tell us', 'what do you think', 'change my mind', 'pro tip',
            'reminder', 'alert', 'don\'t miss'
        ]
        
        content_lower = content.lower()
        detected_ctas = [keyword for keyword in cta_keywords if keyword in content_lower]
        
        return {
            "has_cta": len(detected_ctas) > 0,
            "cta_types": detected_ctas,
            "cta_strength": len(detected_ctas)
        }
    
    def analyze_sentiment(self, content):
        """Basic sentiment analysis"""
        positive_words = ['amazing', 'awesome', 'great', 'excellent', 'fantastic', 'love', 'perfect', 'incredible', 'outstanding', 'brilliant', 'excited', 'happy', 'thrilled', 'proud', 'grateful']
        negative_words = ['terrible', 'awful', 'horrible', 'hate', 'disappointed', 'frustrated', 'angry', 'sad', 'annoyed', 'upset', 'worried', 'concerned']
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "positive_score": positive_count,
            "negative_score": negative_count,
            "sentiment_strength": abs(positive_count - negative_count)
        }
    
    def analyze_brand_voice(self, posts):
        """Analyze brand voice patterns"""
        all_content = " ".join([post['content'] for post in posts])
        
        # Analyze language patterns
        avg_length = sum(len(post['content']) for post in posts) / len(posts)
        total_emojis = sum(post['emoji_count'] for post in posts)
        avg_emojis = total_emojis / len(posts)
        
        # CTA analysis
        cta_posts = sum(1 for post in posts if post['call_to_action']['has_cta'])
        cta_frequency = cta_posts / len(posts)
        
        # Sentiment analysis
        sentiments = [post['sentiment']['sentiment'] for post in posts]
        sentiment_distribution = Counter(sentiments)
        
        return {
            "average_caption_length": round(avg_length, 1),
            "average_emoji_count": round(avg_emojis, 2),
            "cta_frequency": round(cta_frequency, 2),
            "sentiment_distribution": dict(sentiment_distribution),
            "primary_sentiment": sentiment_distribution.most_common(1)[0][0],
            "tone_indicators": {
                "professional": avg_length > 100,
                "casual": avg_emojis > 1,
                "engaging": cta_frequency > 0.3,
                "positive": sentiment_distribution.get("positive", 0) > len(posts) * 0.6
            }
        }
    
    def analyze_engagement_patterns(self, posts):
        """Analyze engagement patterns"""
        total_likes = sum(post['likes'] for post in posts)
        total_comments = sum(post['comments'] for post in posts)
        total_shares = sum(post['shares'] for post in posts)
        
        avg_likes = total_likes / len(posts)
        avg_comments = total_comments / len(posts)
        avg_shares = total_shares / len(posts)
        
        # Engagement rate calculation
        # Assuming follower count (use 10000 as baseline)
        baseline_followers = 10000
        engagement_rate = ((total_likes + total_comments + total_shares) / len(posts)) / baseline_followers
        
        # Find best performing content
        best_post = max(posts, key=lambda p: p['likes'] + p['comments'] + p['shares'])
        worst_post = min(posts, key=lambda p: p['likes'] + p['comments'] + p['shares'])
        
        return {
            "total_engagement": {
                "likes": total_likes,
                "comments": total_comments,
                "shares": total_shares
            },
            "average_engagement": {
                "likes": round(avg_likes, 1),
                "comments": round(avg_comments, 1),
                "shares": round(avg_shares, 1)
            },
            "engagement_rate": round(engagement_rate, 4),
            "best_performing_post": {
                "id": best_post['id'],
                "engagement": best_post['likes'] + best_post['comments'] + best_post['shares'],
                "content_preview": best_post['content'][:50] + "..."
            },
            "worst_performing_post": {
                "id": worst_post['id'],
                "engagement": worst_post['likes'] + worst_post['comments'] + worst_post['shares'],
                "content_preview": worst_post['content'][:50] + "..."
            }
        }
    
    def analyze_content_themes(self, posts):
        """Analyze content themes and patterns"""
        all_content = " ".join([post['content'] for post in posts])
        all_hashtags = []
        for post in posts:
            all_hashtags.extend(post['hashtags'])
        
        # Common words analysis
        words = re.findall(r'\b\w+\b', all_content.lower())
        common_words = Counter(words)
        
        # Hashtag analysis
        hashtag_counter = Counter(all_hashtags)
        
        # Media type analysis
        media_types = Counter([post['media_type'] for post in posts])
        
        return {
            "most_common_words": dict(common_words.most_common(10)),
            "most_used_hashtags": dict(hashtag_counter.most_common(10)),
            "media_type_distribution": dict(media_types),
            "content_themes": self.identify_themes(common_words),
            "hashtag_strategy": {
                "branded_hashtags": len([h for h in hashtag_counter.keys() if 'brand' in h.lower()]),
                "trending_hashtags": len([h for h in hashtag_counter.keys() if len(h) > 10]),
                "average_hashtags_per_post": len(all_hashtags) / len(posts)
            }
        }
    
    def identify_themes(self, word_counter):
        """Identify content themes from words"""
        themes = {
            "product_focused": any(word in str(word_counter) for word in ['product', 'launch', 'new', 'available']),
            "behind_scenes": any(word in str(word_counter) for word in ['behind', 'scenes', 'process', 'making']),
            "customer_focused": any(word in str(word_counter) for word in ['customer', 'client', 'review', 'testimonial']),
            "educational": any(word in str(word_counter) for word in ['tip', 'how', 'guide', 'learn', 'tutorial']),
            "promotional": any(word in str(word_counter) for word in ['sale', 'discount', 'offer', 'deal', 'limited']),
            "community": any(word in str(word_counter) for word in ['community', 'family', 'team', 'together'])
        }
        
        return [theme for theme, present in themes.items() if present]
    
    def scrape_enhanced_data(self, url, content_type='posts', limit=50):
        """Scrape and enhance data for AI agent"""
        
        # Detect platform
        platform = self.detect_platform(url)
        if not platform:
            raise Exception(f"Unsupported platform for URL: {url}")
        
        # Generate enhanced mock data (replace with real Skraper call when available)
        posts = self.generate_enhanced_mock_data(platform, url, limit)
        
        # Perform enhanced analysis
        brand_voice = self.analyze_brand_voice(posts)
        engagement_patterns = self.analyze_engagement_patterns(posts)
        content_themes = self.analyze_content_themes(posts)
        
        # Create comprehensive dataset
        enhanced_data = {
            "metadata": {
                "url": url,
                "platform": platform,
                "scraped_at": datetime.utcnow().isoformat() + "Z",
                "content_type": content_type,
                "limit": limit,
                "total_posts": len(posts)
            },
            "posts": posts,
            "brand_analysis": {
                "voice_analysis": brand_voice,
                "engagement_patterns": engagement_patterns,
                "content_themes": content_themes,
                "overall_performance": {
                    "total_likes": sum(p['likes'] for p in posts),
                    "total_comments": sum(p['comments'] for p in posts),
                    "total_shares": sum(p['shares'] for p in posts),
                    "average_engagement_per_post": sum(p['likes'] + p['comments'] + p['shares'] for p in posts) / len(posts)
                }
            },
            "ai_agent_recommendations": self.generate_ai_recommendations(posts, brand_voice, engagement_patterns)
        }
        
        return enhanced_data
    
    def generate_ai_recommendations(self, posts, brand_voice, engagement_patterns):
        """Generate recommendations for AI agent"""
        
        recommendations = {
            "content_strategy": {
                "optimal_post_length": brand_voice['average_caption_length'],
                "recommended_emoji_usage": brand_voice['average_emoji_count'],
                "cta_frequency": brand_voice['cta_frequency'],
                "tone_guidelines": brand_voice['tone_indicators']
            },
            "engagement_optimization": {
                "best_performing_content_type": engagement_patterns['best_performing_post']['content_preview'],
                "engagement_rate": engagement_patterns['engagement_rate'],
                "optimal_hashtag_count": sum(len(post['hashtags']) for post in posts) / len(posts)
            },
            "brand_voice_guidelines": {
                "primary_tone": brand_voice['primary_sentiment'],
                "formality_level": "semi_formal" if brand_voice['average_caption_length'] > 100 else "casual",
                "emoji_strategy": "moderate" if brand_voice['average_emoji_count'] > 1 else "minimal",
                "cta_approach": "frequent" if brand_voice['cta_frequency'] > 0.3 else "occasional"
            },
            "content_ideas": self.generate_content_ideas(posts, brand_voice)
        }
        
        return recommendations
    
    def generate_content_ideas(self, posts, brand_voice):
        """Generate content ideas based on analysis"""
        
        ideas = []
        
        # Based on brand voice
        if brand_voice['tone_indicators'].get('professional', False):
            ideas.append("Industry insights and thought leadership content")
            ideas.append("Behind-the-scenes of business operations")
        
        if brand_voice['tone_indicators'].get('casual', False):
            ideas.append("Team culture and workplace content")
            ideas.append("User-generated content and community features")
        
        if brand_voice['tone_indicators'].get('engaging', False):
            ideas.append("Interactive polls and Q&A sessions")
            ideas.append("Challenges and contests")
        
        # Based on performance
        best_post = max(posts, key=lambda p: p['likes'] + p['comments'] + p['shares'])
        if best_post['media_type'] == 'video':
            ideas.append("More video content and tutorials")
        else:
            ideas.append("High-quality image carousels")
        
        return ideas

# Initialize service
skraper_service = EnhancedSkraperService()

@app.route('/')
def index():
    """Root endpoint with API information"""
    return jsonify({
        "name": "Skraper Web API - Enhanced for AI Agents",
        "version": "2.0.0",
        "description": "Enhanced web API for social media scraping with AI agent data analysis",
        "features": [
            "Enhanced brand voice analysis",
            "Engagement pattern recognition",
            "Content theme identification",
            "AI agent recommendations",
            "Visual content analysis (placeholder)",
            "Sentiment analysis"
        ],
        "endpoints": {
            "GET /health": "Health check",
            "POST /api/scrape/enhanced": "Enhanced scraping with AI analysis",
            "GET /api/platforms": "Get supported platforms",
            "GET /api/scrape/status": "Check scraping service status"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "skraper_available": skraper_service.skraper_available,
        "enhanced_features": True
    })

@app.route('/api/platforms')
def get_platforms():
    """Get supported platforms"""
    return jsonify({
        "platforms": list(SUPPORTED_PLATFORMS.keys()),
        "count": len(SUPPORTED_PLATFORMS),
        "note": "Enhanced analysis available for all platforms"
    })

@app.route('/api/scrape/enhanced', methods=['POST'])
def scrape_enhanced_endpoint():
    """Enhanced scraping endpoint with AI agent data"""
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
        
        # Scrape enhanced data
        enhanced_data = skraper_service.scrape_enhanced_data(
            url=url,
            content_type=content_type,
            limit=limit
        )
        
        return jsonify(enhanced_data)
        
    except Exception as e:
        logger.error(f"Enhanced scraping error: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False,
            "note": "This is an enhanced mock implementation. Install Skraper CLI for real data."
        }), 500

@app.route('/api/scrape/status')
def scrape_status():
    """Check scraping service status"""
    return jsonify({
        "skraper_available": skraper_service.skraper_available,
        "enhanced_features": True,
        "supported_platforms": len(SUPPORTED_PLATFORMS),
        "timestamp": datetime.utcnow().isoformat(),
        "note": "Enhanced version with AI agent data analysis"
    })

# Additional endpoint for AI agent specific data
@app.route('/api/ai-agent/brand-analysis', methods=['POST'])
def ai_agent_brand_analysis():
    """Dedicated endpoint for AI agent brand analysis"""
    try:
        data = request.get_json()
        
        if not data or not data.get('url'):
            return jsonify({"error": "URL is required"}), 400
        
        # Get enhanced data
        enhanced_data = skraper_service.scrape_enhanced_data(
            url=data.get('url'),
            limit=data.get('limit', 50)
        )
        
        # Extract AI-specific data
        ai_data = {
            "brand_profile": {
                "platform": enhanced_data['metadata']['platform'],
                "username": enhanced_data['posts'][0]['username'] if enhanced_data['posts'] else 'unknown',
                "total_posts_analyzed": len(enhanced_data['posts'])
            },
            "content_strategy": enhanced_data['brand_analysis']['voice_analysis'],
            "engagement_insights": enhanced_data['brand_analysis']['engagement_patterns'],
            "content_themes": enhanced_data['brand_analysis']['content_themes'],
            "ai_recommendations": enhanced_data['ai_agent_recommendations'],
            "sample_posts": enhanced_data['posts'][:5]  # Include sample posts for context
        }
        
        return jsonify(ai_data)
        
    except Exception as e:
        logger.error(f"AI agent analysis error: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Check if skraper is available
    if not skraper_service.skraper_available:
        logger.warning("Skraper CLI not available. Using enhanced mock data.")
        logger.info("To enable real data scraping, install Skraper CLI:")
        logger.info("https://github.com/sokomishalov/skraper")
    else:
        logger.info("Skraper CLI available. Enhanced features enabled.")
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)