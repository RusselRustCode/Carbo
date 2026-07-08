from typing import Generic, TypeVar, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id) -> Optional[ModelType]:
        return await db.get(self.model, id)

    async def create(self, db: AsyncSession, obj_in) -> ModelType:
        obj = self.model(**obj_in)
        db.add(obj)
        await db.flush()
        return obj
