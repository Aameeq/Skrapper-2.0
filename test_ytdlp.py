import subprocess
import json

print("Testing yt-dlp integration...")
print("=" * 50)

# Test 1: Check if yt-dlp is installed
print("\n1. Checking yt-dlp installation...")
try:
    result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print(f"✅ yt-dlp is installed: {result.stdout.strip()}")
    else:
        print(f"❌ yt-dlp check failed: {result.stderr}")
        exit(1)
except Exception as e:
    print(f"❌ yt-dlp not found: {e}")
    exit(1)

# Test 2: Test with a real YouTube URL
print("\n2. Testing yt-dlp with a YouTube video...")
test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video

try:
    cmd = [
        'yt-dlp',
        '--dump-json',
        '--no-download',
        '--playlist-items', '1',
        test_url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        # Parse the JSON output
        data = json.loads(result.stdout)
        
        print(f"✅ Successfully scraped video data!")
        print(f"   Title: {data.get('title', 'N/A')}")
        print(f"   Uploader: {data.get('uploader', 'N/A')}")
        print(f"   Views: {data.get('view_count', 'N/A'):,}")
        print(f"   Duration: {data.get('duration', 'N/A')} seconds")
        print(f"   Upload Date: {data.get('upload_date', 'N/A')}")
        
    else:
        print(f"❌ yt-dlp command failed:")
        print(f"   Error: {result.stderr}")
        
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse JSON output: {e}")
    print(f"   Raw output (first 200 chars): {result.stdout[:200]}")
except subprocess.TimeoutExpired:
    print(f"❌ yt-dlp command timed out")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("Test complete!")
