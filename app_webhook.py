import logging

from fastapi import FastAPI, Request, Response, HTTPException
from telegram import Update

from config import Config
from models.database import init_db
from handlers.command_handlers import CommandHandlers
from handlers.message_handlers import MessageHandlers
from handlers.callback_handlers import CallbackHandlers
from utils.cache import CacheManager
from utils.search import SearchManager
from services.quran_service import QuranService
from services.user_service import UserService
from services.audio_service import AudioService

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

app = FastAPI()

# Singletons
cache_manager = CacheManager()
search_manager = SearchManager()
quran_service = QuranService()
user_service = UserService()
audio_service = AudioService()

command_handlers = CommandHandlers(quran_service, user_service, audio_service, cache_manager)
message_handlers = MessageHandlers(quran_service, search_manager, cache_manager)
callback_handlers = CallbackHandlers(quran_service, user_service, audio_service, cache_manager)

telegram_app = None


@app.on_event("startup")
async def startup():
    global telegram_app
    from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, filters

    if not Config.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

    # Ensure DB tables exist (safe for first boot on Railway)
    init_db()

    telegram_app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", command_handlers.start))
    telegram_app.add_handler(CommandHandler("help", command_handlers.help_command))
    telegram_app.add_handler(CommandHandler("settings", command_handlers.settings))
    telegram_app.add_handler(CommandHandler("bookmark", command_handlers.bookmark))
    telegram_app.add_handler(CommandHandler("bookmarks", command_handlers.bookmarks))
    telegram_app.add_handler(CommandHandler("dailyayah", command_handlers.daily_ayah))
    telegram_app.add_handler(CommandHandler("about", command_handlers.about))
    telegram_app.add_handler(CommandHandler("privacy", command_handlers.privacy))

    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_text_message))
    telegram_app.add_handler(CallbackQueryHandler(callback_handlers.handle_callback))
    telegram_app.add_handler(InlineQueryHandler(message_handlers.handle_inline_query))

    await telegram_app.initialize()

    if Config.WEBHOOK_URL:
        webhook_full = Config.WEBHOOK_URL.rstrip("/") + Config.WEBHOOK_PATH
        logger.info("Setting webhook to %s", webhook_full)
        await telegram_app.bot.set_webhook(
            url=webhook_full,
            secret_token=Config.WEBHOOK_SECRET_TOKEN or None,
        )


@app.on_event("shutdown")
async def shutdown():
    global telegram_app
    if telegram_app:
        await telegram_app.shutdown()
        telegram_app = None


@app.get("/health")
def health():
    return {"ok": True, "mode": "webhook"}


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    if telegram_app is None:
        raise HTTPException(status_code=503, detail="Bot not initialized")

    if Config.WEBHOOK_SECRET_TOKEN:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret != Config.WEBHOOK_SECRET_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid secret token")

    payload = await request.json()
    update = Update.de_json(payload, telegram_app.bot)
    await telegram_app.process_update(update)
    return Response(status_code=200)
