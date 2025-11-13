import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bot.game.character_manager import CharacterManager
from bot.game.user_manager import UserManager
from bot.keyboards.start_keyboards import get_start_keyboard, get_character_creation_keyboard
from bot.states.character_states import CharacterCreation

logger = logging.getLogger(__name__)


class StartStates(StatesGroup):
    main_menu = State()


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    try:
        user_manager = UserManager()
        character_manager = CharacterManager()

        # Регистрация или получение пользователя
        user = user_manager.get_user(message.from_user.id)
        if not user:
            user = user_manager.create_user(
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name
            )

        # Проверяем есть ли у пользователя персонаж
        character = character_manager.get_character(message.from_user.id)

        if character:
            # Персонаж есть - показываем главное меню
            await message.answer(
                f"Добро пожаловать назад, {character.name}!\n"
                f"Уровень: {character.level} | Опыт: {character.experience}\n"
                f"Здоровье: {character.health}/{character.max_health}",
                reply_markup=get_start_keyboard()
            )
            await state.set_state(StartStates.main_menu)
        else:
            # Персонажа нет - предлагаем создать
            await message.answer(
                "Добро пожаловать в Overcats!\n"
                "У вас еще нет персонажа. Давайте создадим его!",
                reply_markup=get_character_creation_keyboard()
            )
            await state.set_state(CharacterCreation.choose_archetype)

    except Exception as e:
        logger.error(f"Error in cmd_start: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    try:
        character_manager = CharacterManager()
        character = character_manager.get_character(callback.from_user.id)

        if character:
            await callback.message.edit_text(
                f"Главное меню - {character.name}\n"
                f"Уровень: {character.level} | Опыт: {character.experience}",
                reply_markup=get_start_keyboard()
            )
            await state.set_state(StartStates.main_menu)
        else:
            await callback.message.edit_text(
                "У вас нет персонажа. Давайте создадим его!",
                reply_markup=get_character_creation_keyboard()
            )
            await state.set_state(CharacterCreation.choose_archetype)

    except Exception as e:
        logger.error(f"Error in back_to_main_menu: {e}")
        await callback.message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")


def register_start_handlers(main_router: Router):
    """Регистрация обработчиков старта"""
    main_router.include_router(router)