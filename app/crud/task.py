from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.crud.base import CRUDBase
from app.models.task import Task
from app.services.status_validator import validate_transition
from app.services.audit import AuditService
import json

audit_service = AuditService()


class CRUDTask(CRUDBase[Task]):
    async def update(self, db: AsyncSession, db_obj: Task, obj_in: Dict[str, Any]) -> Task:
        # capture old values
        old = {"status": db_obj.status, "deadline_at": getattr(db_obj, "deadline_at", None)}
        # validate status transition
        if "status" in obj_in:
            from app.models.enums import TaskStatus
            if not validate_transition(TaskStatus(db_obj.status), TaskStatus(obj_in["status"])):
                raise ValueError(f"Invalid status transition: {db_obj.status} -> {obj_in['status']}")

        for k, v in obj_in.items():
            setattr(db_obj, k, v)

        await db.flush()

        new = {"status": db_obj.status, "deadline_at": getattr(db_obj, "deadline_at", None)}
        # automatic audit on status or deadline change
        if old.get("status") != new.get("status"):
            await audit_service.log_change(db, "task", str(db_obj.id), None, "status_changed", {"status": old.get("status")}, {"status": new.get("status")})
        if old.get("deadline_at") != new.get("deadline_at"):
            await audit_service.log_change(db, "task", str(db_obj.id), None, "deadline_changed", {"deadline_at": old.get("deadline_at")}, {"deadline_at": new.get("deadline_at")})

        return db_obj


task_crud = CRUDTask(Task)
