from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from app.crud.base import CRUDBase
from app.models.work import Work


class CRUDWork(CRUDBase[Work]):
    async def list_by_task(self, db: AsyncSession, task_id, skip: int = 0, limit: int = 100) -> List[Work]:
        q = await db.execute(
            select(self.model).where(self.model.task_id == task_id, self.model.deleted_at == None).offset(skip).limit(limit)
        )
        return q.scalars().all()

    async def soft_delete(self, db: AsyncSession, id) -> None:
        await db.execute(update(self.model).where(self.model.id == id).values(deleted_at=func.now()))
        await db.flush()

    async def update(self, db: AsyncSession, db_obj: Work, obj_in: Dict[str, Any]) -> Work:
        for k, v in obj_in.items():
            setattr(db_obj, k, v)
        await db.flush()
        return db_obj


work_crud = CRUDWork(Work)
