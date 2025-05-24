from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio
import sys
import os
sys.path.append(os.getcwd())
from src.models.models import Base
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        future=True
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
def do_run_migrations(connection):
    """Actual migration runner."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()
if context.is_offline_mode():
    run_migrations_offline()
else:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        loop.create_task(run_migrations_online())
    else:
        asyncio.run(run_migrations_online())