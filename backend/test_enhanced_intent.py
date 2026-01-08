from app.prompt_engine import generate_systematic_prompt

# Test queries
test_queries = [
    "create a report from this data for meta ads so I can send it to my manager",
    "who should be my target audience for fitness supplements",
    "how do I optimize my facebook ad campaign to reduce CPA"
]

print("Enhanced Intent Classification Test\n" + "="*80 + "\n")

for query in test_queries:
    print(f"\nQuery: {query}")
    print("-" * 80)
    
    result = generate_systematic_prompt(query)
    
    print(f"Intent: {result.intent}")
    print(f"Sub-Intent: {result.sub_intent}")
    print(f"Confidence: {result.confidence_score:.2f}")
    
    if result.context:
        print(f"Has Data: {result.context.get('has_data')}")
        print(f"Stakeholder: {result.context.get('stakeholder')}")
    
    print(f"\nSuggestions:")
    for i, suggestion in enumerate(result.suggestions, 1):
        print(f"  {i}. {suggestion}")
    
    print(f"\nGenerated STOK Preview:")
    print(f"Situation: {result.structured_prompt.situation[:100]}...")
    print("="*80)
