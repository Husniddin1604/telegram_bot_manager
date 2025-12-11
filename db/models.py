# db/models.py
# SQLAlchemy модели для проекта telegram_publisher
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Text,
)
from sqlalchemy.dialects.sqlite import JSON as SQLITE_JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Статусы публикации — 'scheduled', 'sent', 'error'
from enum import Enum as PyEnum


class PublicationStatus(PyEnum):
    scheduled = "scheduled"
    sent = "sent"
    error = "error"


class Bot(Base):
    """
    Таблица Bots:
    - id: PK
    - name: название бота (человекочитаемое)
    - encrypted_token: токен бота, зашифрованный с помощью Fernet (bytes/str)
    """
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    encrypted_token = Column(String, nullable=False)

    channels = relationship("Channel", back_populates="bot", cascade="all, delete-orphan")
    publications = relationship("Publication", back_populates="bot", cascade="all, delete-orphan")


class Channel(Base):
    """
    Таблица Channels:
    - id: PK
    - bot_id: FK -> bots.id
    - title: заголовок / имя канала
    - channel_id: идентификатор канала (username или numeric id в Telegram)
    """
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bot_id = Column(Integer, ForeignKey("bots.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    channel_id = Column(String(255), nullable=False)  # строка, т.к. может быть '@channel' или числовой id

    bot = relationship("Bot", back_populates="channels")
    publications = relationship("Publication", back_populates="channel", cascade="all, delete-orphan")


class Publication(Base):
    """
    Таблица Publications:
    - id: PK
    - bot_id: FK -> bots.id
    - channel_id: FK -> channels.id
    - text: текст публикации
    - media_path: путь к медиа (опционально)
    - inline_buttons: JSON (список кнопок/структур)
    - status: enum('scheduled','sent','error')
    - scheduled_time: когда запланировано (UTC)
    - sent_at: когда отправлено (UTC)
    - error_message: сообщение об ошибке (если есть)
    """
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bot_id = Column(Integer, ForeignKey("bots.id", ondelete="CASCADE"), nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)

    text = Column(Text, nullable=True)
    media_path = Column(String(1024), nullable=True)
    inline_buttons = Column(SQLITE_JSON, nullable=True)  # JSON-структура для inline кнопок

    status = Column(Enum(PublicationStatus), default=PublicationStatus.scheduled, nullable=False)

    scheduled_time = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    bot = relationship("Bot", back_populates="publications")
    channel = relationship("Channel", back_populates="publications")
