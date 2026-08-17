from typing import NotRequired, TypedDict

from langchain_core.messages import AnyMessage

from src.models import StateStatus


class CVTailorHumanApprovalResult(TypedDict):
    status: StateStatus
    tailored_cv_feedback: NotRequired[str]
    messages: NotRequired[list[AnyMessage]]