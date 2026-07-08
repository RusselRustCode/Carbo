from typing import Any, Dict, List
import json
from app.models.audit_log import AuditLog
from sqlalchemy.ext.asyncio import AsyncSession


class AuditService:
    async def log_change(
        self,
        session: AsyncSession,
        entity_type: str,
        entity_id: str,
        actor_member_id: str | None,
        action: str,
        old_value: Dict[str, Any] | None,
        new_value: Dict[str, Any] | None,
    ) -> None:
        """Compare old and new dicts and insert an AuditLog entry for changed fields."""
        old = old_value or {}
        new = new_value or {}
        changed: List[str] = []
        for k in set(old.keys()) | set(new.keys()):
            if old.get(k) != new.get(k):
                changed.append(k)

        if not changed:
            return

        entry = AuditLog(
            entity_type=entity_type,
            entity_id=str(entity_id),
            actor_member_id=actor_member_id,
            action=action,
            changed_fields=json.dumps(changed),
            old_value=json.dumps({k: old.get(k) for k in changed}),
            new_value=json.dumps({k: new.get(k) for k in changed}),
            created_at=None,
        )
        session.add(entry)
        await session.flush()

