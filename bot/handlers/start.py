from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.database.database import get_db
from bot.database.models import User, UserCharacter
from bot.utils.keyboards import get_start_keyboard, get_character_selection_keyboard, CharacterCallback
from bot.game.character_manager import CharacterManager

router = Router()
character_manager = CharacterManager()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    db = get_db()

    # Проверяем, есть ли пользователь в БД
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()

    if not user:
        # Новый пользователь - показываем выбор персонажа
        await message.answer(
            "🐱 <b>Добро пожаловать в Overcats!</b>\n\n"
            "Выберите своего стартового персонажа:",
            reply_markup=get_character_selection_keyboard(character_manager.get_starting_characters())
        )
    else:
        # Существующий пользователь
        await message.answer(
            f"С возвращением, {message.from_user.full_name}!",
            reply_markup=get_start_keyboard()
        )


@router.callback_query(CharacterCallback.filter(F.action == "select"))
async def character_selection_handler(callback: CallbackQuery, callback_data: CharacterCallback, state: FSMContext):
    """Обработчик выбора стартового персонажа"""
    db = get_db()
    character_id = callback_data.character_id

    # Создаем пользователя
    user = User(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        current_character_id=character_id,
        stac=50
    )
    db.add(user)
    db.commit()

    # Добавляем персонажа пользователю
    user_character = UserCharacter(
        user_id=user.id,
        character_id=character_id
    )
    db.add(user_character)
    db.commit()

    character = character_manager.get_all_characters()[character_id]

    try:
        await callback.message.answer_photo(
            photo=open(f"media/characters/{character_id}.jpg", 'rb'),
            caption=f"✅ Отличный выбор! Теперь вы играете за: <b>{character.name}</b>\n\n"
                    f"Используйте /profile для управления персонажами",
            reply_markup=get_start_keyboard()
        )
    except FileNotFoundError:
        await callback.message.answer(
            f"✅ Отличный выбор! Теперь вы играете за: <b>{character.name}</b>\n\n"
            f"Используйте /profile для управления персонажами",
            reply_markup=get_start_keyboard()
        )

    await callback.answer()


def register_start_handlers(dp):
    dp.include_router(router)