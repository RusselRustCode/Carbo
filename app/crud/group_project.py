from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from app.crud.base import CRUDBase
from app.models.group_project import GroupProject
from app.services.audit import audit_service

class CRUDGroupProject(CRUDBase[GroupProject]):
    async def list_by_project(self, db: AsyncSession, project_id, skip: int = 0, limit: int = 100) -> List[GroupProject]:
        q = await db.execute(
            select(self.model).where(self.model.project_id == project_id, self.model.deleted_at == None).offset(skip).limit(limit)
        )
        return q.scalars().all()

    async def soft_delete(self, db: AsyncSession, id) -> None:
        await db.execute(update(self.model).where(self.model.id == id).values(deleted_at=func.now()))

    async def update(self, db: AsyncSession, db_obj: GroupProject, obj_in: Dict[str, Any]) -> GroupProject:
        old = {"access_level": db_obj.access_level}
        for k, v in obj_in.items():
            setattr(db_obj, k, v)

        await db.flush()

        new = {"access_level": db_obj.access_level}
        if old.get("access_level") != new.get("access_level"):
            await audit_service.log_change(
                db,
                "group_project",
                str(db_obj.id),
                None,
                "access_level_changed",
                {"access_level": old.get("access_level")},
                {"access_level": new.get("access_level")},
            )

        return db_obj

group_project_crud = CRUDGroupProject(GroupProject)
