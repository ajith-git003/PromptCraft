from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.prompt_engine import generate_systematic_prompt, PromptAnalysis

app = FastAPI(title="AI Prompt Studio API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (frontend access)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

# Root route (for testing)
@app.get("/")
def read_root():
    return {"message": "Welcome to AI Prompt Studio Backend! 🚀"}

# Generation route
@app.post("/generate", response_model=PromptAnalysis)
def generate_prompt_api(request: PromptRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    analysis = generate_systematic_prompt(request.prompt)
    return analysis
