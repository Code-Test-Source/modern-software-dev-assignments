from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    content: Optional[str] = ""


class NoteCreate(NoteBase):
    pass


class NotePatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemBase(BaseModel):
    description: str
    completed: Optional[bool] = False


class ActionItemCreate(ActionItemBase):
    pass


class ActionItemPatch(BaseModel):
    description: Optional[str] = None
    completed: Optional[bool] = None


class ActionItemRead(ActionItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
