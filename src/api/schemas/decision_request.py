from pydantic import BaseModel, Field

from src.api.schemas import AllowedActions


class DecisionRequest(BaseModel):
    action: AllowedActions = Field(..., description="Action to perform")
    feedback: str = Field(default="", description="Feedback to LLM about generated copy")