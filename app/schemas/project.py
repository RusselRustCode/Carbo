from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = None
    deadline_at: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline_at: Optional[datetime] = None

class ProjectResponse(ProjectBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
