import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config
from bot.database.database import init_db
from bot.handlers.start import register_start_handlers
from bot.handlers.profile import register_profile_handlers
from bot.handlers.characters import register_character_handlers
from bot.handlers.shop import register_shop_handlers
from bot.handlers.admin import register_admin_handlers


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Инициализация БД
    await init_db()

    # Регистрация обработчиков
    register_start_handlers(dp)
    register_profile_handlers(dp)
    register_character_handlers(dp)
    register_shop_handlers(dp)
    register_admin_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())