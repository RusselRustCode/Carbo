from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime
from app.schemas.group_member import GroupMemberResponse

class ResearchGroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class ResearchGroupCreate(ResearchGroupBase):
    pass

class ResearchGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ResearchGroupResponse(ResearchGroupBase):
    id: uuid.UUID
    owner_member_id: Optional[uuid.UUID] = None
    status: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    members: Optional[List[GroupMemberResponse]] = None

    model_config = {"from_attributes": True}
