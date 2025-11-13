from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    rating = Column(Integer, default=1000)
    stac = Column(Integer, default=50)
    current_character_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    characters = relationship("UserCharacter", back_populates="user")
    battles = relationship("Battle", back_populates="user")

class UserCharacter(Base):
    __tablename__ = 'user_characters'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    character_id = Column(String)
    
    user = relationship("User", back_populates="characters")

class Battle(Base):
    __tablename__ = 'battles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    opponent_type = Column(String)
    opponent_id = Column(String)
    result = Column(String)
    stac_reward = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="battles")