import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "@QuranBot")

    # Bot runtime mode
    # - polling: local dev
    # - webhook: recommended for production deployments
    BOT_MODE = os.getenv("BOT_MODE", "polling").lower()

    # Webhook configuration
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")  # e.g. https://your-domain.com
    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/telegram/webhook")
    WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8080"))
    
    # Database Configuration
    # For production, prefer PostgreSQL:
    # postgresql+psycopg://user:pass@localhost:5432/quran_bot
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///quran_bot.db")
    
    # Redis Configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Audio Configuration
    AUDIO_BASE_URL = os.getenv("AUDIO_BASE_URL", "https://download.quranicaudio.com/quran/")
    RECITERS = {
        "mishary": {"id": 1, "name": "Mishary Rashid Alafasy", "folder": "mishary_alafasy"},
        "maher": {"id": 2, "name": "Maher Al-Muaiqly", "folder": "maher_al_muaiqly"},
        "saud": {"id": 3, "name": "Saud Al-Shuraim", "folder": "saud_al_shuraim"},
        "sudais": {"id": 4, "name": "Abdurrahman Al-Sudais", "folder": "abdul_rahman_al_sudais"},
        "salah": {"id": 5, "name": "Salah Bukhatir", "folder": "salah_bukhatir"}
    }
    
    # Tafsir Sources
    TAFSIR_SOURCES = {
        "ibn_kathir": {"name": "Ibn Kathir", "language": "en"},
        "jalalayn": {"name": "Jalalayn", "language": "en"},
        "saadi": {"name": "Sa'di", "language": "en"}
    }
    
    # Translations
    TRANSLATIONS = {
        "en_sahih": {"name": "Sahih International", "language": "en"},
        "en_clear": {"name": "The Clear Quran", "language": "en"},
        "am_hussein": {"name": "Amharic Translation", "language": "am"}
    }
    
    # Search Configuration
    MEILISEARCH_URL = os.getenv("MEILISEARCH_URL", "http://localhost:7700")
    MEILISEARCH_API_KEY = os.getenv("MEILISEARCH_API_KEY", "")
    
    # File Storage
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = 30
    RATE_LIMIT_PERIOD = 60  # seconds
    
    # Daily Ayah Configuration
    DAILY_AYAH_TIME = os.getenv("DAILY_AYAH_TIME", "07:00")  # 7 AM
    
    # Web App Configuration
    WEB_APP_URL = os.getenv("WEB_APP_URL", "https://your-domain.com")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        required_vars = ["TELEGRAM_BOT_TOKEN"]
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
