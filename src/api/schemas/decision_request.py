from pydantic import BaseModel, Field

from src.api.schemas import AllowedActions


class DecisionRequest(BaseModel):
    action: AllowedActions = Field(..., description="Action to perform")
    feedback: str = Field(description="Feedback to LLM about generated copy")