# db/database.py
# Инициализация БД, сессий и простые CRUD-функции.
import os
from typing import List, Optional
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from cryptography.fernet import Fernet, InvalidToken

from .models import Base, Bot, Channel, Publication, PublicationStatus

# По умолчанию — файл sqlite в проекте. Для тестов можно передать 'sqlite:///:memory:'.
DEFAULT_DB_URL = os.getenv("DATABASE_URL", "sqlite:///telegram_publisher.db")


def _get_fernet(encryption_key: Optional[bytes]) -> Optional[Fernet]:
    """
    Создаёт экземпляр Fernet при наличии ключа.
    encryption_key может быть bytes или base64-encoded str.
    """
    if not encryption_key:
        return None
    if isinstance(encryption_key, str):
        encryption_key = encryption_key.encode()
    return Fernet(encryption_key)


class Database:
    """
    Обёртка для работы с SQLAlchemy engine/session и простыми CRUD-операциями.
    При создании можно указать encryption_key (bytes или str) для шифрования токенов.
    """
    def __init__(self, db_url: str = DEFAULT_DB_URL, encryption_key: Optional[bytes] = None, echo: bool = False):
        self.engine = create_engine(db_url, echo=echo, connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {})
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.fernet = _get_fernet(encryption_key)  # None если ключ не указан

    def init_db(self):
        """Создаёт таблицы (если ещё не созданы)."""
        Base.metadata.create_all(bind=self.engine)

    # -----------------
    # Шифрование токена
    # -----------------
    def encrypt_token(self, token: str) -> str:
        """Зашифровать токен (возвращает base64-encoded строку)."""
        if not self.fernet:
            raise RuntimeError("Encryption key is not configured")
        if isinstance(token, str):
            token = token.encode()
        return self.fernet.encrypt(token).decode()

    def decrypt_token(self, encrypted_token: str) -> str:
        """Дешифровать токен (возвращает строку)."""
        if not self.fernet:
            raise RuntimeError("Encryption key is not configured")
        try:
            return self.fernet.decrypt(encrypted_token.encode()).decode()
        except InvalidToken:
            raise ValueError("Invalid encryption key or corrupted token")

    # -------------
    # CRUD-методы
    # -------------
    def add_bot(self, name: str, token: str, session: Optional[Session] = None) -> Bot:
        """
        Добавляет бота. Токен шифруется.
        Возвращает объект Bot.
        """
        own_session = False
        if session is None:
            session = self.SessionLocal()
            own_session = True
        try:
            encrypted = self.encrypt_token(token)
            bot = Bot(name=name, encrypted_token=encrypted)
            session.add(bot)
            session.commit()
            session.refresh(bot)
            return bot
        except IntegrityError:
            session.rollback()
            raise
        finally:
            if own_session:
                session.close()

    def get_bot_token(self, bot_id: int, session: Optional[Session] = None) -> str:
        """Возвращает расшифрованный токен бота по id."""
        own_session = False
        if session is None:
            session = self.SessionLocal()
            own_session = True
        try:
            bot = session.query(Bot).filter(Bot.id == bot_id).one_or_none()
            if bot is None:
                raise ValueError(f"Bot with id {bot_id} not found")
            return self.decrypt_token(bot.encrypted_token)
        finally:
            if own_session:
                session.close()

    def add_channel(self, bot_id: int, title: str, channel_id: str, session: Optional[Session] = None) -> Channel:
        """
        Добавляет канал, связанный с ботом.
        channel_id может быть '@username' или numeric id в строковом виде.
        """
        own_session = False
        if session is None:
            session = self.SessionLocal()
            own_session = True
        try:
            channel = Channel(bot_id=bot_id, title=title, channel_id=channel_id)
            session.add(channel)
            session.commit()
            session.refresh(channel)
            return channel
        except IntegrityError:
            session.rollback()
            raise
        finally:
            if own_session:
                session.close()

    def add_publication(
        self,
        bot_id: int,
        channel_db_id: int,
        text: Optional[str] = None,
        media_path: Optional[str] = None,
        inline_buttons: Optional[dict] = None,
        scheduled_time: Optional[datetime] = None,
        status: PublicationStatus = PublicationStatus.scheduled,
        session: Optional[Session] = None,
    ) -> Publication:
        """
        Добавляет публикацию.
        channel_db_id — это внутренний id из таблицы channels (не telegram channel_id).
        """
        own_session = False
        if session is None:
            session = self.SessionLocal()
            own_session = True
        try:
            pub = Publication(
                bot_id=bot_id,
                channel_id=channel_db_id,
                text=text,
                media_path=media_path,
                inline_buttons=inline_buttons,
                scheduled_time=scheduled_time,
                status=status,
            )
            session.add(pub)
            session.commit()
            session.refresh(pub)
            return pub
        except IntegrityError:
            session.rollback()
            raise
        finally:
            if own_session:
                session.close()

    def get_publications_by_status(self, status: PublicationStatus, session: Optional[Session] = None) -> List[Publication]:
        """
        Получить список публикаций по статусу.
        """
        own_session = False
        if session is None:
            session = self.SessionLocal()
            own_session = True
        try:
            pubs = session.query(Publication).filter(Publication.status == status).all()
            return pubs
        finally:
            if own_session:
                session.close()

    # Дополнительные утилиты (обновление статуса/отправки)
    def mark_publication_sent(self, publication_id: int, sent_at: Optional[datetime] = None, session: Optional[Session] = None):
        own_session = False
        if session is None:
            session = self.SessionLocal()
            own_session = True
        try:
            pub = session.query(Publication).get(publication_id)
            if pub is None:
                raise ValueError("Publication not found")
            pub.status = PublicationStatus.sent
            pub.sent_at = sent_at or datetime.utcnow()
            session.commit()
            session.refresh(pub)
            return pub
        finally:
            if own_session:
                session.close()

    def mark_publication_error(self, publication_id: int, error_message: str, session: Optional[Session] = None):
        own_session = False
        if session is None:
            session = self.SessionLocal()
            own_session = True
        try:
            pub = session.query(Publication).get(publication_id)
            if pub is None:
                raise ValueError("Publication not found")
            pub.status = PublicationStatus.error
            pub.error_message = error_message
            session.commit()
            session.refresh(pub)
            return pub
        finally:
            if own_session:
                session.close()
