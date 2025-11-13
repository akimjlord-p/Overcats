from typing import Dict, List
from bot.game.models import CampaignLevel

class CampaignManager:
    def __init__(self):
        self.campaigns = self._load_campaigns()
    
    def _load_campaigns(self) -> Dict[str, List[CampaignLevel]]:
        return {
            "cat_adventure": [
                CampaignLevel(
                    id="alley_cats",
                    name="Коты переулка",
                    description="Группа уличных котов охраняет свою территорию",
                    enemy_bot_id="street_cat_leader",
                    reward_stac=25
                ),
                CampaignLevel(
                    id="mouse_magic",
                    name="Магия мышей", 
                    description="Мыши-маги используют древние заклинания",
                    enemy_bot_id="mouse_mage",
                    reward_stac=35,
                    unlock_requirement="alley_cats"
                )
            ]
        }
    
    def get_campaign_levels(self, campaign_id: str) -> List[CampaignLevel]:
        """Возвращает уровни кампании"""
        return self.campaigns.get(campaign_id, [])