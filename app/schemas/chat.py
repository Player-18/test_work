from pydantic import BaseModel
from typing import List, Literal
from .user import UserRead


class ChatBase(BaseModel):
    name: str
    chat_type: Literal['private', 'group']


class ChatCreate(ChatBase):
    user_ids: List[int]  # Участники чата


class ChatRead(ChatBase):
    id: int
    participants: List[UserRead]

    class Config:
        from_attributes = True


class GroupCreate(BaseModel):
    name: str
    creator_id: int
    chat_id: int
    