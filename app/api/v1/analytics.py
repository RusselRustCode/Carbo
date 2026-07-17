from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.analytics import TaskAnalyticsResponse
from app.services.analytics_service import analytics_service

router = APIRouter()


@router.get("/tasks/{task_id}", response_model=TaskAnalyticsResponse)
async def get_task_analytics(
    task_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Программный JOIN: объединяет метаданные задачи из PostgreSQL
    с содержимым Parquet-файла из MinIO в единый JSON-ответ.
    """
    try:
        return await analytics_service.get_task_analytics(db, task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))