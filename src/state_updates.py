from typing import Optional, Literal, TypedDict

from src.models import CompanyType, FitRecommendation, StateStatus
from src.models.structured_cv import TailoredCV


class CompanyResearchUpdate(TypedDict):
    company_name: Optional[str]
    company_type: Optional[CompanyType]
    company_summary: Optional[str]
    status: StateStatus


class FitAnalystUpdate(TypedDict):
    fit_score: Optional[float]
    fit_gaps: list[str]
    fit_rationale: Optional[str]
    fit_recommendation: Optional[FitRecommendation]
    fit_analysis_cv_source: Optional[Literal["cv", "tailored_cv"]]
    status: StateStatus


class CVTailorUpdate(TypedDict):
    cv_edits: Optional[str]
    tailored_cv: Optional[TailoredCV]
    status: StateStatus
