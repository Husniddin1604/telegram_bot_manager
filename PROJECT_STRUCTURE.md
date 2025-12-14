# Telegram Bot Manager - Project Structure

## Overview
This is a Telegram bot management application built with Python, Kivy for the GUI, and aiogram for Telegram bot functionality. The application allows users to manage multiple Telegram bots, send messages, and create publications.

## Project Structure

### Root Directory
- `main.py` - The main application entry point. Initializes the Kivy application and sets up the screen manager.
- `requirements.txt` - Lists all Python dependencies including Kivy, aiogram, and other required packages.
- `README.md` - Project documentation and setup instructions.

### Bot Module (`/bot`)
- `__init__.py` - Makes the bot directory a Python package.
- `bot_manager.py` - Manages multiple Telegram bot instances, handles token storage, and bot operations.
- `chat_manager.py` - Manages chat interactions and message handling for bots.
- `sender.py` - Handles sending messages and media through the bots.
- `async_loop.py` - Manages asynchronous operations and event loops.

### Data (`/data`)
- `bots.json` - Stores bot tokens and configurations.
- `chats.json` - Stores chat information and message history.

### Screens (`/screens`)
Contains Kivy screen classes for the application's UI:
- `__init__.py` - Makes the screens directory a Python package.
- `bots_screen.py` - Displays and manages the list of bots.
- `control_panel_screen.py` - Main control panel for bot operations.
- `create_publication_screen.py` - Interface for creating and scheduling publications.
- `log_stats_screen.py` - Displays logs and statistics.
- `login_screen.py` - Handles user authentication.
- `menu_screen.py` - Main navigation menu.
- `send_screen.py` - Interface for sending messages.

### UI (`/ui`)
Kivy language (.kv) files defining the UI layout for each screen:
- `__init__.py` - Makes the UI directory a Python package.
- `bots.kv` - UI layout for the bots screen.
- `control_panel.kv` - UI layout for the control panel.
- `create_publication.kv` - UI layout for creating publications.
- `log_stats.kv` - UI layout for logs and statistics.
- `login.kv` - UI layout for the login screen.
- `menu.kv` - UI layout for the main menu.
- `send.kv` - UI layout for the message sending interface.

## Dependencies
- **Kivy** (v2.3.1) - For the graphical user interface
- **aiogram** (v3.22.0) - For Telegram Bot API integration
- **aiohttp** - For asynchronous HTTP client/server
- **Other dependencies** for async operations, data validation, and utilities

## Key Features
- Manage multiple Telegram bots from a single interface
- Send messages and media to different chats
- Create and schedule publications
- View logs and statistics
- User-friendly mobile-responsive interface

## Data Storage
- Bot tokens and configurations are stored in `data/bots.json`
- Chat information and message history are stored in `data/chats.json`

## Security Note
- The application stores bot tokens locally in JSON files. Ensure proper file permissions are set.
- The application requires internet access to interact with the Telegram API.
