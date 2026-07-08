from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas import employee
from app.models.task import Task
from app.schemas.research_group import ResearchGroupResponse
from app.crud.task import task_crud
from app.schemas.research_group import ResearchGroupCreate
from app.schemas.research_group import ResearchGroupResponse
from typing import List
from app.schemas import research_group
from app.schemas import group_member
from app.schemas.group_member import GroupMemberResponse
from app.schemas.group_member import GroupMemberCreate
from app.schemas.group_member import GroupMemberUpdate
from app.schemas.research_group import ResearchGroupCreate
from app.schemas.research_group import ResearchGroupResponse
from app.schemas.group_member import GroupMemberResponse
from pydantic import BaseModel
import uuid

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str | None = None
    deadline_at: str | None = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    status: str
    deadline_at: str | None

    model_config = {"from_attributes": True}


@router.post("/tasks", response_model=TaskResponse)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    data = payload.model_dump()
    obj = await task_crud.create(db, data)
    return obj

@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(skip: int = Query(0), limit: int = Query(50), db: AsyncSession = Depends(get_db)):
    q = await db.execute("SELECT * FROM tasks WHERE deleted_at IS NULL OFFSET :skip LIMIT :limit", {"skip": skip, "limit": limit})
    rows = q.fetchall()
    return [dict(r) for r in q]

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: AsyncSession = Depends(get_db)):
    obj = await task_crud.get(db, task_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return obj

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    obj = await task_crud.get(db, task_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = await task_crud.update(db, obj, payload.model_dump(exclude_none=True))
    return updated

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: AsyncSession = Depends(get_db)):
    await task_crud.soft_delete(db, task_id)
    return {"ok": True}
