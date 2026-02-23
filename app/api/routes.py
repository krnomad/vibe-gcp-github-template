from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.db.models import Item
from app.db.session import get_db_session
from app.schemas.item import ItemCreate, ItemRead

router = APIRouter()


@router.get("/")
async def read_root(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "service": settings.app_name,
        "environment": settings.app_env,
    }


@router.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/db/healthz")
async def db_healthcheck(session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database connection failed.") from exc

    return {
        "status": "ok",
        "database": "reachable",
    }


@router.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, session: AsyncSession = Depends(get_db_session)) -> ItemRead:
    item = Item(name=payload.name, description=payload.description)
    session.add(item)

    try:
        await session.commit()
        await session.refresh(item)
    except SQLAlchemyError as exc:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create item.") from exc

    return ItemRead.model_validate(item)


@router.get("/items/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, session: AsyncSession = Depends(get_db_session)) -> ItemRead:
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found.")

    return ItemRead.model_validate(item)
