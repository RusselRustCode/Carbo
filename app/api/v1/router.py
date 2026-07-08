from fastapi import APIRouter
from . import employees

router = APIRouter()
router.include_router(employees.router, prefix="/employees", tags=["employees"])
