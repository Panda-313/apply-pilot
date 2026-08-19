from pydantic import BaseModel

class NewApplicationResponse(BaseModel):
    status: str
    id: str