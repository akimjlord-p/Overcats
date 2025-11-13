import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from datetime import datetime
from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from bot.database.database import get_db
from bot.database.models import User, UserCharacter
from bot.config import config
from bot.utils.keyboards import get_admin_keyboard, get_broadcast_confirmation_keyboard
from bot.game.character_manager import CharacterManager

# Состояния для FSM
class BroadcastStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirmation = State()

async def admin_handler(message: types.Message):
    """Панель администратора"""
    if message.from_user.id not in config.ADMIN_IDS:
        await message.answer("⛔ Доступ запрещен")
        return
    
    admin_text = (
        "🛠️ <b>Панель администратора</b>\n\n"
        "Доступные команды:\n"
        "👥 /admin_users - Статистика пользователей\n" 
        "💰 /admin_add_stac - Выдать STAC\n"
        "🎭 /admin_add_character - Выдать персонажа\n"
        "📢 /admin_broadcast - Рассылка сообщений\n"
        "🔄 /admin_reload - Перезагрузить конфиги"
    )
    await message.answer(admin_text, reply_markup=get_admin_keyboard())

async def admin_users_handler(message: types.Message):
    """Статистика пользователей"""
    if message.from_user.id not in config.ADMIN_IDS:
        return
    
    db = get_db()
    users = db.query(User).all()
    
    total_stac = sum(user.stac for user in users)
    active_today = len([u for u in users if u.created_at.date() == datetime.now().date()])
    
    stats_text = (
        f"👥 <b>Статистика пользователей</b>\n\n"
        f"📊 Всего пользователей: {len(users)}\n"
        f"💰 Общий STAC в системе: {total_stac}\n"
        f"🆕 Новых сегодня: {active_today}\n\n"
        f"📈 Последние 5 регистраций:\n"
    )
    
    for user in users[-5:]:
        created = user.created_at.strftime("%d.%m %H:%M")
        username = user.username or 'No name'
        stats_text += f"• {username} (ID: {user.telegram_id}) - {created}\n"
    
    await message.answer(stats_text)

async def admin_add_stac_handler(message: types.Message):
    """Выдать STAC пользователю"""
    if message.from_user.id not in config.ADMIN_IDS:
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 3:
            await message.answer("❌ Использование: /admin_add_stac USER_ID AMOUNT")
            return
            
        user_id = int(parts[1])
        amount = int(parts[2])
    except (ValueError, IndexError):
        await message.answer("❌ Использование: /admin_add_stac USER_ID AMOUNT")
        return
    
    db = get_db()
    user = db.query(User).filter(User.telegram_id == user_id).first()
    
    if not user:
        await message.answer("❌ Пользователь не найден")
        return
    
    user.stac += amount
    db.commit()
    
    await message.answer(f"✅ Пользователю {user_id} выдано {amount} STAC\n"
                        f"💰 Теперь у него: {user.stac} STAC")

async def admin_add_character_handler(message: types.Message):
    """Выдать персонажа пользователю"""
    if message.from_user.id not in config.ADMIN_IDS:
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 3:
            await message.answer("❌ Использование: /admin_add_character USER_ID CHARACTER_ID")
            return
            
        user_id = int(parts[1])
        character_id = parts[2]
    except (ValueError, IndexError):
        await message.answer("❌ Использование: /admin_add_character USER_ID CHARACTER_ID")
        return
    
    db = get_db()
    user = db.query(User).filter(User.telegram_id == user_id).first()
    
    if not user:
        await message.answer("❌ Пользователь не найден")
        return
    
    character_manager = CharacterManager()
    
    # Проверяем существование персонажа
    if character_id not in character_manager.get_all_characters():
        await message.answer(f"❌ Персонаж {character_id} не найден в конфигах")
        return
    
    # Проверяем, есть ли уже персонаж
    existing = db.query(UserCharacter).filter(
        UserCharacter.user_id == user.id,
        UserCharacter.character_id == character_id
    ).first()
    
    if existing:
        await message.answer("⚠️ У пользователя уже есть этот персонаж")
        return
    
    # Добавляем персонажа
    new_character = UserCharacter(
        user_id=user.id,
        character_id=character_id
    )
    db.add(new_character)
    db.commit()
    
    character = character_manager.get_all_characters()[character_id]
    await message.answer(f"✅ Пользователю {user_id} выдан персонаж: {character.name}")

async def admin_broadcast_handler(message: types.Message, state: FSMContext):
    """Начало рассылки"""
    if message.from_user.id not in config.ADMIN_IDS:
        return
    
    await message.answer(
        "📢 <b>Начало рассылки</b>\n\n"
        "Отправьте сообщение для рассылки всем пользователям.\n"
        "Можно использовать HTML разметку."
    )
    await state.set_state(BroadcastStates.waiting_for_message)

async def broadcast_message_handler(message: types.Message, state: FSMContext):
    """Обработчик сообщения для рассылки"""
    if message.from_user.id not in config.ADMIN_IDS:
        return
    
    await state.update_data(broadcast_message=message.html_text)
    
    db = get_db()
    users_count = db.query(User).count()
    
    preview_text = (
        f"📊 <b>Предпросмотр рассылки</b>\n\n"
        f"Получателей: {users_count} пользователей\n\n"
        f"<b>Сообщение:</b>\n{message.html_text}\n\n"
        f"Подтвердите отправку:"
    )
    
    await message.answer(
        preview_text,
        reply_markup=get_broadcast_confirmation_keyboard()
    )
    await state.set_state(BroadcastStates.waiting_for_confirmation)

async def broadcast_confirmation_handler(callback: types.CallbackQuery, state: FSMContext):
    """Подтверждение и отправка рассылки"""
    if callback.from_user.id not in config.ADMIN_IDS:
        return
    
    data = await state.get_data()
    broadcast_message = data.get('broadcast_message')
    
    if not broadcast_message:
        await callback.answer("❌ Сообщение не найдено")
        await state.clear()
        return
    
    db = get_db()
    users = db.query(User).all()
    
    bot = callback.bot
    successful = 0
    failed = 0
    
    # Отправляем сообщение о начале рассылки
    await callback.message.edit_text("🔄 Начинаю рассылку...")
    
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.telegram_id,
                text=broadcast_message
            )
            successful += 1
        except Exception as e:
            print(f"Ошибка отправки пользователю {user.telegram_id}: {e}")
            failed += 1
        
        # Небольшая задержка чтобы не спамить
        await asyncio.sleep(0.1)
    
    result_text = (
        f"✅ <b>Рассылка завершена</b>\n\n"
        f"📤 Успешно отправлено: {successful}\n"
        f"❌ Не удалось отправить: {failed}\n"
        f"📊 Всего пользователей: {len(users)}"
    )
    
    await callback.message.edit_text(result_text)
    await state.clear()
    await callback.answer()

async def broadcast_cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    """Отмена рассылки"""
    if callback.from_user.id not in config.ADMIN_IDS:
        return
    
    await callback.message.edit_text("❌ Рассылка отменена")
    await state.clear()
    await callback.answer()

async def admin_reload_handler(message: types.Message):
    """Перезагрузка конфигов"""
    if message.from_user.id not in config.ADMIN_IDS:
        return
    
    from bot.game.shop_manager import ShopManager
    
    try:
        # Пересоздаем менеджеры для перезагрузки конфигов
        character_manager = CharacterManager()
        shop_manager = ShopManager(character_manager)
        
        await message.answer(
            f"✅ Конфиги перезагружены\n"
            f"🎭 Персонажей: {len(character_manager.get_all_characters())}\n"
            f"🏪 Товаров: {len(shop_manager.items)}"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка перезагрузки: {e}")

def register_admin_handlers(dp: Dispatcher):
    dp.message.register(admin_handler, Command("admin"))
    dp.message.register(admin_users_handler, Command("admin_users"))
    dp.message.register(admin_add_stac_handler, Command("admin_add_stac"))
    dp.message.register(admin_add_character_handler, Command("admin_add_character"))
    dp.message.register(admin_broadcast_handler, Command("admin_broadcast"))
    dp.message.register(admin_reload_handler, Command("admin_reload"))
    
    # Обработчики FSM для рассылки
    dp.message.register(broadcast_message_handler, BroadcastStates.waiting_for_message)
    dp.callback_query.register(
        broadcast_confirmation_handler,
        F.data == "broadcast_confirm",
        BroadcastStates.waiting_for_confirmation
    )
    dp.callback_query.register(
        broadcast_cancel_handler,
        F.data == "broadcast_cancel",
        BroadcastStates.waiting_for_confirmation
    )