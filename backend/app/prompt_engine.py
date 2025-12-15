import os
import google.generativeai as genai
from typing import List, Optional
from pydantic import BaseModel
import re

# Configure Gemini API
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
else:
    model = None
    print("Warning: GEMINI_API_KEY not found. Helper functions will return fallback data.")

class StructuredPrompt(BaseModel):
    situation: str
    task: str
    objective: str
    knowledge: str

class PromptAnalysis(BaseModel):
    original_prompt: str
    enhanced_prompt: str
    structured_prompt: StructuredPrompt
    intent: str
    confidence_score: int
    suggestions: List[str]

def identify_intent_fallback(text: str) -> str:
    """Simple intent detection for fallback."""
    text = text.lower()
    if any(k in text for k in ["code", "python", "function", "api", "app"]): return "coding"
    if any(k in text for k in ["image", "photo", "logo", "design"]): return "image"
    if any(k in text for k in ["write", "blog", "essay", "email"]): return "writing"
    if any(k in text for k in ["market", "brand", "audience", "ad"]): return "marketing"
    return "general"

def generate_systematic_prompt(prompt: str) -> PromptAnalysis:
    """Uses Gemini API to generate a high-quality STOK prompt."""
    
    if not model:
        # Fallback if no API key (prevents crashing)
        return PromptAnalysis(
            original_prompt=prompt,
            enhanced_prompt="Error: GEMINI_API_KEY not set. Please add it to your environment variables.",
            structured_prompt=StructuredPrompt(
                situation="API Key Missing",
                task="Please configure backend environment variables.",
                objective="Enable AI Features",
                knowledge="Get key from aistudio.google.com"
            ),
            intent="general",
            confidence_score=0,
            suggestions=["Add GEMINI_API_KEY to backend .env", "Deploy with env var"]
        )

    try:
        # Construct the prompt for Gemini
        system_instruction = f"""
        You are an expert prompt engineer. Analyze the user's request: "{prompt}"
        
        1. Identify the Intent (Coding, Image, Writing, Marketing, or General).
        2. Create a "Situation, Task, Objective, Knowledge" (STOK) framework analysis.
        3. Generate 3 specific, high-value suggestions to improve their request.
        
        Output strictly in this format (no markdown code blocks, just the text sections separated by special markers):
        
        [INTENT]
        (The intent here)
        
        [SITUATION]
        (Detailed situation with context)
        
        [TASK]
        (Specific instructions with bullet points)
        
        [OBJECTIVE]
        (Clear success criteria)
        
        [KNOWLEDGE]
        (Expert tips, best practices, bullet points)
        
        [SUGGESTIONS]
        (Suggestion 1)
        (Suggestion 2)
        (Suggestion 3)
        """
        
        response = model.generate_content(system_instruction)
        text_resp = response.text
        
        # Parse logic
        intent_match = re.search(r'\[INTENT\]\s*(.*?)\s*(?=\[SITUATION\])', text_resp, re.DOTALL)
        situation_match = re.search(r'\[SITUATION\]\s*(.*?)\s*(?=\[TASK\])', text_resp, re.DOTALL)
        task_match = re.search(r'\[TASK\]\s*(.*?)\s*(?=\[OBJECTIVE\])', text_resp, re.DOTALL)
        objective_match = re.search(r'\[OBJECTIVE\]\s*(.*?)\s*(?=\[KNOWLEDGE\])', text_resp, re.DOTALL)
        knowledge_match = re.search(r'\[KNOWLEDGE\]\s*(.*?)\s*(?=\[SUGGESTIONS\])', text_resp, re.DOTALL)
        suggestions_match = re.search(r'\[SUGGESTIONS\]\s*(.*)', text_resp, re.DOTALL)
        
        intent = intent_match.group(1).strip() if intent_match else "general"
        situation = situation_match.group(1).strip() if situation_match else "Could not generate situation."
        task = task_match.group(1).strip() if task_match else "Could not generate task."
        objective = objective_match.group(1).strip() if objective_match else "Could not generate objective."
        knowledge = knowledge_match.group(1).strip() if knowledge_match else "Could not generate knowledge."
        suggestions_raw = suggestions_match.group(1).strip() if suggestions_match else ""
        
        # Split suggestions by newlines and clean up
        suggestions = [s.strip('- ').strip() for s in suggestions_raw.split('\n') if s.strip()]
        
        stok = StructuredPrompt(
            situation=situation,
            task=task,
            objective=objective,
            knowledge=knowledge
        )
        
        full_text = f"""**Situation**
{situation}

**Task**
{task}

**Objective**
{objective}

**Knowledge**
{knowledge}"""

        return PromptAnalysis(
            original_prompt=prompt,
            enhanced_prompt=full_text,
            structured_prompt=stok,
            intent=intent,
            confidence_score=98,
            suggestions=suggestions[:3]
        )

    except Exception as e:
        # Error handling
        return PromptAnalysis(
            original_prompt=prompt,
            enhanced_prompt=f"Error generating prompt: {str(e)}",
            structured_prompt=StructuredPrompt(situation="Error", task="Error", objective="Error", knowledge="Error"),
            intent="error",
            confidence_score=0,
            suggestions=["Check API Quota", "Verify Internet Connection"]
        )
