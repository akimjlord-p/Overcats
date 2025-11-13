import yaml
import copy
from typing import Dict
from Data.Characters.Character import BaseCharacter
from bot.config import config

class CharacterGenerator:
    """Генератор персонажей"""
    
    @staticmethod
    def load_characters(file_path: str, abilities_dict: Dict) -> Dict[str, BaseCharacter]:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file) or {}
        
        characters = {}
        
        for char_id, char_data in data.items():
            character = CharacterGenerator._create_character(char_id, char_data)
            
            # Добавляем способности если они есть
            if 'abilities' in char_data:
                for ability_name in char_data['abilities']:
                    if ability_name in abilities_dict:
                        # Копируем способность чтобы у каждого персонажа была своя
                        ability_copy = copy.deepcopy(abilities_dict[ability_name])
                        character.add_ability(ability_copy)
            
            characters[char_id] = character
        
        return characters

    @staticmethod
    def _create_character(char_id: str, char_data: dict) -> BaseCharacter:
        """Создает персонажа из данных"""
        # Создаем конкретного персонажа (наследуем от BaseCharacter)
        class ConcreteCharacter(BaseCharacter):
            def __init__(self, name, max_health, armor, picture):
                super().__init__(name, max_health, armor, picture)
                # Устанавливаем дополнительные параметры
                self.current_magic_resistance = char_data.get('magic_resistance', 0.1)
                self.base_magic_resistance = char_data.get('magic_resistance', 0.1)
                
                self.current_magic_amplify = char_data.get('magic_amplify', 0)
                self.base_magic_amplify = char_data.get('magic_amplify', 0)
                
                self.current_attack_amplify = char_data.get('attack_amplify', 0)
                self.base_attack_amplify = char_data.get('attack_amplify', 0)
        
        character = ConcreteCharacter(
            name=char_data.get('name', char_id),
            max_health=char_data.get('max_health', 100),
            armor=char_data.get('armor', 0.1),
            picture=char_data.get('picture', '')
        )
        
        return character