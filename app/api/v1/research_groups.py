from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.research_group import ResearchGroupCreate, ResearchGroupResponse, ResearchGroupUpdate
from app.crud.research_group import research_group_crud
from typing import List

router = APIRouter()

@router.post("/", response_model=ResearchGroupResponse)
async def create_group(payload: ResearchGroupCreate, db: AsyncSession = Depends(get_db)):
    obj = await research_group_crud.create(db, payload.model_dump())
    return {
        'id': obj.id,
        'name': obj.name,
        'description': obj.description,
        'owner_member_id': obj.owner_member_id,
        'status': obj.status,
        'created_at': obj.created_at,
        'updated_at': obj.updated_at,
        'deleted_at': obj.deleted_at,
        'members': [],
    }

@router.get("/", response_model=List[ResearchGroupResponse])
async def list_groups(skip: int = Query(0), limit: int = Query(50), db: AsyncSession = Depends(get_db)):
    objs = await research_group_crud.list(db, skip=skip, limit=limit)
    return objs

@router.get("/{group_id}", response_model=ResearchGroupResponse)
async def get_group(group_id: str, db: AsyncSession = Depends(get_db)):
    obj = await research_group_crud.get(db, group_id)
    if not obj or obj.is_deleted:
        raise HTTPException(status_code=404, detail="Group not found")
    return obj

@router.patch("/{group_id}", response_model=ResearchGroupResponse)
async def update_group(group_id: str, payload: ResearchGroupUpdate, db: AsyncSession = Depends(get_db)):
    obj = await research_group_crud.get(db, group_id)
    if not obj or obj.is_deleted:
        raise HTTPException(status_code=404, detail="Group not found")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(obj, k, v)
    await db.flush()
    return obj

@router.delete("/{group_id}")
async def delete_group(group_id: str, db: AsyncSession = Depends(get_db)):
    await research_group_crud.soft_delete(db, group_id)
    return {"ok": True}
