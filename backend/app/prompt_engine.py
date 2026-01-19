import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Optional
from pydantic import BaseModel
import re

# Load environment variables from .env file
load_dotenv()

from app.embeddings import analyze_similarity

# Configure OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

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
    similarity_score: float
    is_vague: bool
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
    """Uses OpenAI API to generate a high-quality STOK prompt."""
    
    if not client:
        # Fallback if no API key (prevents crashing)
        return PromptAnalysis(
            original_prompt=prompt,
            enhanced_prompt="Error: OPENAI_API_KEY not set. Please add it to your environment variables.",
            structured_prompt=StructuredPrompt(
                situation="API Key Missing",
                task="Please configure backend environment variables.",
                objective="Enable AI Features",
                knowledge="Get key from platform.openai.com"
            ),
            intent="general",
            confidence_score=0,
            similarity_score=0.0,
            is_vague=True,
            suggestions=["Add OPENAI_API_KEY to backend .env", "Deploy with env var"]
        )

    try:
        # Hybrid Analysis: Calculate Similarity first
        similarity_score, is_vague = analyze_similarity(prompt)
        
        # Context note for the LLM
        vague_context = ""
        if is_vague:
            vague_context = "\nNOTE: This prompt seems VAGUE or low-quality based on semantic analysis. Please provide extra guidance on how to make it specific."

        # Construct the prompt for OpenAI
        system_instruction = f"""
        You are an expert prompt engineer. The user wants: "{prompt}"
        {vague_context}
        
        Create an action-oriented STOK (Situation, Task, Objective, Knowledge) framework that helps them accomplish this goal.
        
        IMPORTANT GUIDELINES:
        - Situation: Define the ACTUAL scenario they are working in (NOT a meta-analysis of their request)
        - Task: Provide specific, actionable instructions for what needs to be done
        - Objective: Define clear success criteria for the output
        - Knowledge: List required information, best practices, or context needed
        - Use proper markdown formatting with dashes (-) for bullet points
        - Make content specific to their request, not generic
        
        1. Identify the Intent (Coding, Image, Writing, Marketing, or General).
        2. Create the STOK framework.
        3. Generate 3 specific, actionable suggestions.
        
        Output strictly in this format (no markdown code blocks, just the text sections separated by special markers):
        
        [INTENT]
        (The intent here)
        
        [SITUATION]
        (Define the ACTUAL working scenario - e.g., "You are writing a blog post for an audience interested in AI technology...")
        
        [TASK]
        (Specific instructions with proper markdown bullet points using dashes)
        
        [OBJECTIVE]
        (Clear success criteria)
        
        [KNOWLEDGE]
        (Required information, best practices - use proper markdown bullet points with dashes)
        
        [SUGGESTIONS]
        - (Suggestion 1)
        - (Suggestion 2)
        - (Suggestion 3)
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert prompt engineer."},
                {"role": "user", "content": system_instruction}
            ],
            temperature=0.7
        )
        text_resp = response.choices[0].message.content
        
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
            similarity_score=float(similarity_score),
            is_vague=is_vague,
            suggestions=suggestions[:3]
        )

    except Exception as e:
        # Error handling with detailed logging
        error_msg = f"Error generating prompt: {str(e)}"
        print(f"\n❌ GEMINI API ERROR: {error_msg}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        return PromptAnalysis(
            original_prompt=prompt,
            enhanced_prompt=error_msg,
            structured_prompt=StructuredPrompt(
                situation=f"API Error: {type(e).__name__}",
                task=str(e),
                objective="Fix the API configuration",
                knowledge="Check console for detailed error"
            ),
            intent="error",
            confidence_score=0,
            similarity_score=0.0,
            is_vague=True,
            suggestions=["Check API Quota", "Verify Internet Connection", "Check API Key"]
        )
