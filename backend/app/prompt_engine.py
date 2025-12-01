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
    
    coding_keywords = {"code", "python", "script", "function", "api", "app", "html", "css", "react", "bug", "error", "debug", "calculator"}
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

def generate_coding_stok(original: str) -> StructuredPrompt:
    return StructuredPrompt(
        situation=f"You need a functional application or script for '{original}' with an intuitive user interface (if applicable) and polished code structure that provides a professional developer experience.",
        task=f"""The assistant should create complete, production-ready code for '{original}' that includes:
-   Core functionality implemented efficiently
-   A clean, modern structure (or GUI if applicable)
-   Clear display of outputs and results
-   Proper error handling and edge case management
-   Responsive design or robust logic flow""",
        objective=f"Deliver a fully functional solution for '{original}' that users can run immediately with minimal setup, featuring clean code that makes it easy to understand and modify.",
        knowledge="""-   The code should support standard operations relevant to the task
-   The implementation should use modern best practices and design principles
-   Variable naming should be clear and consistent
-   The solution should include comments explaining complex logic
-   Dependencies should be clearly listed"""
    )

def generate_image_stok(original: str) -> StructuredPrompt:
    return StructuredPrompt(
        situation=f"You need a high-quality visual asset representing '{original}' that meets professional artistic standards for composition, lighting, and detail.",
        task=f"""Create a stunning visual representation of '{original}' that includes:
-   A clear, focused subject matter
-   Cinematic lighting and atmospheric depth
-   High-resolution textures and details (8k quality)
-   Harmonious color palette and composition
-   Specific artistic style (e.g., photorealistic, digital art)""",
        objective="Generate a photorealistic or artistically consistent image that captures the essence of the subject with perfect composition and no visual artifacts.",
        knowledge="""-   Use the Rule of Thirds for composition
-   Ensure lighting matches the mood (e.g., golden hour, neon, soft studio)
-   Avoid common AI artifacts (distorted hands, blurry text)
-   Maintain consistent style throughout the image
-   Use negative prompts to filter out unwanted elements"""
    )

def generate_writing_stok(original: str) -> StructuredPrompt:
    return StructuredPrompt(
        situation=f"You need a compelling written piece about '{original}' that engages the reader and communicates the core message effectively.",
        task=f"""Write a comprehensive piece about '{original}' that includes:
-   A strong, attention-grabbing hook
-   Logical flow and structured paragraphs
-   Clear and persuasive arguments or narrative
-   Appropriate tone and voice for the target audience
-   A memorable conclusion""",
        objective="Produce content that captures the reader's attention, maintains a consistent tone, and delivers the message effectively without fluff.",
        knowledge="""-   Use active voice for better engagement
-   Vary sentence structure to maintain rhythm
-   Include sensory details or specific examples
-   Ensure grammatical correctness and clarity
-   Tailor the vocabulary to the intended audience"""
    )

def generate_marketing_stok(original: str) -> StructuredPrompt:
    return StructuredPrompt(
        situation=f"You are developing a marketing strategy for '{original}' and need to identify and define the target audience segments that would be most receptive to your product.",
        task=f"""Identify and describe 4-5 distinct audience segments for '{original}', including:
-   Demographics (age, location, income)
-   Psychographics (interests, values, lifestyle)
-   Purchasing behaviors and key drivers
-   Primary motivations for engaging with the brand""",
        objective="Create a clear audience profile that will guide marketing messaging, channel selection, and product positioning to maximize market reach and brand resonance.",
        knowledge="""-   Consider audiences ranging from budget-conscious to premium consumers
-   Analyze both B2B and B2C segments if applicable
-   Focus on pain points and how the product solves them
-   Look for underserved niches in the current market
-   Consider the customer journey from awareness to loyalty"""
    )

def generate_general_stok(original: str) -> StructuredPrompt:
    return StructuredPrompt(
        situation=f"You need a comprehensive and well-researched answer for '{original}' that provides deep insight and actionable information.",
        task=f"""Analyze the request '{original}' and provide a detailed response that includes:
-   A direct and clear answer to the core question
-   Key concepts and definitions relevant to the topic
-   Step-by-step explanations or logical arguments
-   Real-world examples or case studies to illustrate points
-   Potential challenges or alternative perspectives""",
        objective="Deliver a high-quality, authoritative response that fully addresses the user's needs, clears up any confusion, and provides value beyond a simple answer.",
        knowledge="""-   Synthesize information from reliable sources
-   Break down complex ideas into simple, understandable terms
-   Use analogies to explain abstract concepts
-   Structure the response with clear headings and bullet points
-   Anticipate the 'why' and 'how' behind the user's query"""
    )

def generate_systematic_prompt(prompt: str) -> PromptAnalysis:
    """Main function to take a raw prompt and return a systematic one."""
    intent = identify_intent(prompt)
    
    if intent == "coding":
        stok = generate_coding_stok(prompt)
        suggestions = ["Specify the programming language", "Mention specific libraries", "Describe expected input/output"]
    elif intent == "image":
        stok = generate_image_stok(prompt)
        suggestions = ["Add aspect ratio (e.g., --ar 16:9)", "Specify an art style", "Describe lighting conditions"]
    elif intent == "writing":
        stok = generate_writing_stok(prompt)
        suggestions = ["Define the target audience", "Specify word count", "Choose a specific tone"]
    elif intent == "marketing":
        stok = generate_marketing_stok(prompt)
        suggestions = ["Define the budget range", "Specify the geographic region", "Identify key competitors"]
    else:
        stok = generate_general_stok(prompt)
        suggestions = ["Be more specific about the goal", "Provide context", "Ask for a specific format"]
    
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
