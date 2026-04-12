from pydantic import BaseModel
from typing import Optional

class RoomMemberResponse(BaseModel):
    id: int
    username: str
    avatar: Optional[str]

    class Config:
        from_attributes = True