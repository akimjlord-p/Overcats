import asyncio
import logging
import sys
import os

# Добавляем корневую директорию проекта в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import config
from bot.handlers.start import register_start_handlers
from bot.handlers.character import register_character_handlers
from bot.middlewares.user_middleware import UserMiddleware

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Основная функция запуска бота"""
    # Инициализация бота и диспетчера
    bot = Bot(token=config.bot_token.get_secret_value())
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация middleware
    dp.update.outer_middleware(UserMiddleware())

    # Регистрация роутеров
    register_start_handlers(dp)
    register_character_handlers(dp)

    # Запуск поллинга
    try:
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())