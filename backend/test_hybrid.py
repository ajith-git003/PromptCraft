import sys
import os

# Add current directory to path so we can import app modules
sys.path.append(os.path.join(os.getcwd(), 'app'))

from app.prompt_engine import generate_systematic_prompt
from app.embeddings import analyze_similarity

def test_hybrid_system():
    print("=== Testing Hybrid AI System ===")
    
    # Test 1: Vague Prompt
    print("\n[Test 1] Vague Prompt: 'do it'")
    vague_prompt = "do it"
    sim_score, is_vague = analyze_similarity(vague_prompt)
    print(f"Similarity Score: {sim_score:.4f}")
    print(f"Is Vague? {is_vague}")
    
    if is_vague:
        print("✅ PASS: Correctly identified as vague.")
    else:
        print("❌ FAIL: Should be vague.")

    # Test 2: Good Prompt (Similar to curated)
    print("\n[Test 2] Good Prompt: 'Write a Python script to scrape data'")
    good_prompt = "Write a Python script to scrape product data from Amazon using BeautifulSoup"
    sim_score_good, is_vague_good = analyze_similarity(good_prompt)
    print(f"Similarity Score: {sim_score_good:.4f}")
    print(f"Is Vague? {is_vague_good}")
    
    if not is_vague_good and sim_score_good > 0.8:
        print("✅ PASS: Correctly identified as high quality.")
    else:
        print(f"❌ FAIL: Should be high quality. Score: {sim_score_good}")

    # Test 3: Full End-to-End Generation
    print("\n[Test 3] End-to-End Generation")
    try:
        result = generate_systematic_prompt("Create a snake game in python")
        print("Generated Structured Prompt successfully.")
        print(f"Similarity Score in Result: {result.similarity_score}")
        print(f"Is Vague in Result: {result.is_vague}")
        print("Enhancement Preview:\n" + result.original_prompt)
    except Exception as e:
        print(f"❌ FAIL: Generation Error: {e}")

if __name__ == "__main__":
    test_hybrid_system()
