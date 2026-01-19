import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key (first 20 chars): {api_key[:20]}...")
print(f"API Key length: {len(api_key)}")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "messages": [
        {
            "role": "user",
            "content": "Hello!"
        }
    ],
    "model": "grok-beta",
    "stream": False
}

print("\nTesting Grok API...")
response = requests.post(
    "https://api.x.ai/v1/chat/completions",
    headers=headers,
    json=payload
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text[:500]}")
