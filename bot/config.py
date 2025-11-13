from dataclasses import dataclass, field
from typing import List
import os

@dataclass
class Config:
    BOT_TOKEN: str = "8290905107:AAHvs3Vuj6WlZdNCyH8kZIcF_0zDyNmKGCw"
    DATABASE_URL: str = "sqlite:///overcats.db"
    
    # Настройки валюты
    CURRENCY_NAME: str = "Stone Acorn"
    CURRENCY_SYMBOL: str = "STAC"
    
    # Награды
    PVP_WIN_REWARD: int = 10
    PVP_LOSE_REWARD: int = 3
    CAMPAIGN_REWARD_MULTIPLIER: int = 5
    
    # Пути
    MEDIA_PATH: str = "media/characters/"
    CHARACTERS_YAML_PATH: str = "Data/Characters/characters.yaml"
    ABILITIES_YAML_PATH: str = "Data/Abilities/abilities.yaml"
    
    # Админы (замените на ваш Telegram ID)
    ADMIN_IDS: List[int] = field(default_factory=lambda: [123456789])

config = Config()