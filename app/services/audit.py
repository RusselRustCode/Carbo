from typing import Any, Dict, List
from app.models.audit_log import AuditLog
from app.models.enums import AuditAction
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime, date
from typing import Iterable


class AuditService:
    async def log_change(
        self,
        session: AsyncSession,
        entity_type: str,
        entity_id: str,
        actor_member_id: str | None,
        action: AuditAction,
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

        def _serialize(v):
            if v is None:
                return None
            if isinstance(v, uuid.UUID):
                return str(v)
            if isinstance(v, (datetime, date)):
                return v.isoformat()
            if isinstance(v, dict):
                return {kk: _serialize(vv) for kk, vv in v.items()}
            if isinstance(v, list) or isinstance(v, tuple) or isinstance(v, set):
                return [_serialize(x) for x in v]
            return v

        entry = AuditLog(
            entity_type=entity_type,
            entity_id=entity_id,
            actor_member_id=str(actor_member_id) if actor_member_id is not None else None,
            action=action,
            changed_fields=changed,
            old_value={k: _serialize(old.get(k)) for k in changed},
            new_value={k: _serialize(new.get(k)) for k in changed},
        )
        session.add(entry)
        await session.flush()
# single shared instance for the app
audit_service = AuditService()

