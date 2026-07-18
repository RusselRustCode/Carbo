from typing import Generic, TypeVar, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id) -> Optional[ModelType]:
        return await db.get(self.model, id)

    async def create(self, db: AsyncSession, obj_in) -> ModelType:
        if hasattr(obj_in, "model_dump"):
            obj_in_data = obj_in.model_dump()  
        elif hasattr(obj_in, "dict"):
            obj_in_data = obj_in.dict()        
        else:
            obj_in_data = obj_in               

        obj = self.model(**obj_in_data)
        db.add(obj)
        await db.flush()
        await db.refresh(obj)   
        return obj