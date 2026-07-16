from logging.config import fileConfig
import os
import asyncio
import importlib
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
import sys
from alembic import context
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

models_mod = importlib.import_module('app.models')
target_metadata = models_mod.Base.metadata

def run_migrations_offline() -> None:
    url = os.environ.get("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    connectable = create_async_engine(os.environ.get('DATABASE_URL'))
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
