from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import (
    ActionItemCreate,
    ActionItemRead,
    BulkCompleteRequest,
    PaginatedActionItems,
)

router = APIRouter(prefix="/action-items", tags=["action_items"])


def success(data) -> dict:
    """Return success envelope."""
    return {"ok": True, "data": data, "error": None}


@router.get("/")
def list_items(
    completed: Optional[bool] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    base_query = select(ActionItem)

    # Apply filter if provided
    if completed is not None:
        base_query = base_query.where(ActionItem.completed == completed)

    # Get total count
    total = db.execute(select(func.count()).select_from(base_query.subquery())).scalar()

    # Get paginated results
    offset = (page - 1) * page_size
    rows = db.execute(base_query.offset(offset).limit(page_size)).scalars().all()

    result = PaginatedActionItems(
        items=[ActionItemRead.model_validate(row) for row in rows],
        total=total or 0,
        page=page,
        page_size=page_size,
    )
    return success(result.model_dump())


@router.post("/", status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> dict:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return success(ActionItemRead.model_validate(item).model_dump())


@router.put("/{item_id}/complete")
def complete_item(item_id: int, db: Session = Depends(get_db)) -> dict:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return success(ActionItemRead.model_validate(item).model_dump())


@router.post("/bulk-complete")
def bulk_complete(payload: BulkCompleteRequest, db: Session = Depends(get_db)) -> dict:
    items = []
    for item_id in payload.ids:
        item = db.get(ActionItem, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"Action item {item_id} not found")
        item.completed = True
        db.add(item)
        items.append(item)

    db.flush()
    for item in items:
        db.refresh(item)

    return success([ActionItemRead.model_validate(item).model_dump() for item in items])
