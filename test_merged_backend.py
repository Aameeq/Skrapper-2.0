import requests
import json

print("Testing merged backend with yt-dlp integration...")
print("=" * 60)

# Test URL - YouTube video
test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

print(f"\nTest URL: {test_url}")
print("\nSending request to backend...")

try:
    response = requests.post(
        'http://127.0.0.1:5000/api/scrape/enhanced',
        json={"url": test_url, "limit": 1},
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n" + "=" * 60)
        print("RESPONSE SUMMARY")
        print("=" * 60)
        
        # Metadata
        metadata = data.get('metadata', {})
        print(f"\nPlatform: {metadata.get('platform')}")
        print(f"Scraping Method: {metadata.get('scraping_method')}")
        print(f"yt-dlp Available: {metadata.get('yt_dlp_available')}")
        print(f"Total Posts: {metadata.get('total_posts')}")
        
        # Posts
        posts = data.get('posts', [])
        if posts:
            post = posts[0]
            print(f"\n--- First Post ---")
            print(f"ID: {post.get('id')}")
            print(f"Username: {post.get('username')}")
            print(f"Content: {post.get('content', '')[:100]}...")
            print(f"Likes: {post.get('likes')}")
            print(f"Comments: {post.get('comments')}")
            print(f"Views: {post.get('view_count')}")
            print(f"Duration: {post.get('duration')} seconds")
        
        # AI Analysis
        brand_analysis = data.get('brand_analysis', {})
        voice_analysis = brand_analysis.get('voice_analysis', {})
        
        print(f"\n--- AI Analysis ---")
        print(f"Average Caption Length: {voice_analysis.get('average_caption_length')}")
        print(f"Average Emoji Count: {voice_analysis.get('average_emoji_count')}")
        print(f"Primary Sentiment: {voice_analysis.get('primary_sentiment')}")
        
        # Recommendations
        recommendations = data.get('ai_agent_recommendations', {})
        brand_voice = recommendations.get('brand_voice_guidelines', {})
        
        print(f"\n--- Brand Voice Guidelines ---")
        print(f"Primary Tone: {brand_voice.get('primary_tone')}")
        print(f"Formality Level: {brand_voice.get('formality_level')}")
        print(f"Emoji Strategy: {brand_voice.get('emoji_strategy')}")
        
        print("\n" + "=" * 60)
        
        if metadata.get('scraping_method') == 'yt-dlp':
            print("✅ SUCCESS: Real scraping with yt-dlp + AI analysis working!")
        else:
            print("⚠️  WARNING: Using mock data (yt-dlp not available or failed)")
        
    else:
        print(f"\n❌ ERROR: {response.text}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 60)
print("Test complete!")
