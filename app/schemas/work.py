from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import date, datetime


class WorkBase(BaseModel):
    title: str
    description: Optional[str] = None
    result: Optional[str] = None
    assignee_member_id: Optional[uuid.UUID] = None
    starts_at: Optional[date] = None
    deadline_at: Optional[date] = None
    status: Optional[str] = None


class WorkCreate(WorkBase):
    pass


class WorkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    result: Optional[str] = None
    assignee_member_id: Optional[uuid.UUID] = None
    starts_at: Optional[date] = None
    deadline_at: Optional[date] = None
    completed_at: Optional[datetime] = None
    status: Optional[str] = None


class WorkResponse(WorkBase):
    id: uuid.UUID
    task_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
