from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note, Tag
from ..schemas import (
    NoteCreate,
    NoteRead,
    NoteUpdate,
    PaginatedNotes,
    TagAttachRequest,
    TagRead,
)
from ..services.extract import extract_all

router = APIRouter(prefix="/notes", tags=["notes"])


def success(data) -> dict:
    """Return success envelope."""
    return {"ok": True, "data": data, "error": None}


@router.get("/")
def list_notes(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    tag: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    base_query = select(Note)

    # Filter by tag if provided
    if tag:
        tag_obj = db.execute(select(Tag).where(Tag.name == tag)).scalar_one_or_none()
        if tag_obj:
            base_query = base_query.where(Note.tags.contains(tag_obj))
        else:
            # Tag doesn't exist, return empty
            return success(
                {
                    "items": [],
                    "total": 0,
                    "page": page,
                    "page_size": page_size,
                }
            )

    # Get total count
    total = db.execute(select(func.count()).select_from(base_query.subquery())).scalar()

    # Get paginated results
    offset = (page - 1) * page_size
    rows = db.execute(base_query.offset(offset).limit(page_size)).scalars().all()

    result = PaginatedNotes(
        items=[NoteRead.model_validate(row) for row in rows],
        total=total or 0,
        page=page,
        page_size=page_size,
    )
    return success(result.model_dump())


@router.post("/", status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> dict:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return success(NoteRead.model_validate(note).model_dump())


@router.get("/search/")
def search_notes(
    q: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    sort: Optional[str] = Query(default="created_desc", pattern="^(created_desc|title_asc)$"),
    tag: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    base_query = select(Note)

    # Filter by tag if provided
    if tag:
        tag_obj = db.execute(select(Tag).where(Tag.name == tag)).scalar_one_or_none()
        if tag_obj:
            base_query = base_query.where(Note.tags.contains(tag_obj))
        else:
            return success(
                {
                    "items": [],
                    "total": 0,
                    "page": page,
                    "page_size": page_size,
                }
            )

    if q:
        base_query = base_query.where((Note.title.contains(q)) | (Note.content.contains(q)))

    # Apply sorting
    if sort == "title_asc":
        base_query = base_query.order_by(asc(Note.title))
    else:  # created_desc (default)
        base_query = base_query.order_by(desc(Note.id))

    # Get total count
    total = db.execute(select(func.count()).select_from(base_query.subquery())).scalar()

    # Get paginated results
    offset = (page - 1) * page_size
    rows = db.execute(base_query.offset(offset).limit(page_size)).scalars().all()

    result = PaginatedNotes(
        items=[NoteRead.model_validate(row) for row in rows],
        total=total or 0,
        page=page,
        page_size=page_size,
    )
    return success(result.model_dump())


@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)) -> dict:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return success(NoteRead.model_validate(note).model_dump())


@router.put("/{note_id}")
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)) -> dict:
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
    return success(NoteRead.model_validate(note).model_dump())


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)) -> dict:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    return success({"id": note_id, "deleted": True})


@router.post("/{note_id}/extract")
def extract_from_note(
    note_id: int,
    apply: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict:
    """Extract hashtags and action items from a note.

    Args:
        note_id: The note ID
        apply: If True, persist extracted action items and tags to the database
    """
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    result = extract_all(note.content)

    created_items = []
    created_tags = []
    if apply:
        # Create action items from extracted items
        for item_text in result["action_items"]:
            action_item = ActionItem(description=item_text, completed=False)
            db.add(action_item)
            created_items.append(action_item)

        # Create or attach tags from hashtags
        for tag_name in result["hashtags"]:
            tag_obj = db.execute(select(Tag).where(Tag.name == tag_name)).scalar_one_or_none()
            if not tag_obj:
                tag_obj = Tag(name=tag_name)
                db.add(tag_obj)
                created_tags.append(tag_name)
            if tag_obj not in note.tags:
                note.tags.append(tag_obj)

        db.flush()
        for item in created_items:
            db.refresh(item)

    response = {
        "hashtags": result["hashtags"],
        "action_items": result["action_items"],
        "created_action_items": len(created_items) if apply else 0,
        "created_tags": created_tags,
    }
    return success(response)


@router.post("/{note_id}/tags")
def attach_tags(note_id: int, payload: TagAttachRequest, db: Session = Depends(get_db)) -> dict:
    """Attach tags to a note."""
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    attached = []
    for tag_id in payload.tag_ids:
        tag = db.get(Tag, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
        if tag not in note.tags:
            note.tags.append(tag)
            attached.append(TagRead.model_validate(tag).model_dump())

    db.flush()
    db.refresh(note)
    return success(
        {
            "note_id": note_id,
            "attached": attached,
            "tags": [TagRead.model_validate(t).model_dump() for t in note.tags],
        }
    )


@router.delete("/{note_id}/tags/{tag_id}")
def detach_tag(note_id: int, tag_id: int, db: Session = Depends(get_db)) -> dict:
    """Detach a tag from a note."""
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag in note.tags:
        note.tags.remove(tag)

    db.flush()
    return success(
        {
            "note_id": note_id,
            "detached_tag_id": tag_id,
            "tags": [TagRead.model_validate(t).model_dump() for t in note.tags],
        }
    )
