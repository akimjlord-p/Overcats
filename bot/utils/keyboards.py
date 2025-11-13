from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

# Callback Data
class CharacterCallback(CallbackData, prefix="character"):
    action: str
    character_id: str

class ShopCallback(CallbackData, prefix="shop"):
    action: str
    item_id: str

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎭 Персонажи", callback_data="profile_characters"),
         InlineKeyboardButton(text="🏪 Магазин", callback_data="shop_main")],
        [InlineKeyboardButton(text="⚔️ Бой", callback_data="battle_quick"),
         InlineKeyboardButton(text="🏆 Кампания", callback_data="campaign_list")]
    ])

def get_profile_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎭 Мои персонажи", callback_data="profile_characters")],
        [InlineKeyboardButton(text="⚔️ Быстрый бой", callback_data="battle_quick")],
        [InlineKeyboardButton(text="🏆 Кампания", callback_data="campaign_list")]
    ])

def get_character_selection_keyboard(characters):
    keyboard = []
    for char_id, character in characters.items():
        keyboard.append([InlineKeyboardButton(
            text=f"{character.picture} {character.name}",
            callback_data=CharacterCallback(action="select", character_id=char_id).pack()
        )])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_character_gallery_keyboard(characters):
    keyboard = []
    for char_id, character in characters.items():
        keyboard.append([InlineKeyboardButton(
            text=f"{character.picture} {character.name}",
            callback_data=CharacterCallback(action="detail", character_id=char_id).pack()
        )])
    keyboard.append([InlineKeyboardButton(text="🏪 Магазин", callback_data="shop_characters")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_characters_keyboard(user_characters, current_character_id):
    keyboard = []
    for uc in user_characters:
        character_id = uc.character_id
        text = f"✅ {character_id}" if character_id == current_character_id else f"🔓 {character_id}"
        keyboard.append([InlineKeyboardButton(
            text=text,
            callback_data=CharacterCallback(action='switch', character_id=character_id).pack()
        )])
    keyboard.append([InlineKeyboardButton(text="🏪 Магазин", callback_data="shop_characters")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_shop_keyboard(items):
    keyboard = []
    for item in items:
        keyboard.append([InlineKeyboardButton(
            text=f"{item.name} - {item.price} STAC",
            callback_data=ShopCallback(action="buy", item_id=item.id).pack()
        )])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users"),
         InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="💰 Выдать STAC", callback_data="admin_add_stac"),
         InlineKeyboardButton(text="🎭 Выдать персонажа", callback_data="admin_add_character")]
    ])

def get_broadcast_confirmation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Отправить", callback_data="broadcast_confirm"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="broadcast_cancel")
    ]])