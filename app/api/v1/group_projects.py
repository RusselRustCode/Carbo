from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db
from app.crud.group_project import group_project_crud
from app.crud.project import project_crud
from app.crud.research_group import research_group_crud
from app.schemas.group_project import GroupProjectCreate, GroupProjectResponse, GroupProjectUpdate

router = APIRouter()

@router.post("/projects/{project_id}/group-projects", response_model=GroupProjectResponse)
async def create_group_project(project_id: str, payload: GroupProjectCreate, db: AsyncSession = Depends(get_db)):
    project = await project_crud.get(db, project_id)
    if not project or project.is_deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    group = await research_group_crud.get(db, payload.group_id)
    if not group or group.is_deleted:
        raise HTTPException(status_code=404, detail="Research group not found")
    data = payload.model_dump()
    data["project_id"] = project_id
    obj = await group_project_crud.create(db, data)
    return obj

@router.get("/projects/{project_id}/group-projects", response_model=List[GroupProjectResponse])
async def list_group_projects(project_id: str, skip: int = Query(0), limit: int = Query(50), db: AsyncSession = Depends(get_db)):
    project = await project_crud.get(db, project_id)
    if not project or project.is_deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    items = await group_project_crud.list_by_project(db, project_id, skip=skip, limit=limit)
    return items

@router.get("/group-projects/{link_id}", response_model=GroupProjectResponse)
async def get_group_project(link_id: str, db: AsyncSession = Depends(get_db)):
    obj = await group_project_crud.get(db, link_id)
    if not obj or obj.is_deleted:
        raise HTTPException(status_code=404, detail="Group project not found")
    return obj

@router.patch("/group-projects/{link_id}", response_model=GroupProjectResponse)
async def update_group_project(link_id: str, payload: GroupProjectUpdate, db: AsyncSession = Depends(get_db)):
    obj = await group_project_crud.get(db, link_id)
    if not obj or obj.is_deleted:
        raise HTTPException(status_code=404, detail="Group project not found")
    updated = await group_project_crud.update(db, obj, payload.model_dump(exclude_none=True))
    await db.refresh(updated)
    return updated

@router.delete("/group-projects/{link_id}")
async def delete_group_project(link_id: str, db: AsyncSession = Depends(get_db)):
    await group_project_crud.soft_delete(db, link_id)
    return {"ok": True}
