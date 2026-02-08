import google.generativeai as genai
import os

# User provided key
API_KEY = "AIzaSyCEjFapVppb5cSuRMBBlSvM1QKt0MbCJEU"

genai.configure(api_key=API_KEY)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
