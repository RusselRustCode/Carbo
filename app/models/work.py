import uuid
from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.models.enums import WorkStatus


class Work(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "works"

    task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    assignee_member_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("group_members.id", ondelete="RESTRICT"),
        nullable=True,
    )
    starts_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    deadline_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[WorkStatus] = mapped_column(String(32), nullable=False, default=WorkStatus.todo.value)

    task = relationship("Task", back_populates="works")
    assignee_member = relationship("GroupMember")
