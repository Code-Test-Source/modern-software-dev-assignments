from __future__ import annotations

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    content: str = Field(min_length=1)


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


class ActionItemResponse(BaseModel):
    id: int
    note_id: int | None
    text: str
    done: bool = False
    created_at: str | None = None


class ActionItemDoneUpdate(BaseModel):
    done: bool = True


class ExtractActionItemsRequest(BaseModel):
    text: str = Field(min_length=1)
    save_note: bool = False


class ExtractActionItemsResponse(BaseModel):
    note_id: int | None
    items: list[ActionItemResponse]
