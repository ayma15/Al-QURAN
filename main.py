import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, filters
from config import Config
from handlers.command_handlers import CommandHandlers
from handlers.message_handlers import MessageHandlers
from handlers.callback_handlers import CallbackHandlers
from utils.cache import CacheManager
from utils.search import SearchManager
from services.quran_service import QuranService
from services.user_service import UserService
from services.audio_service import AudioService

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

class QuranBot:
    def __init__(self):
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        self.cache_manager = CacheManager()
        self.search_manager = SearchManager()
        self.quran_service = QuranService()
        self.user_service = UserService()
        self.audio_service = AudioService()
        
        # Initialize handlers
        self.command_handlers = CommandHandlers(
            self.quran_service, 
            self.user_service, 
            self.audio_service,
            self.cache_manager
        )
        self.message_handlers = MessageHandlers(
            self.quran_service,
            self.search_manager,
            self.cache_manager
        )
        self.callback_handlers = CallbackHandlers(
            self.quran_service,
            self.user_service,
            self.audio_service,
            self.cache_manager
        )
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all bot handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.command_handlers.start))
        self.application.add_handler(CommandHandler("help", self.command_handlers.help_command))
        self.application.add_handler(CommandHandler("settings", self.command_handlers.settings))
        self.application.add_handler(CommandHandler("bookmark", self.command_handlers.bookmark))
        self.application.add_handler(CommandHandler("bookmarks", self.command_handlers.bookmarks))
        self.application.add_handler(CommandHandler("dailyayah", self.command_handlers.daily_ayah))
        self.application.add_handler(CommandHandler("about", self.command_handlers.about))
        self.application.add_handler(CommandHandler("privacy", self.command_handlers.privacy))
        
        # Message handlers (for free text search)
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handlers.handle_text_message)
        )
        
        # Callback query handlers (for inline keyboards)
        self.application.add_handler(CallbackQueryHandler(self.callback_handlers.handle_callback))
        
        # Inline query handler (for @bot mentions)
        self.application.add_handler(InlineQueryHandler(self.message_handlers.handle_inline_query))
    
    async def run(self):
        """Start the bot"""
        try:
            logger.info("Starting Quran Bot...")
            await self.application.initialize()
            await self.application.start()
            await self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
        finally:
            await self.application.stop()
            await self.application.shutdown()

def main():
    """Main entry point"""
    try:
        Config.validate()
        bot = QuranBot()
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
