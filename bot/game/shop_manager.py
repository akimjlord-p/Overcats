from typing import List, Dict
from bot.game.models import ShopItem
from bot.game.character_manager import CharacterManager

class ShopManager:
    def __init__(self, character_manager: CharacterManager):
        self.character_manager = character_manager
        self.items = self._load_shop_items()
    
    def _load_shop_items(self) -> List[ShopItem]:
        """Автоматически создает товары на основе персонажей из YAML"""
        items = []
        purchasable_chars = self.character_manager.get_purchasable_characters()
        
        # Цены для персонажей
        character_prices = {
            'northpaw_veteran': 0,  # Бесплатный стартовый
            'bloodfang_berserker': 0,  # Бесплатный стартовый
            # Новые персонажи автоматически получат цену 100 STAC
        }
        
        for char_id, character in purchasable_chars.items():
            price = character_prices.get(char_id, 100)  # Цена по умолчанию 100
            if price > 0:  # Только платные персонажи в магазин
                items.append(ShopItem(
                    id=char_id,
                    name=character.name,
                    description=f"Новый персонаж: {character.name}",
                    price=price,
                    item_type="character",
                    data={"character_id": char_id}
                ))
        
        # Способности
        items.extend([
            ShopItem(
                id="combo_strike",
                name="Комбо Удар",
                description="Атака с растущим уроном",
                price=50,
                item_type="ability",
                data={"ability_id": "combo_strike"}
            ),
            ShopItem(
                id="life_steal", 
                name="Кража Жизни",
                description="Вампирическая атака",
                price=75,
                item_type="ability",
                data={"ability_id": "life_steal"}
            )
        ])
        
        return items
    
    def get_character_items(self) -> List[ShopItem]:
        """Возвращает только персонажей из магазина"""
        return [item for item in self.items if item.item_type == "character"]
    
    def get_ability_items(self) -> List[ShopItem]:
        """Возвращает только способности из магазина"""
        return [item for item in self.items if item.item_type == "ability"]