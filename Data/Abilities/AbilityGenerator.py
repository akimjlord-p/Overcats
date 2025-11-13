import yaml
import copy
from typing import Dict, List
from Data.Abilities.Ability import Ability
from Data.Effects.Effects import *

class AbilityGenerator:
    """Генератор способностей"""
    
    @staticmethod
    def load_abilities(file_path: str) -> Dict[str, Ability]:
        abilities = {}
        
        # Загружаем способности из YAML
        abilities.update(AbilityGenerator._load_yaml_abilities(file_path))
        
        # Добавляем кастомные способности
        abilities.update(AbilityGenerator._load_custom_abilities())
        
        return abilities
    
    @staticmethod
    def _load_yaml_abilities(file_path: str) -> Dict[str, Ability]:
        """Загружает способности из YAML файла"""
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file) or {}
        
        abilities = {}
        
        for ability_id, ability_data in data.items():
            display_name = ability_data.get('name', ability_id.replace('_', ' ').title())
            
            # Создаем эффекты
            effects = []
            for effect_data in ability_data.get('effects', []):
                effect = AbilityGenerator._create_effect(effect_data)
                if effect:
                    effects.append(effect)
            
            ability = Ability(
                name=ability_id,
                display_name=display_name,
                description=ability_data.get('description', ''),
                cooldown=ability_data.get('cooldown', 0),
                effects=effects,
                icon=ability_data.get('icon', ''),
                damage=ability_data.get('damage'),
                heal=ability_data.get('heal')
            )
            
            abilities[ability_id] = ability
        
        return abilities
    
    @staticmethod
    def _load_custom_abilities() -> Dict[str, Ability]:
        """Загружает кастомные способности"""
        custom_abilities = {}
        
        try:
            from Data.Abilities.custom_abilities import BloodSacrifice, FeelingOfBlood
            custom_abilities['blood_sacrifice'] = BloodSacrifice()
            custom_abilities['feeling_of_blood'] = FeelingOfBlood()
        except ImportError:
            print("Кастомные способности не найдены")
        
        return custom_abilities
    
    @staticmethod
    def _create_effect(effect_data: dict):
        effect_type = effect_data.get('type', '')
        power = effect_data.get('power', 0)
        duration = effect_data.get('duration', 1)
        target = effect_data.get('target', 'enemy')
        
        effect_classes = {
            'bleed': Bleed,
            'poison': Poison,
            'weakness': Weakness,
            'power': Power,
            'stun': Stun,
            'regeneration': Regeneration,
            'burning': Burning,
            'curse': Curse,
            'strength': Strength,
            'crack': Crack,
            'wisdom': Wisdom
        }
        
        if effect_type in effect_classes:
            effect_class = effect_classes[effect_type]
            effect_instance = effect_class(power=power, duration=duration)
            effect_instance.target = target
            return effect_instance
        
        return None