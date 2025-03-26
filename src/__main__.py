import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.config import config
from src.db.database import init_db, close_db
from src.handlers.admin import admin_router
from src.handlers.user import user_router

def register_handlers(dp: Dispatcher):
    dp.include_routers(
        admin_router,
        user_router
    )

async def main():
    logger = logging.getLogger(__name__)
    
    bot = Bot(token=config.telegram.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    await init_db()
    
    register_handlers(dp)
    
    logger.info("Бот запущен")
    await dp.start_polling(bot, close_bot_session=True)
    
    await close_db()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")