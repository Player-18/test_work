from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .user import UserRead


class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    chat_id: int
    sender_id: int
    timestamp: datetime = Field(default_factory=datetime.now)
    is_read: bool = False


class MessageRead(MessageBase):
    # id: int
    chat_id: int
    sender_id: int
    timestamp: datetime
    is_read: bool

    class Config:
        from_attributes = True