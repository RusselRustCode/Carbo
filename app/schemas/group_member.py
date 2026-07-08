from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class GroupMemberBase(BaseModel):
    employee_id: uuid.UUID
    role: Optional[str] = None
    status: Optional[str] = None

class GroupMemberCreate(GroupMemberBase):
    pass

class GroupMemberUpdate(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None
    left_at: Optional[datetime] = None

class GroupMemberResponse(GroupMemberBase):
    id: uuid.UUID
    group_id: uuid.UUID
    joined_at: datetime
    left_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
