from datetime import datetime

from pydantic import BaseModel, field_validator


class CountResponse(BaseModel):
    count: int


class NoteCreate(BaseModel):
    title: str
    content: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        if len(v) > 200:
            raise ValueError("Title must be 200 characters or less")
        return v.strip()

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Content cannot be empty or whitespace only")
        if len(v) > 10000:
            raise ValueError("Content must be 10000 characters or less")
        return v.strip()


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: str | None = None
    content: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str | None) -> str | None:
        if v is not None:
            if not v.strip():
                raise ValueError("Title cannot be empty or whitespace only")
            if len(v) > 200:
                raise ValueError("Title must be 200 characters or less")
            return v.strip()
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str | None) -> str | None:
        if v is not None:
            if not v.strip():
                raise ValueError("Content cannot be empty or whitespace only")
            if len(v) > 10000:
                raise ValueError("Content must be 10000 characters or less")
            return v.strip()
        return v


# NoteUpdate is for PUT endpoint - requires both fields
NoteUpdate = NoteCreate


class ActionItemCreate(BaseModel):
    description: str

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Description cannot be empty or whitespace only")
        if len(v) > 1000:
            raise ValueError("Description must be 1000 characters or less")
        return v.strip()


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = None
    completed: bool | None = None

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        if v is not None:
            if not v.strip():
                raise ValueError("Description cannot be empty or whitespace only")
            if len(v) > 1000:
                raise ValueError("Description must be 1000 characters or less")
            return v.strip()
        return v
