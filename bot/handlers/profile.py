import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from aiogram import Dispatcher, types
from bot.database.database import get_db
from bot.database.models import User
from bot.utils.keyboards import get_profile_keyboard
from bot.game.character_manager import CharacterManager

character_manager = CharacterManager()

async def profile_handler(message: types.Message):
    """Показывает профиль пользователя"""
    db = get_db()
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
    
    if not user:
        await message.answer("Сначала используйте /start")
        return
    
    character = character_manager.get_all_characters().get(user.current_character_id)
    if not character:
        await message.answer("Ошибка: персонаж не найден")
        return
    
    profile_text = (
        f"🏅 <b>Профиль игрока</b>\n"
        f"👤 {message.from_user.full_name}\n"
        f"⭐ Рейтинг: {user.rating}\n"
        f"🌰 STAC: {user.stac}\n"
        f"🎭 Текущий персонаж: {character.name}\n"
        f"⚔️ Всего боев: {len(user.battles)}"
    )
    
    try:
        photo_path = f"media/characters/{user.current_character_id}.jpg"
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo:
                await message.answer_photo(
                    photo=photo,
                    caption=profile_text,
                    reply_markup=get_profile_keyboard()
                )
        else:
            await message.answer(
                profile_text,
                reply_markup=get_profile_keyboard()
            )
    except Exception as e:
        await message.answer(
            profile_text,
            reply_markup=get_profile_keyboard()
        )

def register_profile_handlers(dp: Dispatcher):
    dp.message.register(profile_handler, commands=["profile", "me"])