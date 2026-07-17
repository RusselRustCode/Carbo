from fastapi import APIRouter
from . import employees, research_groups, group_members, tasks, audit_log
from . import projects, goals, group_projects
from . import analytics


router = APIRouter()
router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
router.include_router(employees.router, prefix="/employees", tags=["employees"])
router.include_router(research_groups.router, prefix="/research-groups", tags=["research-groups"])
router.include_router(group_members.router, prefix="", tags=["group-members"])
router.include_router(tasks.router, prefix="", tags=["tasks"])
router.include_router(projects.router, prefix="", tags=["projects"])
router.include_router(goals.router, prefix="", tags=["goals"])
router.include_router(group_projects.router, prefix="", tags=["group-projects"])
router.include_router(audit_log.router, prefix="", tags=["audit"])
