from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.work import WorkCreate, WorkResponse, WorkUpdate
from app.services.task_service import TaskService
from app.crud.task import task_crud
from app.crud.work import work_crud
from app.models.task import Task
from app.models.work import Work
from app.models.goal import Goal
from app.models.enums import TaskStatus
import tempfile
import os
from fastapi import UploadFile, File, BackgroundTasks
from app.services.s3_storage import s3_storage
from data_pipeline.integration import run_full_pipeline

router = APIRouter()
service = TaskService()


class TaskQueryParams:
    def __init__(
        self,
        my_tasks: bool = Query(False),
        member_id: str | None = None,
        overdue: bool = Query(False),
        due_this_week: bool = Query(False),
        unassigned: bool = Query(False),
        goal_id: str | None = None,
        project_id: str | None = None,
        status: str | None = None,
    ):
        self.my_tasks = my_tasks
        self.member_id = member_id
        self.overdue = overdue
        self.due_this_week = due_this_week
        self.unassigned = unassigned
        self.goal_id = goal_id
        self.project_id = project_id
        self.status = status


@router.post("/tasks", response_model=TaskResponse)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    task = await service.create_task(db, payload.model_dump())
    await db.refresh(task)
    return task


@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(params: TaskQueryParams = Depends(), skip: int = Query(0), limit: int = Query(50), db: AsyncSession = Depends(get_db)):
    q = select(Task).where(Task.deleted_at == None)

    if params.my_tasks:
        if not params.member_id:
            raise HTTPException(status_code=400, detail="member_id is required when my_tasks=true")
        q = q.where(Task.responsible_member_id == params.member_id)
    if params.status:
        q = q.where(Task.status == params.status)
    if params.goal_id:
        q = q.where(Task.goal_id == params.goal_id)
    if params.project_id:
        q = q.join(Goal, Task.goal).where(Goal.project_id == params.project_id)
    if params.overdue:
        q = q.where(Task.deadline_at < date.today(), Task.status.notin_([TaskStatus.done.value, TaskStatus.cancelled.value]))
    if params.due_this_week:
        today = date.today()
        week_end = today + timedelta(days=7)
        q = q.where(Task.deadline_at >= today, Task.deadline_at <= week_end)
    if params.unassigned:
        q = q.where(Task.responsible_member_id == None)

    q = q.offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get(db, task_id)
    if not task or task.is_deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.refresh(task)
    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, payload: TaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await service.update_task(db, task_id, payload.model_dump(exclude_none=True))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.refresh(task)
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: AsyncSession = Depends(get_db)):
    await task_crud.soft_delete(db, task_id)
    return {"ok": True}


@router.post("/tasks/{task_id}/works", response_model=WorkResponse)
async def create_work(task_id: str, payload: WorkCreate, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get(db, task_id)
    if not task or task.is_deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    work = await service.create_work(db, task_id, payload.model_dump())
    return work


@router.get("/tasks/{task_id}/works", response_model=List[WorkResponse])
async def list_works(task_id: str, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get(db, task_id)
    if not task or task.is_deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    q = await db.execute(select(Work).where(Work.task_id == task_id, Work.deleted_at == None))
    return q.scalars().all()


@router.patch("/works/{work_id}", response_model=WorkResponse)
async def update_work(work_id: str, payload: WorkUpdate, db: AsyncSession = Depends(get_db)):
    work = await service.update_work(db, work_id, payload.model_dump(exclude_none=True))
    if not work:
        raise HTTPException(status_code=404, detail="Work not found")
    return work


@router.delete("/works/{work_id}")
async def delete_work(work_id: str, db: AsyncSession = Depends(get_db)):
    await work_crud.soft_delete(db, work_id)
    return {"ok": True}


@router.post("/tasks/{task_id}/artifacts")
async def upload_task_artifact(
    task_id: str,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Загружает CSV с результатами анализов и запускает ETL-пайплайн.
    Связывает данные с задачей через data_artifact_key.
    """
    task = await task_crud.get(db, task_id)
    if not task or task.is_deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Запускаем полный пайплайн (Bronze → Silver → Validation)
        # Для MVP делаем синхронно в запросе, 
        # для прода — вынести в BackgroundTasks или Celery
        result = run_full_pipeline(tmp_path, task_id=str(task.id))

        task.data_artifact_key = result["silver_key"]
        await db.flush()

        return {
            "task_id": result["task_id"],
            "bronze_key": result["bronze_key"],
            "silver_key": result["silver_key"],
            "message": "Data ingested and processed successfully",
        }
    finally:
        os.unlink(tmp_path)