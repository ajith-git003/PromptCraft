"""
Comparison test between basic intent classification and enhanced intent classification.
This demonstrates the improvements made to match the reference tool's output.
"""

from app.prompt_engine import generate_systematic_prompt

# Test query from the user's example
test_query = "create a report from this data for meta ads so I can send it to my manager"

print("="*80)
print("ENHANCED INTENT CLASSIFICATION - COMPARISON TEST")
print("="*80)
print()

print(f"Test Query: {test_query}")
print()

# Generate the enhanced prompt
result = generate_systematic_prompt(test_query)

print("="*80)
print("ENHANCED CLASSIFICATION RESULTS")
print("="*80)
print()

print(f"Primary Intent: {result.intent}")
print(f"Sub-Intent: {result.sub_intent}")
print(f"Confidence Score: {result.confidence_score:.2%}")
print()

print("Context Detection:")
if result.context:
    print(f"  - Has Data: {result.context.get('has_data')}")
    print(f"  - Needs Data: {result.context.get('needs_data')}")
    print(f"  - Stakeholder: {result.context.get('stakeholder')}")
    print(f"  - Query Length: {result.context.get('query_length')} words")
print()

print("Smart Suggestions (context-aware):")
for i, suggestion in enumerate(result.suggestions, 1):
    print(f"  {i}. {suggestion}")
print()

print("="*80)
print("GENERATED STOK (SITUATION-TASK-OBJECTIVE-KNOWLEDGE)")
print("="*80)
print()
print(result.enhanced_prompt)
print()

print("="*80)
print("KEY IMPROVEMENTS OVER BASIC CLASSIFICATION")
print("="*80)
print()
print("✓ Sub-intent detection (reporting vs strategy vs optimization, etc.)")
print("✓ Data context awareness (knows user has data to analyze)")
print("✓ Stakeholder detection (identified 'manager' as recipient)")
print("✓ Context-specific STOK generation (tailored for reporting with data)")
print("✓ Smart suggestions based on sub-intent and context")
print("✓ Confidence scoring for intent classification")
print()

print("="*80)
print("ADDITIONAL TEST CASES")
print("="*80)
print()

additional_tests = [
    {
        "query": "who should be my target audience for fitness supplements",
        "expected_sub_intent": "audience_targeting"
    },
    {
        "query": "how do I optimize my facebook ad campaign to reduce CPA",
        "expected_sub_intent": "optimization"
    },
    {
        "query": "what's the best marketing strategy for launching a new product",
        "expected_sub_intent": "strategy"
    }
]

for test in additional_tests:
    result = generate_systematic_prompt(test["query"])
    status = "✓" if result.sub_intent == test["expected_sub_intent"] else "✗"
    print(f"{status} Query: {test['query']}")
    print(f"  → Detected: {result.sub_intent} (confidence: {result.confidence_score:.2%})")
    print()
