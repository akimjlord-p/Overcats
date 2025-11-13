import random
from abc import ABC, abstractmethod

class Effect:
    def __init__(self, power, duration, description, icon, apply_on_turn_end=False):
        self.power = power
        self.duration = duration
        self.description = description
        self.icon = icon
        self.apply_on_turn_end = apply_on_turn_end

    @abstractmethod
    def apply_effect(self, target):
        pass

    def __str__(self):
        return f' {self.icon}  Сила: {self.power} Длительность: {self.duration}'

    def info(self):
        return f'{self.description}{self.icon}  \nСила: {self.power} Длительность: {self.duration}'

    def on_remove(self, target):
        pass

class Bleed(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Вы истекаете кровью!', icon='🩸', apply_on_turn_end=True)

    def apply_effect(self, target):
        target.take_physical_damage(self.power)

class Poison(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Вас отравили ядом!', icon='☣️', apply_on_turn_end=True)

    def apply_effect(self, target):
        target.take_magic_damage(self.power)

class Weakness(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Вы изнемогаете!', icon='😪', apply_on_turn_end=False)

    def apply_effect(self, target):
        target.current_attack_amplify -= self.power
    
    def on_remove(self, target):
        target.current_attack_amplify += self.power

class Power(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Вы полны энергии!', icon='💪', apply_on_turn_end=False)

    def apply_effect(self, target):
        target.current_attack_amplify += self.power
    
    def on_remove(self, target):
        target.current_attack_amplify -= self.power

class Stun(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Вы оглушены!', icon='💫', apply_on_turn_end=False)

    def apply_effect(self, target):
        target.stunned = True
    
    def on_remove(self, target):
        target.stunned = False

class Regeneration(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Вы восполняете силы', icon='♻️', apply_on_turn_end=True)

    def apply_effect(self, target):
        target.current_health = min(target.max_health, target.current_health + self.power)

class Burning(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Вы горите магическим огнем!', icon='🔥', apply_on_turn_end=True)

    def apply_effect(self, target):
        target.take_magic_damage(self.power)

class Curse(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Вас прокляли!', icon='☠️', apply_on_turn_end=True)

    def apply_effect(self, target):
        target.take_magic_damage(self.power)

class Strength(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Вы укрепили свою боевую позицию', icon='🛡️', apply_on_turn_end=False)

    def apply_effect(self, target):
        target.current_armor += self.power
    
    def on_remove(self, target):
        target.current_armor -= self.power

class Crack(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Ваша броня сейчас менее эффективна!', icon='💥', apply_on_turn_end=False)

    def apply_effect(self, target):
        target.current_armor -= self.power
    
    def on_remove(self, target):
        target.current_armor += self.power

class Wisdom(Effect):
    def __init__(self, power, duration):
        super().__init__(power=power, duration=duration, description='Ваша мудрость возрастает!', icon='🧠', apply_on_turn_end=False)

    def apply_effect(self, target):
        target.current_magic_amplify += self.power
    
    def on_remove(self, target):
        target.current_magic_amplify -= self.power