from abc import ABC, abstractmethod
from typing import List
import copy

class BaseCharacter(ABC):
    def __init__(self, name: str, max_health: float, armor: float, picture: str):
        self.name = name
        self.picture = picture
        self.current_health = max_health
        self.max_health = max_health
        self.current_armor = armor
        self.base_armor = armor
        self.abilities = []
        self.effects = []
        self.current_magic_amplify = 0
        self.base_magic_amplify = 0
        self.current_attack_amplify = 0
        self.base_attack_amplify = 0
        self.stunned = False

    def take_magic_damage(self, damage: float, amplify=1) -> str:
        actual_damage = max(1.0, damage * (1 - self.current_magic_resistance) * amplify)
        self.current_health = max(0.0, self.current_health - actual_damage)
        return f'📜{actual_damage}'

    def take_physical_damage(self, damage: float, amplify=1) -> str:
        actual_damage = max(1.0, damage * (1 - self.current_armor) * amplify)
        self.current_health = max(0.0, self.current_health - actual_damage)
        return f'🗡️{actual_damage}'
    
    def heal(self, hp_points) -> str:
        self.current_health = min(self.max_health, self.current_health + hp_points)
        return f'❤️‍🩹 {hp_points}'

    def add_ability(self, ability):
        self.abilities.append(ability)

    def update_abilities(self):
        for ability in self.abilities:
            ability.update_cooldown()

    def add_effect(self, effect):
        self.effects.append(effect)
        return effect.info()

    def remove_effect(self, effect):
        if effect in self.effects:
            self.effects.remove(effect)

    def update_effects(self):
        self.stunned = False
        self.current_armor = self.base_armor
        self.current_magic_amplify = self.base_magic_amplify
        self.current_attack_amplify = self.base_attack_amplify

        effects_to_remove = []
        for effect in self.effects:
            effect.apply_effect(self)
            effect.duration -= 1
            if effect.duration <= 0:
                effects_to_remove.append(effect)

        for effect in effects_to_remove:
            effect.on_remove(self)
            self.effects.remove(effect)

    def is_alive(self) -> bool:
        return self.current_health > 0

    def info(self) -> str:
        """Возвращает базовую информацию о персонаже"""
        info = f"Здоровье: {self.current_health:.1f}/{self.max_health:.1f}\n"
        info += f"Броня: {self.current_armor:.1%}\n"
        if hasattr(self, 'current_magic_resistance'):
            info += f"Маг. сопротивление: {self.current_magic_resistance:.1%}\n"
        info += f"Сила атаки: {self.current_attack_amplify:+.1%}\n"
        info += f"Сила магии: {self.current_magic_amplify:+.1%}"
        return info

    def __str__(self) -> str:
        return f"{self.name} - HP: {self.current_health:.1f}/{self.max_health:.1f}"