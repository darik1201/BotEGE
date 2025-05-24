from alembic.config import Config
from alembic import command
def run_sync_migrations():
    """Запуск миграций синхронно"""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
async def run_migrations():
    """Асинхронная обертка для миграций"""
    run_sync_migrations()