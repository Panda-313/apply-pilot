from typing import TypedDict, Optional, Annotated
from typing import Literal

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

from src.models import TailoredCV
from src.models import FitRecommendation, CompanyType, StateStatus
from src.models.structured_cv import StructuredCV
from src.models.structured_offer import StructuredOffer

class State(TypedDict):
    offer: StructuredOffer
    cv: StructuredCV

    fit_score: Optional[float]
    fit_gaps: list[str]
    fit_rationale: Optional[str]
    fit_recommendation: Optional[FitRecommendation]

    analysis_feedback: Optional[str]
    fit_analysis_cv_source: Optional[Literal["cv", "tailored_cv"]]

    company_name: Optional[str]
    company_type: Optional[CompanyType]
    company_summary: Optional[str]

    cv_edits: Optional[str]
    tailored_cv: Optional[TailoredCV]

    tailored_cv_feedback: Optional[str]

    mail_draft: Optional[str]

    status: StateStatus
    human_feedback: Optional[str]
    messages: Annotated[list[BaseMessage], add_messages]