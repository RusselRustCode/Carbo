from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime


class TaskAnalyticsData(BaseModel):
    """Содержимое Parquet-файла из Silver слоя."""
    columns: List[str]
    rows: List[Dict[str, Any]]
    row_count: int
    silver_key: str


class TaskAnalyticsResponse(BaseModel):
    """Единый ответ, объединяющий метаданные задачи и данные из S3."""
    task_id: uuid.UUID
    title: str
    status: str
    priority: str
    deadline_at: Optional[str] = None
    responsible_member_id: Optional[uuid.UUID] = None
    data_artifact_key: Optional[str] = None
    
    analytics: Optional[TaskAnalyticsData] = None
    analytics_error: Optional[str] = None