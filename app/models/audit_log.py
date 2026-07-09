import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, JSON, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin
from app.models.enums import AuditAction

class AuditLog(Base, UUIDMixin):
    __tablename__ = "audit_log"

    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    actor_member_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    action: Mapped[AuditAction] = mapped_column(Enum(AuditAction, native_enum=False), nullable=False)
    changed_fields: Mapped[list | None] = mapped_column(JSON, nullable=True)
    old_value: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    new_value: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
