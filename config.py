# config.py
import os
from pathlib import Path
from cryptography.fernet import Fernet

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = os.getenv("DB_PATH", str(DATA_DIR / "app.db"))
DB_URL = f"sqlite:///{DB_PATH}"

# Генерация ключа шифрования если не задан
ENCRYPT_KEY_PATH = DATA_DIR / "encryption.key"
if os.getenv("ENCRYPT_KEY"):
    ENCRYPT_KEY = os.getenv("ENCRYPT_KEY").encode()
elif ENCRYPT_KEY_PATH.exists():
    with open(ENCRYPT_KEY_PATH, "rb") as f:
        ENCRYPT_KEY = f.read()
else:
    ENCRYPT_KEY = Fernet.generate_key()
    with open(ENCRYPT_KEY_PATH, "wb") as f:
        f.write(ENCRYPT_KEY)

APP_BOT_TOKEN = os.getenv("APP_BOT_TOKEN")
THEME = os.getenv("THEME", "light").lower()


class Config:
    DB_URL = DB_URL
    ENCRYPT_KEY = ENCRYPT_KEY
    APP_BOT_TOKEN = APP_BOT_TOKEN
    THEME = THEME