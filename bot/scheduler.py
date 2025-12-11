# bot/scheduler.py (исправленная версия)
import asyncio
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.database import Database
from db.models import PublicationStatus
from bot.bot_manager import BotManager
from bot.publisher import send_publication
from config import Config

scheduler = None
bot_manager = None


async def check_and_send():
    """Проверка и отправка запланированных публикаций"""
    global bot_manager
    if not bot_manager:
        return

    db = Database(encryption_key=Config.ENCRYPT_KEY)
    db.init_db()

    now = datetime.now(timezone.utc)

    session = db.SessionLocal()
    try:
        from db.models import Publication
        pubs = session.query(Publication).filter(
            Publication.status == PublicationStatus.scheduled,
            Publication.scheduled_time <= now
        ).all()

        for pub in pubs:
            bot_instance = await bot_manager.get_bot(pub.bot_id)
            await send_publication(db, pub, bot_instance)
    finally:
        session.close()


async def start_scheduler(db: Database):
    """Запуск планировщика"""
    global bot_manager, scheduler

    bot_manager = BotManager(db)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send, "interval", seconds=15)
    scheduler.start()

    print("Планировщик публикаций запущен (проверка каждые 15 сек)")