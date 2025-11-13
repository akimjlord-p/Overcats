from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.database.database import get_db
from bot.database.models import User, UserCharacter
from bot.utils.keyboards import get_shop_keyboard, ShopCallback
from bot.game.shop_manager import ShopManager
from bot.game.character_manager import CharacterManager

router = Router()
character_manager = CharacterManager()
shop_manager = ShopManager(character_manager)


@router.message(Command("shop"))
async def shop_handler(message: Message):
    """Показывает магазин"""
    db = get_db()
    user = db.query(User).filter(User.telegram_id == message.from_user.id).first()

    if not user:
        await message.answer("Сначала используйте /start")
        return

    shop_text = (
        f"🏪 <b>Магазин Overcats</b>\n\n"
        f"💰 Ваш баланс: {user.stac} STAC\n\n"
        f"Доступные товары:\n"
    )

    character_items = shop_manager.get_character_items()
    ability_items = shop_manager.get_ability_items()

    for item in character_items:
        status = "✅ Куплено" if any(uc.character_id == item.id for uc in user.characters) else f"🌰 {item.price} STAC"
        shop_text += f"\n🎭 <b>{item.name}</b> - {status}"

    for item in ability_items:
        shop_text += f"\n⚡ <b>{item.name}</b> - 🌰 {item.price} STAC"

    await message.answer(
        shop_text,
        reply_markup=get_shop_keyboard(character_items + ability_items),
        parse_mode="HTML"
    )


@router.callback_query(ShopCallback.filter(F.action == "buy"))
async def shop_buy_handler(callback: CallbackQuery, callback_data: ShopCallback):
    """Обработчик покупки в магазине"""
    db = get_db()
    user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
    item_id = callback_data.item_id

    if not user:
        await callback.answer("Пользователь не найден")
        return

    # Находим товар
    item = next((i for i in shop_manager.items if i.id == item_id), None)
    if not item:
        await callback.answer("Товар не найден")
        return

    # Проверяем баланс
    if user.stac < item.price:
        await callback.answer(f"Недостаточно STAC! Нужно: {item.price}")
        return

    # Проверяем, есть ли уже товар
    if item.item_type == "character":
        existing = db.query(UserCharacter).filter(
            UserCharacter.user_id == user.id,
            UserCharacter.character_id == item_id
        ).first()
        if existing:
            await callback.answer("У вас уже есть этот персонаж!")
            return

    # Совершаем покупку
    user.stac -= item.price
    db.commit()

    # Выдаем товар
    if item.item_type == "character":
        new_character = UserCharacter(
            user_id=user.id,
            character_id=item_id
        )
        db.add(new_character)
        db.commit()

    await callback.answer(f"✅ Успешная покупка: {item.name}")
    await callback.message.answer(f"🎉 Вы купили: <b>{item.name}</b>\n"
                                  f"💰 Осталось STAC: {user.stac}")


def register_shop_handlers(dp):
    dp.include_router(router)