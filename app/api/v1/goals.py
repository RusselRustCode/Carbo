from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db
from app.crud.goal import goal_crud
from app.crud.project import project_crud
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate

router = APIRouter()

@router.post("/projects/{project_id}/goals", response_model=GoalResponse)
async def create_goal(project_id: str, payload: GoalCreate, db: AsyncSession = Depends(get_db)):
    project = await project_crud.get(db, project_id)
    if not project or project.is_deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    data = payload.model_dump()
    data["project_id"] = project_id
    obj = await goal_crud.create(db, data)
    return obj

@router.get("/projects/{project_id}/goals", response_model=List[GoalResponse])
async def list_goals(project_id: str, skip: int = Query(0), limit: int = Query(50), db: AsyncSession = Depends(get_db)):
    project = await project_crud.get(db, project_id)
    if not project or project.is_deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    goals = await goal_crud.list_by_project(db, project_id, skip=skip, limit=limit)
    return goals

@router.get("/goals/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: str, db: AsyncSession = Depends(get_db)):
    obj = await goal_crud.get(db, goal_id)
    if not obj or obj.is_deleted:
        raise HTTPException(status_code=404, detail="Goal not found")
    return obj

@router.patch("/goals/{goal_id}", response_model=GoalResponse)
async def update_goal(goal_id: str, payload: GoalUpdate, db: AsyncSession = Depends(get_db)):
    obj = await goal_crud.get(db, goal_id)
    if not obj or obj.is_deleted:
        raise HTTPException(status_code=404, detail="Goal not found")
    updated = await goal_crud.update(db, obj, payload.model_dump(exclude_none=True))
    return updated

@router.delete("/goals/{goal_id}")
async def delete_goal(goal_id: str, db: AsyncSession = Depends(get_db)):
    await goal_crud.soft_delete(db, goal_id)
    return {"ok": True}
