from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 

router = APIRouter()

from app.api.deps import get_db 

from app.crud.employee import employee_crud 
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_employee(obj_in: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).where(Employee.email == obj_in.email))
    existing_employee = result.scalar_one_or_none()
    
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this email already exists."
        )
    
    return await employee_crud.create(db, obj_in=obj_in)