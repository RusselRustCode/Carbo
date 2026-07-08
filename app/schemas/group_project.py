from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class GroupProjectBase(BaseModel):
    group_id: uuid.UUID
    access_level: Optional[str] = None

class GroupProjectCreate(GroupProjectBase):
    pass

class GroupProjectUpdate(BaseModel):
    access_level: Optional[str] = None

class GroupProjectResponse(GroupProjectBase):
    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
