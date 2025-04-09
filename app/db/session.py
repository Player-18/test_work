from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.get_database_url(),
    echo=True,  # Логирование SQL запросов (отключить в production)
    future=True
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# async def get_db() -> AsyncSession:
#     """Генератор сессий для Dependency Injection"""
#     async with async_session() as session:
#         yield session