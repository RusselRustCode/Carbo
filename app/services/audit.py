from typing import Any

class AuditService:
    async def log(self, action: str, actor: str, details: Any | None = None) -> None:
        # placeholder for writing to audit_log table or external system
        pass
