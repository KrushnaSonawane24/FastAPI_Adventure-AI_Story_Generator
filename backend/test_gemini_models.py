import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("Available Gemini Models:")
print("-" * 60)
for m in genai.list_models():
    print(f"Name: {m.name}")
    print(f"Supported methods: {m.supported_generation_methods}")
    print("-" * 60)
