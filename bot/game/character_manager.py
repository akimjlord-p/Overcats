import random
from datetime import datetime, timedelta
import sys
import os

# Добавляем корневую директорию в путь
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from Data.Characters.CharacterGenerator import CharacterGenerator
from Data.Characters.Character import Character
from Data.db import session
from Data.Models.CharacterModel import CharacterModel
from Data.Models.UserModel import UserModel


class CharacterManager:
    def __init__(self):
        self.generator = CharacterGenerator()

    def create_character(self, user_id: int, character_data: dict) -> Character:
        """Создание нового персонажа для пользователя"""
        try:
            # Создаем персонажа через генератор
            character = self.generator.generate_character(
                character_data.get('name'),
                character_data.get('archetype'),
                character_data.get('background')
            )

            # Сохраняем в базу данных
            character_model = CharacterModel(
                user_id=user_id,
                name=character.name,
                archetype=character.archetype,
                background=character.background,
                strength=character.stats.strength,
                agility=character.stats.agility,
                intelligence=character.stats.intelligence,
                charisma=character.stats.charisma,
                health=character.health,
                max_health=character.max_health,
                level=character.level,
                experience=character.experience,
                created_at=datetime.now()
            )

            session.add(character_model)
            session.commit()

            # Обновляем ID персонажа
            character.id = character_model.id
            return character

        except Exception as e:
            session.rollback()
            raise e

    def get_character(self, user_id: int) -> Character:
        """Получение персонажа пользователя"""
        character_model = session.query(CharacterModel).filter_by(user_id=user_id).first()

        if not character_model:
            return None

        # Создаем объект Character из модели
        from Data.Stats.CharacterStats import CharacterStats

        stats = CharacterStats(
            strength=character_model.strength,
            agility=character_model.agility,
            intelligence=character_model.intelligence,
            charisma=character_model.charisma
        )

        character = Character(
            id=character_model.id,
            name=character_model.name,
            archetype=character_model.archetype,
            background=character_model.background,
            stats=stats,
            health=character_model.health,
            max_health=character_model.max_health,
            level=character_model.level,
            experience=character_model.experience
        )

        return character

    def update_character(self, character: Character) -> None:
        """Обновление данных персонажа"""
        try:
            character_model = session.query(CharacterModel).filter_by(id=character.id).first()

            if character_model:
                character_model.name = character.name
                character_model.archetype = character.archetype
                character_model.background = character.background
                character_model.strength = character.stats.strength
                character_model.agility = character.stats.agility
                character_model.intelligence = character.stats.intelligence
                character_model.charisma = character.stats.charisma
                character_model.health = character.health
                character_model.max_health = character.max_health
                character_model.level = character.level
                character_model.experience = character.experience

                session.commit()

        except Exception as e:
            session.rollback()
            raise e

    def delete_character(self, user_id: int) -> bool:
        """Удаление персонажа пользователя"""
        try:
            character_model = session.query(CharacterModel).filter_by(user_id=user_id).first()

            if character_model:
                session.delete(character_model)
                session.commit()
                return True
            return False

        except Exception as e:
            session.rollback()
            raise e

    def add_experience(self, user_id: int, exp: int) -> bool:
        """Добавление опыта персонажу"""
        try:
            character_model = session.query(CharacterModel).filter_by(user_id=user_id).first()

            if character_model:
                character_model.experience += exp

                # Проверка повышения уровня
                if character_model.experience >= self._get_exp_for_next_level(character_model.level):
                    character_model.level += 1
                    # Здесь можно добавить улучшение характеристик

                session.commit()
                return True
            return False

        except Exception as e:
            session.rollback()
            raise e

    def _get_exp_for_next_level(self, current_level: int) -> int:
        """Расчет необходимого опыта для следующего уровня"""
        return current_level * 100  # Базовая формула