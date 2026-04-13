from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=30)
    email: Optional[str]
    password: str
    description: Optional[str] = None
    avatar: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    description: Optional[str]
    avatar: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True