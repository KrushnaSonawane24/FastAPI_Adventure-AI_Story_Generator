import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "messages": [
        {
            "role": "user",
            "content": "Say 'Groq is working!'"
        }
    ],
    "model": "llama-3.3-70b-versatile",
    "max_tokens": 50
}

print("Testing Groq API...")
response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers=headers,
    json=payload
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"✅ Response: {result['choices'][0]['message']['content']}")
else:
    print(f"❌ Error: {response.text}")
