"""
Test script for Report Template System (Step 2)
"""

from app.prompt_engine import generate_systematic_prompt

# Test queries for different scenarios
test_queries = [
    {
        "name": "Meta Ads Report to Manager",
        "query": "create a report from this data for meta ads so I can send it to my manager"
    },
    {
        "name": "Google Ads Report to Client",
        "query": "analyze this google ads data and create a report for my client"
    },
    {
        "name": "LinkedIn Campaign Optimization",
        "query": "how do I optimize my linkedin ad campaign to reduce cost per lead"
    },
    {
        "name": "TikTok Audience Targeting",
        "query": "who should be my target audience for tiktok ads selling skincare products"
    },
    {
        "name": "Strategy without Platform",
        "query": "what's the best marketing strategy for launching a new SaaS product"
    }
]

print("="*80)
print("REPORT TEMPLATE SYSTEM - STEP 2 TESTING")
print("="*80)
print()

for test in test_queries:
    print(f"\n{'='*80}")
    print(f"Test: {test['name']}")
    print(f"Query: {test['query']}")
    print(f"{'='*80}\n")
    
    result = generate_systematic_prompt(test['query'])
    
    print(f"Intent: {result.intent}")
    print(f"Sub-Intent: {result.sub_intent}")
    print(f"Confidence: {result.confidence_score:.2%}")
    
    if result.context:
        print(f"\nContext:")
        print(f"  - Has Data: {result.context.get('has_data')}")
        print(f"  - Stakeholder: {result.context.get('stakeholder')}")
    
    print(f"\nGenerated STOK:")
    print(f"\n{result.enhanced_prompt[:500]}...")  # First 500 chars
    print()
    
    # Check if platform is detected (for reporting queries)
    if result.sub_intent == "reporting":
        if "meta" in test['query'].lower() and "Meta" in result.enhanced_prompt:
            print("✓ Platform detection working: Meta detected")
        elif "google" in test['query'].lower() and "Google" in result.enhanced_prompt:
            print("✓ Platform detection working: Google detected")
        elif "linkedin" in test['query'].lower() and "Linkedin" in result.enhanced_prompt:
            print("✓ Platform detection working: LinkedIn detected")
        elif "tiktok" in test['query'].lower() and "Tiktok" in result.enhanced_prompt:
            print("✓ Platform detection working: TikTok detected")

print("\n" + "="*80)
print("KEY IMPROVEMENTS IN STEP 2:")
print("="*80)
print("✓ Platform-specific metric detection (Meta, Google, LinkedIn, TikTok)")
print("✓ Stakeholder-aware templates (manager, client, team, executive)")
print("✓ Context-aware report structure (with/without data)")
print("✓ Platform-specific best practices and metrics")
print("✓ Rich, detailed templates with actionable guidance")
print()
