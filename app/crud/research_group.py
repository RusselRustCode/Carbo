from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from app.crud.base import CRUDBase
from app.models.research_group import ResearchGroup
from sqlalchemy import func

class CRUDResearchGroup(CRUDBase[ResearchGroup]):
    async def list(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ResearchGroup]:
        q = await db.execute(
            select(self.model)
            .where(self.model.deleted_at == None)
            .options(selectinload(self.model.members))
            .offset(skip)
            .limit(limit)
        )
        return q.scalars().all()

    async def get(self, db: AsyncSession, id) -> ResearchGroup | None:
        return await db.get(self.model, id, options=[selectinload(self.model.members)])

    async def soft_delete(self, db: AsyncSession, id) -> None:
        await db.execute(update(self.model).where(self.model.id == id).values(deleted_at=func.now()))

research_group_crud = CRUDResearchGroup(ResearchGroup)
