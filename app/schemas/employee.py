from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime

class EmployeeBase(BaseModel):
    full_name: str
    email: EmailStr

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class EmployeeRead(EmployeeBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
