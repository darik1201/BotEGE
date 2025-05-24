from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///ege_bot.db")
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
async def init_db():
    """Инициализация базы данных через миграции"""
    from src.migration.migration import run_migrations
    await run_migrations()
async def get_session():
    """Получение сессии базы данных"""
    async with async_session() as session:
        yield session