import spacy
from typing import Dict, List, Optional
from pydantic import BaseModel

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.lang.en import English
    nlp = English()

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

def identify_intent(text: str) -> str:
    """Identify the intent of the prompt (coding, image, writing, marketing, general)."""
    doc = nlp(text.lower())
    
    coding_keywords = {"code", "python", "script", "function", "api", "app", "html", "css", "react", "bug", "error", "debug", "calculator", "dev"}
    image_keywords = {"image", "photo", "picture", "logo", "design", "draw", "illustration", "sketch", "art", "4k", "realistic"}
    writing_keywords = {"write", "story", "essay", "article", "blog", "email", "letter", "poem", "summary", "rewrite"}
    marketing_keywords = {"marketing", "brand", "audience", "strategy", "sell", "product", "market", "customer", "demographic", "campaign", "ad", "social media"}
    
    tokens = {token.lemma_ for token in doc}
    
    if tokens & coding_keywords:
        return "coding"
    if tokens & image_keywords:
        return "image"
    if tokens & writing_keywords:
        return "writing"
    if tokens & marketing_keywords:
        return "marketing"
    return "general"

def generate_dynamic_suggestions(prompt: str, intent: str) -> List[str]:
    """Generate smart suggestions based on what is MISSING from the prompt."""
    prompt_lower = prompt.lower()
    suggestions = []

    if intent == "coding":
        # Language Check
        if not any(lang in prompt_lower for lang in ["python", "javascript", "java", "c++", "html", "css", "sql", "react", "node"]):
            suggestions.append("Specify the programming language (e.g., Python, JavaScript)")
        elif "python" in prompt_lower:
            suggestions.append("Specify target Python version (e.g., 3.9+)")
            suggestions.append("Mention preferred libraries (e.g., Pandas, Typer)")

        # Application Type Check
        if "calculator" in prompt_lower:
            if not any(ui in prompt_lower for ui in ["gui", "cli", "web", "tkinter", "flask", "react"]):
                suggestions.append("Specify the interface: CLI, GUI (Tkinter/PyQt), or Web?")
            suggestions.append("Do you need scientific functions (sin/cos/tan)?")
        
        # General Coding Checks
        if "test" not in prompt_lower:
            suggestions.append("Include requirements for unit tests (pytest/unittest)")
    
    elif intent == "image":
        if "--ar" not in prompt_lower and "aspect ratio" not in prompt_lower:
            suggestions.append("Specify aspect ratio (e.g., 16:9, 1:1)")
        if "style" not in prompt_lower:
            suggestions.append("Define an art style (e.g., Cyberpunk, Oil Painting)")

    elif intent == "marketing":
        if "budget" not in prompt_lower:
            suggestions.append("Define the budget range")
        if "competitor" not in prompt_lower:
            suggestions.append("Identify key competitors")

    # Fallback if list is too short
    if len(suggestions) < 2:
        suggestions.append("Add constraints or limitations")
    
    return suggestions[:3] # Return top 3 unique suggestions

def extract_rich_knowledge(prompt: str, intent: str) -> str:
    """Inject expert knowledge based on specific keywords."""
    prompt_lower = prompt.lower()
    knowledge_points = []

    if intent == "coding":
        # Base coding knowledge
        knowledge_points.append("Follow Clean Code principles (DRY, SOLID)")
        
        if "python" in prompt_lower:
            knowledge_points.append("Follow PEP 8 style guide for Python code")
            knowledge_points.append("Use Type Hinting (typing module) for better maintainability")
            knowledge_points.append("Include comprehensive Docstrings for all functions/classes")

        if "calculator" in prompt_lower:
            knowledge_points.append("Implement the Shunting-yard algorithm for parsing mathematical expressions")
            knowledge_points.append("Separate business logic (Calculation) from UI code")
            knowledge_points.append("Handle floating-point arithmetic precision issues (decimal module)")
            knowledge_points.append("Support keyboard input binding for better UX")
            knowledge_points.append("Implement a robust history tracking system with Undo/Redo")

        if "api" in prompt_lower:
            knowledge_points.append("Use proper HTTP Status Codes (200, 201, 400, 500)")
            knowledge_points.append("Implement Rate Limiting and Authentication (JWT/OAuth)")
    
    # Generic fallback
    if not knowledge_points:
        knowledge_points.append("Use industry standard best practices")
    
    return "\n- ".join(knowledge_points)

def generate_coding_stok(original: str) -> StructuredPrompt:
    knowledge_content = extract_rich_knowledge(original, "coding")
    
    # Customize Task based on specific keywords
    task_intro = f"Create a production-ready solution for '{original}'."
    if "calculator" in original.lower():
        task_intro = "Develop an advanced Calculator application that goes beyond basic arithmetic."

    return StructuredPrompt(
        situation=f"You are an expert Senior Software Engineer with 10+ years of experience. You need to architect and build '{original}' ensuring scalability, maintainability, and user experience.",
        task=f"""{task_intro} The solution must include:
-   Robust error handling (e.g., try/except blocks, custom exceptions)
-   Modular architecture separating concerns
-   Production-grade features (logging, config management)
-   Full implementation of requested features with edge case coverage""",
        objective=f"Deliver a high-quality, 'copy-paste ready' codebase for '{original}' that serves as a gold standard reference implementation.",
        knowledge=f"- {knowledge_content}"
    )

def generate_image_stok(original: str) -> StructuredPrompt:
    return StructuredPrompt(
        situation=f"You need a high-quality visual asset representing '{original}' that meets professional artistic standards.",
        task=f"Create a stunning visual representation of '{original}' with focus on composition, lighting, and texture.",
        objective="Generate a photorealistic or artistically consistent image without visual artifacts.",
        knowledge="""- Use the Rule of Thirds for composition
- Ensure lighting matches the mood (e.g., golden hour, neon)
- Avoid common AI artifacts (distorted hands)
- Use negative prompts to filter out unwanted elements"""
    )

def generate_writing_stok(original: str) -> StructuredPrompt:
    return StructuredPrompt(
        situation=f"You need a compelling written piece about '{original}' that engages the reader.",
        task=f"Write a comprehensive piece about '{original}' with a strong hook and logical flow.",
        objective="Produce content that captures the reader's attention and delivers the message effectively.",
        knowledge="""- Use active voice for better engagement
- Vary sentence structure to maintain rhythm
- Include sensory details or specific examples
- Tailor vocabulary to the intended audience"""
    )

def generate_marketing_stok(original: str) -> StructuredPrompt:
    return StructuredPrompt(
        situation=f"You are developing a marketing strategy for '{original}' to identify target segments.",
        task=f"Identify and describe 4-5 distinct audience segments for '{original}' including demographics and psychographics.",
        objective="Create clear audience profiles to guide messaging and maximizing market reach.",
        knowledge="""- Consider budget-conscious vs premium consumers
- Focus on pain points and solutions
- Analyze B2B and B2C segments if applicable
- Consider the full customer journey"""
    )

def generate_general_stok(original: str) -> StructuredPrompt:
    return StructuredPrompt(
        situation=f"You need a comprehensive answer for '{original}'.",
        task=f"Analyze '{original}' and provide a detailed response with definitions, examples, and logical arguments.",
        objective="Deliver a authoritative response that fully addresses the user's needs.",
        knowledge="""- Synthesize information from reliable sources
- Break down complex ideas
- Use analogies and clear formatting"""
    )

def generate_systematic_prompt(prompt: str) -> PromptAnalysis:
    """Main function to take a raw prompt and return a systematic one."""
    intent = identify_intent(prompt)
    
    if intent == "coding":
        stok = generate_coding_stok(prompt)
    elif intent == "image":
        stok = generate_image_stok(prompt)
    elif intent == "writing":
        stok = generate_writing_stok(prompt)
    elif intent == "marketing":
        stok = generate_marketing_stok(prompt)
    else:
        stok = generate_general_stok(prompt)
    
    # Generate dynamic suggestions based on intent and content
    suggestions = generate_dynamic_suggestions(prompt, intent)
    
    # Create the full text version for copy-pasting
    full_text = f"""**Situation**
{stok.situation}

**Task**
{stok.task}

**Objective**
{stok.objective}

**Knowledge**
{stok.knowledge}"""

    return PromptAnalysis(
        original_prompt=prompt,
        enhanced_prompt=full_text,
        structured_prompt=stok,
        intent=intent,
        confidence_score=95,
        suggestions=suggestions
    )
