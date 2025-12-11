import os

# Базовая папка
BASE_DIR = "telegram_bot_manager"

# Структура каталогов и файлов
STRUCTURE = {
    "": ["main.py", "requirements.txt", "config.py", "README.md"],
    "assets/icons": ["send.png", "edit.png", "delete.png", "settings.png", "plus.png"],
    "assets/images": ["logo.png"],
    "assets/fonts": ["Roboto-Regular.ttf"],
    "gui": ["__init__.py", "app.py"],
    "gui/screens": [
        "__init__.py",
        "login_screen.py",
        "main_menu_screen.py",
        "publish_screen.py",
        "publications_list_screen.py",
        "settings_screen.py",
    ],
    "gui/widgets": [
        "__init__.py",
        "publication_card.py",
        "channel_selector.py",
        "datetime_picker.py",
        "media_uploader.py",
    ],
    "gui/themes": [
        "__init__.py",
        "light_theme.py",
        "dark_theme.py",
    ],
    "gui/kv": [
        "login.kv",
        "main_menu.kv",
        "publish.kv",
        "publications_list.kv",
        "settings.kv",
    ],
    "bot": [
        "__init__.py",
        "bot_manager.py",
        "publisher.py",
        "scheduler.py",
        "validators.py",
    ],
    "bot/handlers": [
        "__init__.py",
        "channel_handler.py",
        "admin_handler.py",
    ],
    "db": [
        "__init__.py",
        "database.py",
        "models.py",
    ],
    "db/repositories": [
        "__init__.py",
        "bot_repository.py",
        "channel_repository.py",
        "publication_repository.py",
    ],
    "db/migrations": ["init_db.sql"],
    "core": [
        "__init__.py",
        "auth_manager.py",
        "publication_manager.py",
        "channel_manager.py",
        "settings_manager.py",
        "media_handler.py",
        "encryption.py",
    ],
    "utils": [
        "__init__.py",
        "logger.py",
        "validators.py",
        "file_manager.py",
        "datetime_helper.py",
    ],
}


def create_structure():
    print(f"Создаю проект: {BASE_DIR}")

    for folder, files in STRUCTURE.items():
        dir_path = os.path.join(BASE_DIR, folder)
        os.makedirs(dir_path, exist_ok=True)
        print(f"[DIR]  {dir_path}")

        for file in files:
            file_path = os.path.join(dir_path, file)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("")  # пустой файл
                print(f"[FILE] {file_path}")
            else:
                print(f"[SKIP] {file_path} уже существует")


if __name__ == "__main__":
    create_structure()
