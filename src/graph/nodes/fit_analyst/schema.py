from pydantic import BaseModel, Field

from src.models import FitRecommendation

class FitAnalystResult(BaseModel):
    fit_score: float = Field(description="Overall match score from 0 to 10 (10 = perfect match)")
    fit_gaps: list[str] = Field(description="List of important skills, technologies or experience required by the offer but missing or weak in the CV")
    fit_rationale: str = Field(description="Short explanation (2-4 sentences) why this score was given. Mention both strengths and main gaps.")
    fit_recommendation: FitRecommendation = Field(description="Final recommendation: 'apply' if good match, 'weak_fit' if borderline, 'skip' if clearly not worth applying")