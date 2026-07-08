"""add projects, goals, group_projects

Revision ID: 0003_add_projects_goals_group_projects
Revises: 0002_add_groups_members_tasks
Create Date: 2026-07-08 00:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0003_add_projects_goals_group_projects'
down_revision = '0002_add_groups_members_tasks'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default=sa.text("'planning'")),
        sa.Column('deadline_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),
    )

    op.create_table(
        'goals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default=sa.text("'open'")),
        sa.Column('deadline_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),
    )
    op.create_foreign_key('fk_goals_project_id', 'goals', 'projects', ['project_id'], ['id'])
    op.create_index(op.f('ix_goals_project_id'), 'goals', ['project_id'], unique=False)

    op.create_table(
        'group_projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('group_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('access_level', sa.String(length=32), nullable=False, server_default=sa.text("'read'")),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),
    )
    op.create_foreign_key('fk_group_projects_group_id', 'group_projects', 'research_groups', ['group_id'], ['id'])
    op.create_foreign_key('fk_group_projects_project_id', 'group_projects', 'projects', ['project_id'], ['id'])
    op.create_index(op.f('ix_group_projects_group_id'), 'group_projects', ['group_id'], unique=False)
    op.create_index(op.f('ix_group_projects_project_id'), 'group_projects', ['project_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_group_projects_project_id'), table_name='group_projects')
    op.drop_index(op.f('ix_group_projects_group_id'), table_name='group_projects')
    op.drop_table('group_projects')
    op.drop_index(op.f('ix_goals_project_id'), table_name='goals')
    op.drop_table('goals')
    op.drop_table('projects')
