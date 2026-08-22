from typing import Optional

from pydantic import BaseModel

from src.models import TailoredCV, CompanyType, FitRecommendation, StructuredOffer
from src.api.schemas.interview_message import InterviewMessage


class Payload(BaseModel):
    fit_score: Optional[float] = None
    fit_gaps: Optional[list[str]] = None
    fit_rationale: Optional[str] = None
    fit_recommendation: Optional[FitRecommendation] = None
    offer: Optional[StructuredOffer] = None
    cv_edits: Optional[str] = None
    tailored_cv: Optional[TailoredCV] = None
    tailored_cv_feedback: Optional[str] = None
    company_name: Optional[str] = None
    company_type: Optional[CompanyType] = None
    company_summary: Optional[str] = None
    interview_messages: Optional[list[InterviewMessage]] = None
