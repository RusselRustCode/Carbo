from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.employee import EmployeeCreate, EmployeeRead
from app.crud.employee import employee_crud

router = APIRouter()

@router.post("/", response_model=EmployeeRead)
async def create_employee(
    payload: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
):
    obj = await employee_crud.create(db, payload.model_dump())
    return obj
