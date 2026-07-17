import uuid
from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.models.enums import TaskStatus, TaskPriority


class Task(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tasks"

    goal_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("goals.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsible_member_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("group_members.id", ondelete="RESTRICT"),
        nullable=True,
    )
    deadline_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[TaskPriority] = mapped_column(String(32), nullable=False, default=TaskPriority.normal.value)
    status: Mapped[TaskStatus] = mapped_column(String(32), nullable=False, default=TaskStatus.todo.value)

    goal = relationship("Goal", back_populates="tasks")
    responsible_member = relationship("GroupMember")
    works = relationship("Work", back_populates="task", cascade="all, delete-orphan")

    data_artifact_key: Mapped[str | None] = mapped_column(
        String(500), nullable=True, default=None
    )
