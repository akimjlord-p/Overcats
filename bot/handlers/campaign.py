import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Dispatcher, types

async def campaign_handler(message: types.Message):
    """Обработчик кампании"""
    await message.answer("🏆 Система кампании в разработке...")

def register_campaign_handlers(dp: Dispatcher):
    dp.message.register(campaign_handler, commands=["campaign"])