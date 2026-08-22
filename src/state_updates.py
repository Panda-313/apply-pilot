from typing import Optional, Literal, TypedDict, Annotated, NotRequired

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

from src.models import CompanyType, FitRecommendation, StateStatus, Clarifications, TailoredCV

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

class CVInterviewUpdate(TypedDict):
    interview_messages: Annotated[list[BaseMessage], add_messages]
    clarifications: NotRequired[Optional[Clarifications]]
    status: StateStatus