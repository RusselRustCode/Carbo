from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db
from app.crud.project import project_crud
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter()

@router.post("/projects", response_model=ProjectResponse)
async def create_project(payload: ProjectCreate, db: AsyncSession = Depends(get_db)):
    obj = await project_crud.create(db, payload.model_dump())
    return obj

@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(skip: int = Query(0), limit: int = Query(50), db: AsyncSession = Depends(get_db)):
    objs = await project_crud.list(db, skip=skip, limit=limit)
    return objs

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    obj = await project_crud.get(db, project_id)
    if not obj or obj.is_deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj

@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, payload: ProjectUpdate, db: AsyncSession = Depends(get_db)):
    obj = await project_crud.get(db, project_id)
    if not obj or obj.is_deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    updated = await project_crud.update(db, obj, payload.model_dump(exclude_none=True))
    return updated

@router.delete("/projects/{project_id}")
async def delete_project(project_id: str, db: AsyncSession = Depends(get_db)):
    await project_crud.soft_delete(db, project_id)
    return {"ok": True}
