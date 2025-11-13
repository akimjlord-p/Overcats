from typing import List, Dict

class Ability:
    def __init__(self, name: str, display_name: str, description: str, cooldown: int, 
                 effects: List, icon: str = '', damage: dict = None, heal: dict = None):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.effects = effects
        self.icon = icon
        self.damage = damage
        self.heal = heal
    
    def use(self, user, enemy) -> str:
        if self.current_cooldown > 0:
            return f"{self.get_name()} на перезарядке! Осталось: {self.current_cooldown}"
        
        self.current_cooldown = self.cooldown
        
        # Применяем урон с учетом типа урона
        if self.damage:
            target = user if self.damage['target'] == 'self' else enemy
            damage_value = self.damage['value']
            damage_type = self.damage['type']
            
            # Наносим урон в зависимости от типа
            if damage_type == 'physical':
                # target.take_physical_damage(damage_value)
                pass
            elif damage_type == 'magical':
                # target.take_magic_damage(damage_value)
                pass
            elif damage_type == 'pure':
                # target.take_clear_damage(damage_value)
                pass
        
        # Применяем лечение
        if self.heal:
            target = user if self.heal['target'] == 'self' else enemy
            heal_value = self.heal['value']
            # target.heal(heal_value)
        
        # Применяем эффекты
        for effect in self.effects:
            target = user if effect.target == 'self' else enemy
            effect.apply_effect(target)
        
        return f"{user} использует {self.get_name()}!"
    
    def get_full_info(self) -> str:
        """Возвращает полную информацию о способности"""
        info = f"{self.get_name()}\n{self.description}\n"
        
        if self.damage:
            damage_type_names = {
                'physical': 'физический',
                'magical': 'магический', 
                'pure': 'чистый'
            }
            damage_type = damage_type_names.get(self.damage['type'], self.damage['type'])
            target = "себя" if self.damage['target'] == 'self' else "врага"
            info += f"Урон: {self.damage['value']} ({damage_type}) - {target}\n"
        
        if self.heal:
            target = "себя" if self.heal['target'] == 'self' else "врага"
            info += f"Исцеление: {self.heal['value']} - {target}\n"
        
        if self.effects:
            info += "Эффекты:\n"
            for effect in self.effects:
                target = "себя" if effect.target == 'self' else "врага"
                duration = f" ({effect.duration} ходов)" if hasattr(effect, 'duration') else ""
                power = f" - {effect.power}" if hasattr(effect, 'power') and effect.power > 0 else ""
                info += f"  {effect.icon} {effect.description}{duration}{power} - {target}\n"
        
        info += f"Перезарядка: {self.cooldown} ходов"
        return info

    def get_name(self) -> str:
        return f'{self.icon} {self.display_name}'

    def update_cooldown(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1