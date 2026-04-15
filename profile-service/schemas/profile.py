from pydantic import BaseModel, Field
from typing import Optional

class ProfileCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=17, le=100)
    bio: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[str] = None

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=17, le=100)
    bio: Optional[str] = None
    location: Optional[str] = None
    interests: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    age: int
    bio: Optional[str]
    location: Optional[str]
    interests: Optional[str]

    class Config:
        from_attributes = True