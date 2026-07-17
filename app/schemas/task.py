from pydantic import BaseModel, computed_field
from typing import Optional
import uuid
from datetime import datetime, date
from app.models.enums import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    goal_id: Optional[uuid.UUID] = None
    responsible_member_id: Optional[uuid.UUID] = None
    deadline_at: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    goal_id: Optional[uuid.UUID] = None
    responsible_member_id: Optional[uuid.UUID] = None
    deadline_at: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(TaskBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    data_artifact_key: Optional[str] = None

    @computed_field
    @property
    def is_overdue(self) -> bool:
        if self.status in {TaskStatus.done.value, TaskStatus.cancelled.value}:
            return False
        if self.deadline_at is None:
            return False
        deadline = self.deadline_at
        if isinstance(deadline, datetime):
            deadline = deadline.date()
        return deadline < date.today()

    model_config = {"from_attributes": True}
