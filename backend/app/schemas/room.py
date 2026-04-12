from pydantic import BaseModel, Field
from typing import Optional, List

class RoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    video_url: str
    password: str
    owner_id: int

class RoomResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    video_url: str
    current_time: float
    is_playing: bool
    owner_id: int

    class Config:
        from_attributes = True