import copy
from typing import Dict, List, Tuple
from Data.Abilities.AbilityGenerator import AbilityGenerator
from Data.Characters.CharacterGenerator import CharacterGenerator
from bot.config import config

class BattleManager:
    def __init__(self, db_session):
        self.db = db_session
        self.active_battles: Dict[int, BattleSession] = {}
        self.abilities = AbilityGenerator.load_abilities(config.ABILITIES_YAML_PATH)
        self.character_templates = CharacterGenerator.load_characters(
            config.CHARACTERS_YAML_PATH, self.abilities
        )
    
    async def start_pvp_battle(self, user1_id: int, user2_id: int, battle_type: str) -> int:
        """Начинает PvP бой и возвращает ID боя"""
        battle_id = len(self.active_battles) + 1
        
        # Загружаем персонажей пользователей
        user1_char = self._load_user_character(user1_id)
        user2_char = self._load_user_character(user2_id)
        
        battle = BattleSession(user1_char, user2_char, battle_type, battle_id)
        self.active_battles[battle_id] = battle
        
        return battle_id
    
    async def start_pve_battle(self, user_id: int, bot_character_id: str) -> int:
        """Начинает PvE бой против бота"""
        battle_id = len(self.active_battles) + 1
        
        user_char = self._load_user_character(user_id)
        bot_char = copy.deepcopy(self.character_templates[bot_character_id])
        
        battle = BattleSession(user_char, bot_char, 'pve', battle_id)
        self.active_battles[battle_id] = battle
        
        return battle_id
    
    async def make_turn(self, battle_id: int, user_id: int, ability_id: str) -> Tuple[str, bool]:
        """Совершает ход в бою, возвращает результат и закончен ли бой"""
        if battle_id not in self.active_battles:
            return "Бой не найден", True
        
        battle = self.active_battles[battle_id]
        
        # Определяем кто ходит
        if user_id == battle.player1.user_id:
            attacker = battle.player1
            defender = battle.player2
        else:
            attacker = battle.player2
            defender = battle.player1
        
        # Используем способность
        ability = next((a for a in attacker.abilities if a.name == ability_id), None)
        if not ability:
            return "Способность не найдена", False
        
        result = ability.use(attacker.name, defender.name)
        battle.log.append(result)
        
        # Обновляем эффекты
        attacker.update_effects()
        defender.update_effects()
        
        # Проверяем конец боя
        if battle.is_battle_over():
            winner = battle.get_winner()
            await self._finish_battle(battle, winner)
            return f"Бой окончен! Победитель: {winner}", True
        
        return result, False
    
    def _load_user_character(self, user_id: int):
        """Загружает персонажа пользователя из БД"""
        # Здесь будет логика загрузки из БД
        # Пока заглушка - возвращаем копию шаблона
        return copy.deepcopy(self.character_templates['northpaw_veteran'])
    
    async def _finish_battle(self, battle, winner):
        """Завершает бой и начисляет награды"""
        # Здесь будет логика завершения боя
        pass

class BattleSession:
    def __init__(self, player1, player2, battle_type: str, battle_id: int):
        self.player1 = player1
        self.player2 = player2
        self.battle_type = battle_type
        self.battle_id = battle_id
        self.current_turn = 1
        self.log: List[str] = []
    
    def is_battle_over(self) -> bool:
        return not self.player1.is_alive() or not self.player2.is_alive()
    
    def get_winner(self):
        if self.player1.is_alive() and not self.player2.is_alive():
            return self.player1.name
        elif not self.player1.is_alive() and self.player2.is_alive():
            return self.player2.name
        return None