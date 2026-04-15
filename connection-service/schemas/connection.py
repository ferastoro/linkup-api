from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class ConnectionCreate(BaseModel):
    receiver_id: int

class ConnectionUpdate(BaseModel):
    status: Literal["accepted", "rejected"]

class ConnectionResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True