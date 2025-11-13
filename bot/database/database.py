from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from bot.config import config
from bot.database.models import Base

# Для SQLite используем синхронную версию
engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def init_db():
    """Инициализация БД"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Получение сессии БД"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()