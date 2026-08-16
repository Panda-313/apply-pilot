from typing import NotRequired, TypedDict

from langchain_core.messages import AnyMessage

from src.models import StateStatus


class FitAnalystHumanApprovalResult(TypedDict):
    status: StateStatus
    analysis_feedback: NotRequired[str]
    messages: NotRequired[list[AnyMessage]]