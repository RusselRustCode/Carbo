from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from app.crud.base import CRUDBase
from app.models.goal import Goal
from app.services.audit import audit_service

class CRUDGoal(CRUDBase[Goal]):
    async def list_by_project(self, db: AsyncSession, project_id, skip: int = 0, limit: int = 100) -> List[Goal]:
        q = await db.execute(
            select(self.model).where(self.model.project_id == project_id, self.model.deleted_at == None).offset(skip).limit(limit)
        )
        return q.scalars().all()

    async def soft_delete(self, db: AsyncSession, id) -> None:
        await db.execute(update(self.model).where(self.model.id == id).values(deleted_at=func.now()))

    async def update(self, db: AsyncSession, db_obj: Goal, obj_in: Dict[str, Any]) -> Goal:
        old = {"status": db_obj.status, "deadline_at": getattr(db_obj, "deadline_at", None)}
        for k, v in obj_in.items():
            setattr(db_obj, k, v)

        await db.flush()

        new = {"status": db_obj.status, "deadline_at": getattr(db_obj, "deadline_at", None)}
        if old.get("status") != new.get("status"):
            await audit_service.log_change(db, "goal", str(db_obj.id), None, "status_changed", {"status": old.get("status")}, {"status": new.get("status")})
        if old.get("deadline_at") != new.get("deadline_at"):
            await audit_service.log_change(db, "goal", str(db_obj.id), None, "deadline_changed", {"deadline_at": old.get("deadline_at")}, {"deadline_at": new.get("deadline_at")})

        return db_obj

goal_crud = CRUDGoal(Goal)
