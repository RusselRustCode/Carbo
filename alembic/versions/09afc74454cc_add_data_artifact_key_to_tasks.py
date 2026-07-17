"""add data_artifact_key to tasks

Revision ID: 09afc74454cc
Revises: 0003
Create Date: 2026-07-17 16:38:08.132896
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '09afc74454cc'
down_revision: Union[str, None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tasks', sa.Column('data_artifact_key', sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column('tasks', 'data_artifact_key')