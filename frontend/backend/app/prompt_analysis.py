import spacy
from app.models import Analysis, Issue

nlp = spacy.load("en_core_web_sm")

def analyze_prompt(prompt: str):
    words = prompt.split()
    sentences = [s for s in prompt.split('.') if s]
    unique_words = set([w.lower() for w in words])

    clarity = 60 if len(sentences) > 1 else 40
    specificity = 50 if len(words) > 5 else 30
    structure = 55
    completeness = 50

    issues = []
    if specificity < 50:
        issues.append(Issue(
            type='specificity',
            severity='high',
            message='Prompt lacks specific details and constraints',
            details=f'Specificity score: {specificity}/100'
        ))
    if clarity < 50:
        issues.append(Issue(
            type='clarity',
            severity='medium',
            message='Prompt contains ambiguous language',
            details=f'Clarity score: {clarity}/100'
        ))

    suggestions = [
        "Include specific numbers, quantities, or measurements",
        "Provide examples of what you want",
        "Organize your prompt with bullet points",
        "Define the context or background",
        "Specify desired output format"
    ]

    analysis = Analysis(
        overall_score=int((clarity + specificity + structure + completeness)/4),
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

    optimized_prompt = f"Optimized version of your prompt: {prompt}"

    return analysis, optimized_prompt
