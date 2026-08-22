from pydantic import BaseModel, Field

from src.models import Clarifications

class InterviewTurn(BaseModel):
    is_complete: bool = Field(
        description="True only when style, rewrite_permission, key skill years, and all important gaps are resolved"
    )
    assistant_message: str = Field(
        description="Next question or a short closing summary"
    )
    clarifications: Clarifications | None = Field(
        description="Filled only when is_complete is true"
    )