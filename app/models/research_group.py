from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin
from app.models.enums import GroupStatus

class ResearchGroup(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "research_groups"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    owner_member_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("group_members.id"),
        nullable=True,
    )
    status: Mapped[GroupStatus] = mapped_column(
        String(32),
        nullable=False,
        default=GroupStatus.active.value,
    )

    owner_member = relationship(
        "GroupMember",
        foreign_keys=[owner_member_id],
        post_update=True,
    )
    members = relationship(
        "GroupMember",
        back_populates="group",
        cascade="all, delete-orphan",
        foreign_keys="[GroupMember.group_id]",
    )
    group_projects = relationship("GroupProject", back_populates="group", cascade="all, delete-orphan")
