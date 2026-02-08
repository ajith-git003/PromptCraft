from pydantic import BaseModel
from typing import List, Dict

class Issue(BaseModel):
    type: str
    severity: str
    message: str
    details: str

class Analysis(BaseModel):
    overall_score: int
    clarity_score: int
    specificity_score: int
    structure_score: int
    completeness_score: int
    issues: List[Issue]
    suggestions: List[str]
    metrics: Dict[str, int]

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    analysis: Analysis
    optimized_prompt: str
