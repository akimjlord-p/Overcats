from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.database.database import get_db
from bot.database.models import User, UserCharacter
from bot.utils.keyboards import (
    get_characters_keyboard,
    get_character_gallery_keyboard,
    CharacterCallback
)
from bot.game.character_manager import CharacterManager

router = Router()
character_manager = CharacterManager()


@router.message(Command("characters", "gallery"))
async def characters_handler(message: Message):
    """Показывает галерею персонажей"""
    all_characters = character_manager.get_all_characters()

    gallery_text = "🎭 <b>Галерея персонажей</b>\n\n"
    gallery_text += "Доступные персонажи:\n"

    for char_id, character in all_characters.items():
        gallery_text += f"\n<b>{character.name}</b> {character.picture}\n"
        gallery_text += f"❤️ {character.max_health} HP | 🛡️ {character.base_armor * 100}% armor\n"

    await message.answer(
        gallery_text,
        reply_markup=get_character_gallery_keyboard(all_characters),
        parse_mode="HTML"
    )


@router.callback_query(CharacterCallback.filter(F.action == "detail"))
async def character_detail_handler(callback: CallbackQuery, callback_data: CharacterCallback):
    """Показывает детальную информацию о персонаже"""
    character_id = callback_data.character_id

    character_info = character_manager.get_character_info(character_id)

    try:
        await callback.message.answer_photo(
            photo=open(f"media/characters/{character_id}.jpg", 'rb'),
            caption=character_info,
            parse_mode="HTML"
        )
    except FileNotFoundError:
        await callback.message.answer(
            character_info,
            parse_mode="HTML"
        )

    await callback.answer()


@router.message(Command("mycharacters"))
async def my_characters_handler(message: Message):
    """Показывает персонажей пользователя"""
    db = get_db()
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()

    if not user:
        await message.answer("Сначала используйте /start")
        return

    user_characters = db.query(UserCharacter).filter(UserCharacter.user_id == user.id).all()

    if not user_characters:
        await message.answer("У вас нет персонажей")
        return

    characters_text = "🎭 <b>Ваши персонажи:</b>\n\n"

    for uc in user_characters:
        character = character_manager.get_all_characters()[uc.character_id]
        status = "✅ Текущий" if uc.character_id == user.current_character_id else "🔓 Доступен"
        characters_text += f"{status} - <b>{character.name}</b> {character.picture}\n"
        characters_text += f"   ❤️ {character.max_health} HP | 🛡️ {character.base_armor * 100}% armor\n\n"

    await message.answer(
        characters_text,
        reply_markup=get_characters_keyboard(user_characters, user.current_character_id),
        parse_mode="HTML"
    )


@router.callback_query(CharacterCallback.filter(F.action == "switch"))
async def switch_character_handler(callback: CallbackQuery, callback_data: CharacterCallback):
    """Меняет текущего персонажа"""
    db = get_db()
    user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
    character_id = callback_data.character_id

    if not user:
        await callback.answer("Пользователь не найден")
        return

    # Проверяем, есть ли у пользователя этот персонаж
    user_character = db.query(UserCharacter).filter(
        UserCharacter.user_id == user.id,
        UserCharacter.character_id == character_id
    ).first()

    if not user_character:
        await callback.answer("У вас нет этого персонажа!")
        return

    # Меняем персонажа
    user.current_character_id = character_id
    db.commit()

    character = character_manager.get_all_characters()[character_id]

    try:
        await callback.message.answer_photo(
            photo=open(f"media/characters/{character_id}.jpg", 'rb'),
            caption=f"✅ Теперь вы играете за: <b>{character.name}</b>",
            parse_mode="HTML"
        )
    except FileNotFoundError:
        await callback.message.answer(
            f"✅ Теперь вы играете за: <b>{character.name}</b>",
            parse_mode="HTML"
        )

    await callback.answer()


def register_character_handlers(dp):
    dp.include_router(router)