from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemPatch, ActionItemRead, CountResponse

router = APIRouter(prefix="/action-items", tags=["action_items"])

# Valid sort fields for action items
VALID_SORT_FIELDS = {"id", "description", "completed", "created_at", "updated_at"}


def validate_item_id(item_id: int) -> int:
    """Validate item_id is positive (greater than zero)."""
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Action item ID must be a positive integer")
    return item_id


def validate_sort_field(sort: str) -> str:
    """Validate sort field; falls back to -created_at for unknown fields."""
    sort_field = sort.lstrip("-")
    if sort_field not in VALID_SORT_FIELDS:
        return "-created_at"
    return sort


@router.get("/", response_model=list[ActionItemRead])
def list_items(
    db: Session = Depends(get_db),
    completed: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=0, le=200),
    sort: str = Query("-created_at"),
) -> list[ActionItemRead]:
    sort = validate_sort_field(sort)
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    stmt = stmt.order_by(order_fn(getattr(ActionItem, sort_field)))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.get("/count", response_model=CountResponse)
def count_items(
    db: Session = Depends(get_db),
    completed: Optional[bool] = None,
) -> CountResponse:
    stmt = select(func.count(ActionItem.id))
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))
    count = db.execute(stmt).scalar() or 0
    return CountResponse(count=count)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    validate_item_id(item_id)
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/uncomplete", response_model=ActionItemRead)
def uncomplete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    validate_item_id(item_id)
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = False
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.get("/{item_id}", response_model=ActionItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    validate_item_id(item_id)
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return ActionItemRead.model_validate(item)


@router.patch("/{item_id}", response_model=ActionItemRead)
def patch_item(
    item_id: int, payload: ActionItemPatch, db: Session = Depends(get_db)
) -> ActionItemRead:
    validate_item_id(item_id)
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    if payload.description is not None:
        item.description = payload.description
    if payload.completed is not None:
        item.completed = payload.completed
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    validate_item_id(item_id)
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    db.delete(item)
    db.flush()
