from typing import TypedDict, Optional, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

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

    company_name: Optional[str]
    company_type: Optional[CompanyType]
    company_summary: Optional[str]

    cv_edits: Optional[dict]
    tailored_cv: Optional[StructuredCV]

    mail_draft: Optional[str]

    status: StateStatus
    human_feedback: Optional[str]
    messages: Annotated[list[BaseMessage], add_messages]