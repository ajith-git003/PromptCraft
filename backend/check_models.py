import google.generativeai as genai

API_KEY = "AIzaSyASCrEIdPJNia-2wipt3IB1MGsuqbd82SA"
genai.configure(api_key=API_KEY)

print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")
