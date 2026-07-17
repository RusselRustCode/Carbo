import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.task import task_crud
from app.services.s3_storage import s3_storage
from app.schemas.analytics import TaskAnalyticsResponse, TaskAnalyticsData


class AnalyticsService:
    async def get_task_analytics(
        self, db: AsyncSession, task_id: str
    ) -> TaskAnalyticsResponse:
        task = await task_crud.get(db, task_id)
        if not task or task.is_deleted:
            raise ValueError(f"Task {task_id} not found")

        response = TaskAnalyticsResponse(
            task_id=task.id,
            title=task.title,
            status=task.status,
            priority=task.priority,
            deadline_at=task.deadline_at.isoformat() if task.deadline_at else None,
            responsible_member_id=task.responsible_member_id,
            data_artifact_key=task.data_artifact_key,
        )

        if not task.data_artifact_key:
            response.analytics_error = "No data artifact linked to this task"
            return response

        try:
            buffer = await s3_storage.download_to_buffer(task.data_artifact_key)
            df = pd.read_parquet(buffer)

            # Конвертируем в JSON-совместимый формат
            # replace(na=None) превращает NaN в null для JSON
            import json
            rows = json.loads(df.where(pd.notnull(df), None).to_json(orient="records", date_format="iso"))

            response.analytics = TaskAnalyticsData(
                columns=list(df.columns),
                rows=rows,
                row_count=len(df),
                silver_key=task.data_artifact_key,
            )
        except Exception as e:
            response.analytics_error = f"Failed to read analytics data: {str(e)}"

        return response


analytics_service = AnalyticsService()