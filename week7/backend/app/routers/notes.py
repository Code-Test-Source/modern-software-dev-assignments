from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import CountResponse, NoteCreate, NotePatch, NoteRead, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

# Valid sort fields for notes
VALID_SORT_FIELDS = {"id", "title", "created_at", "updated_at"}


def validate_note_id(note_id: int) -> int:
    """Validate note_id is positive."""
    if note_id < 0:
        raise HTTPException(status_code=400, detail="Note ID must be a positive integer")
    return note_id


def validate_sort_field(sort: str) -> str:
    """Validate sort field is valid, return default if not."""
    sort_field = sort.lstrip("-")
    if sort_field not in VALID_SORT_FIELDS:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_field}")
    return sort


@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=0, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    sort = validate_sort_field(sort)
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    stmt = stmt.order_by(order_fn(getattr(Note, sort_field)))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/count", response_model=CountResponse)
def count_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
) -> CountResponse:
    stmt = select(func.count(Note.id))
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))
    count = db.execute(stmt).scalar() or 0
    return CountResponse(count=count)


@router.put("/{note_id}", response_model=NoteRead)
def put_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)) -> NoteRead:
    validate_note_id(note_id)
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = payload.title
    note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NotePatch, db: Session = Depends(get_db)) -> NoteRead:
    validate_note_id(note_id)
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    validate_note_id(note_id)
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> None:
    validate_note_id(note_id)
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()
