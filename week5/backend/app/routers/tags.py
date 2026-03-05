from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Tag
from ..schemas import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["tags"])


def success(data) -> dict:
    """Return success envelope."""
    return {"ok": True, "data": data, "error": None}


@router.get("/")
def list_tags(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    # Get total count
    total = db.execute(select(func.count()).select_from(Tag)).scalar()

    # Get paginated results
    offset = (page - 1) * page_size
    rows = db.execute(select(Tag).offset(offset).limit(page_size)).scalars().all()

    return success(
        {
            "items": [TagRead.model_validate(row).model_dump() for row in rows],
            "total": total or 0,
            "page": page,
            "page_size": page_size,
        }
    )


@router.post("/", status_code=201)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)) -> dict:
    # Check if tag already exists
    existing = db.execute(select(Tag).where(Tag.name == payload.name)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")

    tag = Tag(name=payload.name)
    db.add(tag)
    db.flush()
    db.refresh(tag)
    return success(TagRead.model_validate(tag).model_dump())


@router.get("/{tag_id}")
def get_tag(tag_id: int, db: Session = Depends(get_db)) -> dict:
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return success(TagRead.model_validate(tag).model_dump())


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)) -> dict:
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    return success({"id": tag_id, "deleted": True})
