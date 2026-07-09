from datetime import datetime
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task
from app.models.work import Work
from app.services.status_validator import validate_transition
from app.services.audit import audit_service
from app.crud.task import task_crud
from app.crud.work import work_crud
from app.models.enums import TaskStatus, WorkStatus, AuditAction




class TaskService:
    async def create_task(self, db: AsyncSession, data: Dict[str, Any]) -> Task:
        if data.get("status") == TaskStatus.done.value and not data.get("completed_at"):
            data["completed_at"] = datetime.now()
        task = await task_crud.create(db, data)
        await audit_service.log_change(
            db,
            "task",
            str(task.id),
            data.get("responsible_member_id"),
            AuditAction.created,
            {},
            data,
        )
        return task

    async def update_task(self, db: AsyncSession, task_id: str, data: Dict[str, Any]) -> Task:
        task = await task_crud.get(db, task_id)
        if not task or task.is_deleted:
            return None

        old = {
            "status": task.status,
            "deadline_at": task.deadline_at,
            "responsible_member_id": task.responsible_member_id,
            "completed_at": task.completed_at,
        }

        if "status" in data:
            validate_transition(TaskStatus(task.status), TaskStatus(data["status"]))
            if data["status"] == TaskStatus.done.value:
                data["completed_at"] = datetime.now()
            elif task.status == TaskStatus.done.value and data["status"] != TaskStatus.done.value:
                data["completed_at"] = None

        task = await task_crud.update(db, task, data)

        new_state = {
            "status": task.status,
            "deadline_at": task.deadline_at,
            "responsible_member_id": task.responsible_member_id,
            "completed_at": task.completed_at,
        }

        change_keys = [k for k in set(old.keys()) | set(new_state.keys()) if old.get(k) != new_state.get(k)]
        if len(change_keys) == 1:
            if change_keys[0] == "status":
                action = AuditAction.status_changed
            elif change_keys[0] == "deadline_at":
                action = AuditAction.deadline_changed
            elif change_keys[0] == "responsible_member_id":
                action = AuditAction.assignee_changed
            else:
                action = AuditAction.updated
        else:
            action = AuditAction.updated

        await audit_service.log_change(
            db,
            "task",
            str(task.id),
            None,
            action,
            old,
            new_state,
        )

        return task

    async def create_work(self, db: AsyncSession, task_id: str, data: Dict[str, Any]) -> Work:
        data["task_id"] = task_id
        if data.get("status") == WorkStatus.done.value and not data.get("completed_at"):
            data["completed_at"] = datetime.now()
        work = await work_crud.create(db, data)
        await audit_service.log_change(
            db,
            "work",
            str(work.id),
            data.get("assignee_member_id"),
            AuditAction.created,
            {},
            data,
        )
        return work

    async def update_work(self, db: AsyncSession, work_id: str, data: Dict[str, Any]) -> Work:
        work = await work_crud.get(db, work_id)
        if not work or work.is_deleted:
            return None

        old = {
            "status": work.status,
            "deadline_at": work.deadline_at,
            "assignee_member_id": work.assignee_member_id,
            "completed_at": work.completed_at,
        }

        if "status" in data:
            validate_transition(WorkStatus(work.status), WorkStatus(data["status"]))
            if data["status"] == WorkStatus.done.value:
                data["completed_at"] = datetime.now()
            elif work.status == WorkStatus.done.value and data["status"] != WorkStatus.done.value:
                data["completed_at"] = None

        work = await work_crud.update(db, work, data)

        new_state = {
            "status": work.status,
            "deadline_at": work.deadline_at,
            "assignee_member_id": work.assignee_member_id,
            "completed_at": work.completed_at,
        }

        change_keys = [k for k in set(old.keys()) | set(new_state.keys()) if old.get(k) != new_state.get(k)]
        if len(change_keys) == 1:
            if change_keys[0] == "status":
                action = AuditAction.status_changed
            elif change_keys[0] == "deadline_at":
                action = AuditAction.deadline_changed
            elif change_keys[0] == "assignee_member_id":
                action = AuditAction.assignee_changed
            else:
                action = AuditAction.updated
        else:
            action = AuditAction.updated

        await audit_service.log_change(
            db,
            "work",
            str(work.id),
            None,
            action,
            old,
            new_state,
        )

        return work
