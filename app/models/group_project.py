import uuid
from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.models.enums import AccessLevel


class GroupProject(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "group_projects"

    __table_args__ = (
        Index("ix_group_projects_group_id", "group_id"),
        Index("ix_group_projects_project_id", "project_id"),
    )

    group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("research_groups.id"), nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    access_level: Mapped[AccessLevel] = mapped_column(
        String(32),
        nullable=False,
        default=AccessLevel.read.value,
    )

    group = relationship("ResearchGroup", back_populates="group_projects")
    project = relationship("Project", back_populates="group_projects")
