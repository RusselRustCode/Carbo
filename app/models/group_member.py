from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.models.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.models.enums import MemberRole, MemberStatus

class GroupMember(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "group_members"

    group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("research_groups.id"), nullable=False)
    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    role: Mapped[MemberRole] = mapped_column(String(32), nullable=False, default=MemberRole.researcher.value)
    status: Mapped[MemberStatus] = mapped_column(String(32), nullable=False, default=MemberStatus.active.value)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # relationships
    group = relationship(
        "ResearchGroup",
        back_populates="members",
        foreign_keys=[group_id],
    )
    employee = relationship("Employee")
