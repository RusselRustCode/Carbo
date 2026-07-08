from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.group_member import GroupMemberCreate, GroupMemberResponse, GroupMemberUpdate
from app.crud.group_member import group_member_crud
from app.crud.research_group import research_group_crud
from typing import List

router = APIRouter()

@router.post("/research-groups/{group_id}/members", response_model=GroupMemberResponse)
async def add_member(group_id: str, payload: GroupMemberCreate, db: AsyncSession = Depends(get_db)):
    # ensure group exists
    grp = await research_group_crud.get(db, group_id)
    if not grp or grp.is_deleted:
        raise HTTPException(status_code=404, detail="Group not found")
    data = payload.model_dump()
    data["group_id"] = group_id
    obj = await group_member_crud.create(db, data)
    return obj

@router.get("/research-groups/{group_id}/members", response_model=List[GroupMemberResponse])
async def list_members(group_id: str, db: AsyncSession = Depends(get_db)):
    members = await group_member_crud.members_by_group(db, group_id)
    return members

@router.patch("/group-members/{member_id}", response_model=GroupMemberResponse)
async def update_member(member_id: str, payload: GroupMemberUpdate, db: AsyncSession = Depends(get_db)):
    obj = await group_member_crud.get(db, member_id)
    if not obj or obj.is_deleted:
        raise HTTPException(status_code=404, detail="Member not found")
    for k, v in payload.model_dump(exclude_none=True).items():
        setattr(obj, k, v)
    await db.flush()
    return obj

@router.delete("/group-members/{member_id}")
async def remove_member(member_id: str, db: AsyncSession = Depends(get_db)):
    await group_member_crud.soft_delete(db, member_id)
    return {"ok": True}
