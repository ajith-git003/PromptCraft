from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import PromptRequest, PromptResponse
from app.prompt_analysis import analyze_prompt

app = FastAPI(title="PromptCraft API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (frontend access)
    allow_methods=["*"],
    allow_headers=["*"]
)

# Root route (for testing)
@app.get("/")
def read_root():
    return {"message": "Welcome to PromptCraft backend!"}

# Analysis route
@app.post("/analyze", response_model=PromptResponse)
def analyze_prompt_api(request: PromptRequest):
    analysis, optimized_prompt = analyze_prompt(request.prompt)
    return {"analysis": analysis, "optimized_prompt": optimized_prompt}
