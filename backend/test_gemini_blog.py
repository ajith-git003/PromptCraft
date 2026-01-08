from app.prompt_engine import generate_systematic_prompt

# Test the exact query from the user
test_query = "write me blog about Gemini 3"

print("Testing STOK Generation for: " + test_query)
print("=" * 80 + "\n")

result = generate_systematic_prompt(test_query)

print("Intent:", result.intent)
print("\n" + "=" * 80)
print("\nFull Enhanced Prompt:\n")
print(result.enhanced_prompt)
print("\n" + "=" * 80)
print("\nSuggestions:")
for i, suggestion in enumerate(result.suggestions, 1):
    print(f"  {i}. {suggestion}")
print("\n" + "=" * 80)
