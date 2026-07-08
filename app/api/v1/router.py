from fastapi import APIRouter
from . import employees, research_groups, group_members, tasks, audit_log

router = APIRouter()
router.include_router(employees.router, prefix="/employees", tags=["employees"]) 
router.include_router(research_groups.router, prefix="/research-groups", tags=["research-groups"]) 
router.include_router(group_members.router, prefix="", tags=["group-members"]) 
router.include_router(tasks.router, prefix="", tags=["tasks"]) 
router.include_router(audit_log.router, prefix="", tags=["audit"])
