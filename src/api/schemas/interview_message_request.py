from pydantic import BaseModel, Field


class InterviewMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message in the interview chat")
