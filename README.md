# Quran Telegram Bot

A comprehensive Quran Telegram bot with audio recitations, tafsir, translations, and more.

## Features

### Core Bot Features
- **Quran Lookup**: Search by verse reference (2:255), surah name, or keywords
- **Whole Surah Audio**: 5 renowned reciters with file size estimates
- **Tafsir**: Authorized explanations from Ibn Kathir, Jalalayn, and Sa'di
- **Translations**: English (Sahih International, Clear Quran) and Amharic
- **Bookmarks**: Save and manage favorite verses
- **Daily Ayah**: Opt-in daily verse with audio and tafsir
- **Inline Mode**: Share verses in any chat with @YourBot

### Mini App (Power Features)
- Rich Quran reader with multi-translation view
- Full tafsir viewer with search
- Settings hub for customization
- Export to PDF/ePUB for offline reading

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your bot token and other settings
   ```

3. **Initialize database**:
   ```bash
   python scripts/init_database.py
   ```

4. **Load Quran data**:
   ```bash
   python scripts/load_quran_data.py
   ```

5. **Run the bot**:
   ```bash
   python main.py
   ```

## Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: SQLite (development), PostgreSQL (production)
- **Cache**: Redis for performance
- **Search**: Meilisearch for fast Quran search
- **Bot**: python-telegram-bot library

## Data Sources

- **Arabic Text**: Tanzil project (Hafs/Uthmani)
- **Translations**: Licensed editions with proper attribution
- **Tafsir**: Authorized English explanations
- **Audio**: Quran.com CDN for 5 reciters

## Commands

- `/start` - Welcome message and setup
- `/help` - Usage tips and examples
- `/settings` - Configure preferences
- `/bookmark` - Save current verse
- `/bookmarks` - List saved verses
- `/dailyayah` - Manage daily ayah subscription
- `/about` - Sources and licensing info

## License

MIT License - See LICENSE file for details
