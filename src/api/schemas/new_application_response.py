from pydantic import BaseModel

from src.api.schemas.payload import Payload
from src.api.schemas.allowed_actions import AllowedActions


class NewApplicationResponse(BaseModel):
    status: str
    id: str
    interrupted: bool
    allowed_actions: list[AllowedActions]
    payload: Payload