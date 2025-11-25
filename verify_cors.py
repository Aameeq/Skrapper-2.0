import requests

try:
    print("Testing CORS headers for /api/scrape/enhanced...")
    response = requests.options(
        'http://127.0.0.1:5000/api/scrape/enhanced',
        headers={
            'Origin': 'https://skrapper.netlify.app',
            'Access-Control-Request-Method': 'POST'
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        if 'Access-Control' in key:
            print(f"{key}: {value}")
            
    if 'Access-Control-Allow-Origin' in response.headers:
        print("\n✅ CORS Headers present!")
    else:
        print("\n❌ CORS Headers MISSING!")
        
except Exception as e:
    print(f"Error: {e}")
