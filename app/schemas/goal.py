from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    deadline_at: Optional[datetime] = None

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline_at: Optional[datetime] = None

class GoalResponse(GoalBase):
    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
