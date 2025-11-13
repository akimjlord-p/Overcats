from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BattleRequest:
    from_user_id: int
    to_user_id: int
    battle_type: str  # 'friendly', 'rated'
    created_at: datetime

@dataclass
class CampaignLevel:
    id: str
    name: str
    description: str
    enemy_bot_id: str
    reward_stac: int
    unlock_requirement: Optional[str] = None

@dataclass
class ShopItem:
    id: str
    name: str
    description: str
    price: int
    item_type: str  # 'character', 'ability'
    data: Dict  # character_id или ability_id