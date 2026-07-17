from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin

class Employee(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "employees"

    __table_args__ = (
        Index("ix_employees_email", "email", unique=True),
    )

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
