from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .config import settings

#Строка подключения к бд
DATABASE_URL=f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

#Класс от которого будут наследоваться все модели 
class Base(DeclarativeBase):
    pass


#движок
engine=create_async_engine(
    DATABASE_URL,
    echo=True, #отклю в проде
    pool_size=20,#постоянные
    max_overflow=30,#временные соедения 
    pool_pre_ping=True,#проверка живое ли соединение
    pool_recycle=3600 #обновляю каждый час
)

#фабрика сессий
async_session_maker=async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session()->AsyncGenerator[AsyncSession, None]:
    """Генератор асинхронных сессий"""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
