from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


# Response Envelope
class ErrorDetail(BaseModel):
    code: str
    message: str


class ApiResponse(BaseModel, Generic[T]):
    ok: bool
    data: T | None = None
    error: ErrorDetail | None = None


# Tag Schemas
class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")


class TagRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TagAttachRequest(BaseModel):
    tag_ids: list[int] = Field(min_length=1)


# Note Schemas
class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)


class TagBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    tags: list[TagBrief] = []


class PaginatedNotes(BaseModel):
    items: list[NoteRead]
    total: int
    page: int
    page_size: int


# Action Item Schemas
class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1)


class ActionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    completed: bool


class PaginatedActionItems(BaseModel):
    items: list[ActionItemRead]
    total: int
    page: int
    page_size: int


class BulkCompleteRequest(BaseModel):
    ids: list[int] = Field(min_length=1)


# Extraction Schemas
class ExtractionResult(BaseModel):
    hashtags: list[str]
    action_items: list[str]


class ExtractQuery(BaseModel):
    apply: bool = False
