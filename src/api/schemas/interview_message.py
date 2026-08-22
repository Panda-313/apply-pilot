from typing import Literal

from pydantic import BaseModel


class InterviewMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
