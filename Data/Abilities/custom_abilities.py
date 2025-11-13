from Data.Abilities.Ability import Ability
from Data.Effects.Effects import *

class BloodSacrifice(Ability):
    def __init__(self):
        super().__init__(
            name="blood_sacrifice",
            display_name="Кровавая жертва",
            description="При виде собственной крови берсерк впадает в ярость",
            cooldown=1,
            effects=[],
            icon="🩸"
        )
        self.uses = 0
    
    def use(self, user, enemy):
        self.uses += 1
        user.add_effect(Power(0.2, 3))
        user.add_effect(Regeneration(15, 2))
        user.add_effect(Wisdom(0.15, 3))
        user.take_physical_damage(100 + self.uses * 60)
        return f"{user} использует {self.get_name()}"
    
    def get_full_info(self):
        info = f"{self.get_name()}\n{self.description}\n"
        current_damage = 100 + (self.uses * 60)
        info += f"Наносит владельцу: {current_damage} физического урона\n"
        info += f"Базовый урон: 100 + 60 за каждое использование\n"
        info += "Эффекты на себя:\n"
        info += "  💪 +20% силы атаки (3 хода)\n"
        info += "  ♻️ +15 здоровья (2 хода)\n" 
        info += "  🧠 +15% мудрости (3 хода)\n"
        info += f"Перезарядка: {self.cooldown} ходов"
        if self.uses > 0:
            info += f"\nИспользований: {self.uses}"
        return info


class FeelingOfBlood(Ability):
    def __init__(self):
        super().__init__(
            name="feeling_of_blood",
            display_name="Чувство крови",
            description="Магия крови сливает кровь из открытых ран",
            cooldown=3,
            effects=[],
            icon="💀"
        )
    
    def use(self, user, enemy):
        bleedings = 0
        for effect in enemy.effects:
            if isinstance(effect, Bleed):
                bleedings += 1
                enemy.remove_effect(effect)
        enemy.take_magic_damage(15 + bleedings * 40)
        user.heal(10 + bleedings * 20)
        return f"{user} использует {self.get_name()}"
    
    def get_full_info(self):
        info = f"{self.get_name()}\n{self.description}\n"
        info += "Базовый урон: 15 магического урона\n"
        info += "Базовое лечение: 10 здоровья\n"
        info += "Дополнительный урон: +40 за каждое кровотечение\n"
        info += "Дополнительное лечение: +20 за каждое кровотечение\n"
        info += "Снимает все эффекты кровотечения с врага\n"
        info += f"Перезарядка: {self.cooldown} ходов"
        return info