from aiogram.dispatcher.filters.state import State, StatesGroup

class ShopStates(StatesGroup):
    waiting_for_purchase_confirmation = State()

class BattleStates(StatesGroup):
    waiting_for_ability_selection = State()