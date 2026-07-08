from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.models.audit_log import AuditLog
from typing import List

router = APIRouter()

@router.get("/audit-log", response_model=List[dict])
async def get_audit_log(entity_type: str, entity_id: str, db: AsyncSession = Depends(get_db)):
    q = await db.execute(
        "SELECT entity_type, entity_id, actor_member_id, action, changed_fields, old_value, new_value, created_at FROM audit_log WHERE entity_type = :et AND entity_id = :eid ORDER BY created_at DESC",
        {"et": entity_type, "eid": entity_id},
    )
    rows = q.mappings().all()
    return [dict(r) for r in rows]
