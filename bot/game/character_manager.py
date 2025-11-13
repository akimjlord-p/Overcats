import yaml
from typing import Dict, List
from bot.config import config
from Data.Characters.CharacterGenerator import CharacterGenerator
from Data.Abilities.AbilityGenerator import AbilityGenerator

class CharacterManager:
    def __init__(self):
        self.abilities = AbilityGenerator.load_abilities(config.ABILITIES_YAML_PATH)
        self.character_templates = CharacterGenerator.load_characters(
            config.CHARACTERS_YAML_PATH, self.abilities
        )
        self.starting_characters = ['northpaw_veteran', 'bloodfang_berserker']
    
    def get_all_characters(self) -> Dict:
        """Возвращает всех персонажей из YAML"""
        return self.character_templates
    
    def get_starting_characters(self) -> Dict:
        """Возвращает стартовых персонажей"""
        return {char_id: self.character_templates[char_id] 
                for char_id in self.starting_characters 
                if char_id in self.character_templates}
    
    def get_purchasable_characters(self) -> Dict:
        """Возвращает персонажей для покупки (все кроме стартовых)"""
        return {char_id: char 
                for char_id, char in self.character_templates.items() 
                if char_id not in self.starting_characters}
    
    def get_character_info(self, character_id: str) -> str:
        """Возвращает полную информацию о персонаже"""
        if character_id not in self.character_templates:
            return "Персонаж не найден"
        
        character = self.character_templates[character_id]
        info = f"🎭 <b>{character.name}</b>\n"
        info += f"{character.picture} {character.info()}\n\n"
        
        info += "<b>Способности:</b>\n"
        for ability in character.abilities:
            info += f"• {ability.get_full_info()}\n\n"
        
        return info