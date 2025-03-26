import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db.models import Base
from src.config import config


logger = logging.getLogger(__name__)


engine = create_async_engine(
    config.db.url,
    echo=False,
    future=True,
)


async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    return async_session()


async def init_db():
    """
    Инициализирует соединение с БД и создает таблицы если они не существуют.
    Также создает начальные данные тарифов, если их нет.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("База данных инициализирована")
    except Exception as e:
        logger.error(f"Ошибка при инициализации БД: {e}")
        raise


async def close_db():
    """
    Закрывает соединение с БД.
    """
    await engine.dispose()
    logger.info("Соединение с БД закрыто")