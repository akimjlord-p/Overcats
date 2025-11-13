import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Dispatcher, types

async def battle_handler(message: types.Message):
    """Обработчик боевой системы"""
    await message.answer("⚔️ Система боев в разработке...")

def register_pvp_handlers(dp: Dispatcher):
    dp.message.register(battle_handler, commands=["battle", "fight"])