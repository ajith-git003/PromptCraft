import os
import openai
import numpy as np
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI Client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # User said "Open AI API keys" so we expect this env var
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Curated High-Quality Prompts (The "Gold Standard")
CURATED_PROMPTS = [
    "Write a Python script to scrape product data from Amazon using BeautifulSoup and Handle pagination.",
    "Create a React component for a responsive navigation bar with a hamburger menu for mobile devices.",
    "Generate a marketing email for a new SaaS product launch focusing on productivity features.",
    "Design a SQL query to calculate the monthly recurring revenue (MRR) for a subscription business.",
    "Explain the concept of Recursion in computer science with a simple factorial example.",
    "Write a detailed blog post about the benefits of intermittent fasting backed by scientific studies.",
    "Create a 4k realistic image of a cyberpunk city street at night with neon lights and rain.",
    "Debug this generic error in my Django application related to database migrations.",
    "Optimize this functions time complexity from O(n^2) to O(n log n)."
]

# Cache for embeddings
CURATED_EMBEDDINGS = []

def get_embedding(text: str, model="text-embedding-3-small") -> List[float]:
    """Generates an embedding vector for the input text."""
    text = text.replace("\n", " ")
    try:
        return client.embeddings.create(input=[text], model=model).data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

def load_curated_embeddings():
    """Pre-computes embeddings for the curated prompts on startup."""
    global CURATED_EMBEDDINGS
    if not CURATED_EMBEDDINGS:
        print("Loading curated embeddings...")
        for prompt in CURATED_PROMPTS:
            emb = get_embedding(prompt)
            if emb:
                CURATED_EMBEDDINGS.append(emb)
        print(f"Loaded {len(CURATED_EMBEDDINGS)} curated embeddings.")

def cosine_similarity(a, b):
    """Calculates cosine similarity between two vectors."""
    if not a or not b: return 0.0
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def analyze_similarity(user_prompt: str) -> Tuple[float, bool]:
    """
    Analyzes the user prompt against curated high-quality prompts.
    Returns: (max_similarity_score, is_vague)
    """
    # Ensure curated are loaded
    if not CURATED_EMBEDDINGS:
        load_curated_embeddings()
    
    user_embedding = get_embedding(user_prompt)
    if not user_embedding:
        return 0.0, True # Default to vague if error

    max_score = 0.0
    for curated_emb in CURATED_EMBEDDINGS:
        score = cosine_similarity(user_embedding, curated_emb)
        if score > max_score:
            max_score = score
    
    # Threshold: If similarity is below 0.3, it's likely very different/vague compared to our "good" examples
    # Note: text-embedding-3-small usually has higher baseline similarity, so 0.3-0.4 is a conservative vague threshold.
    is_vague = max_score < 0.35 
    
    return max_score, is_vague
