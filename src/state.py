from typing import TypedDict, Optional, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

from src.models import StateStatus
from src.models.structured_cv import StructuredCV
from src.models.structured_offer import StructuredOffer
from src.state_updates import CompanyResearchUpdate, FitAnalystUpdate, CVTailorUpdate, CVInterviewUpdate


class BaseState(TypedDict):
    offer: StructuredOffer
    cv: StructuredCV
    cv_file_path: Optional[str]
    analysis_feedback: Optional[str]
    tailored_cv_feedback: Optional[str]
    mail_draft: Optional[str]
    human_feedback: Optional[str]
    status: StateStatus
    messages: Annotated[list[BaseMessage], add_messages]


class State(CompanyResearchUpdate, FitAnalystUpdate, CVTailorUpdate, CVInterviewUpdate, BaseState):
    pass