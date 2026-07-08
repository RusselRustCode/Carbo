from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.base import CRUDBase
from app.models.group_member import GroupMember

class CRUDGroupMember(CRUDBase[GroupMember]):
    async def members_by_group(self, db: AsyncSession, group_id) -> List[GroupMember]:
        q = await db.execute(select(self.model).where(self.model.group_id == group_id, self.model.deleted_at == None))
        return q.scalars().all()

    async def groups_by_employee(self, db: AsyncSession, employee_id) -> List[GroupMember]:
        q = await db.execute(select(self.model).where(self.model.employee_id == employee_id, self.model.deleted_at == None))
        return q.scalars().all()

group_member_crud = CRUDGroupMember(GroupMember)
