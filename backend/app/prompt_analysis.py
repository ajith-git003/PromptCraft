import spacy
from app.models import Analysis, Issue

# Load NLP model (for basic text checks)
nlp = spacy.load("en_core_web_sm")

def analyze_prompt(prompt: str):
    # Split into words and sentences
    words = prompt.split()
    sentences = [s.strip() for s in prompt.split('.') if s.strip()]
    unique_words = set([w.lower() for w in words])

    # Calculate basic scores
    clarity = 60 if len(sentences) > 1 else 40
    specificity = 50 if len(words) > 5 else 30
    structure = 55
    completeness = 50

    # Detect issues
    issues = []
    if specificity < 50:
        issues.append(Issue(
            type='specificity',
            severity='high',
            message='Prompt lacks specific details or examples.',
            details=f'Specificity score: {specificity}/100'
        ))
    if clarity < 50:
        issues.append(Issue(
            type='clarity',
            severity='medium',
            message='Prompt may be unclear or ambiguous.',
            details=f'Clarity score: {clarity}/100'
        ))

    # Suggestions
    suggestions = [
        "Add more specific details or examples.",
        "Use shorter, clearer sentences.",
        "Structure the prompt logically.",
        "Specify the desired format or tone of the response."
    ]

    # Build analysis object
    analysis = Analysis(
        overall_score=int((clarity + specificity + structure + completeness) / 4),
        clarity_score=clarity,
        specificity_score=specificity,
        structure_score=structure,
        completeness_score=completeness,
        issues=issues,
        suggestions=suggestions,
        metrics={
            "word_count": len(words),
            "sentence_count": len(sentences),
            "unique_words": len(unique_words)
        }
    )

    # Optimized prompt (simple enhancement)
    optimized_prompt = f"Optimized: {prompt.strip()} (more clear and structured)"

    return analysis, optimized_prompt
