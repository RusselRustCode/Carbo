"""sync models with database schema

Revision ID: 0005_sync_models
Revises: 09afc74454cc
Create Date: 2026-07-17 18:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0005_sync_models'
down_revision = '09afc74454cc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Создаём индексы только если они ещё не существуют
    conn = op.get_bind()
    
    indexes_to_create = [
        ("ix_audit_entity_created", "audit_log", ["entity_type", "entity_id", "created_at"]),
        ("ix_employees_email", "employees", ["email"]),
        ("ix_goals_project_id", "goals", ["project_id"]),
        ("ix_group_members_group_id", "group_members", ["group_id"]),
        ("ix_group_members_employee_id", "group_members", ["employee_id"]),
        ("ix_group_projects_group_id", "group_projects", ["group_id"]),
        ("ix_group_projects_project_id", "group_projects", ["project_id"]),
    ]
    
    for idx_name, table_name, columns in indexes_to_create:
        # Проверяем существование индекса в pg_indexes
        result = conn.execute(
            sa.text("SELECT 1 FROM pg_indexes WHERE indexname = :idx_name"),
            {"idx_name": idx_name}
        ).fetchone()
        
        if not result:
            unique = idx_name == "ix_employees_email"
            op.create_index(idx_name, table_name, columns, unique=unique)
            print(f"✅ Created index {idx_name}")
        else:
            print(f"⏭️  Index {idx_name} already exists, skipping")

    # Возвращаем TEXT для research_groups.description
    op.alter_column(
        'research_groups', 'description',
        existing_type=sa.String(),
        type_=sa.Text(),
        existing_nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        'research_groups', 'description',
        existing_type=sa.Text(),
        type_=sa.String(),
        existing_nullable=True
    )
    op.drop_index('ix_group_projects_project_id', table_name='group_projects')
    op.drop_index('ix_group_projects_group_id', table_name='group_projects')
    op.drop_index('ix_group_members_employee_id', table_name='group_members')
    op.drop_index('ix_group_members_group_id', table_name='group_members')
    op.drop_index('ix_goals_project_id', table_name='goals')
    op.drop_index('ix_employees_email', table_name='employees')
    op.drop_index('ix_audit_entity_created', table_name='audit_log')