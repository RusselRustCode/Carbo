import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.models.enums import ProjectStatus


class Project(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        String(32),
        nullable=False,
        default=ProjectStatus.planning.value,
    )
    deadline_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    goals = relationship("Goal", back_populates="project", cascade="all, delete-orphan")
    group_projects = relationship("GroupProject", back_populates="project", cascade="all, delete-orphan")
