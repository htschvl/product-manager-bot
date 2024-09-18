from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import logging

class TelegramBotService:
    def __init__(self, token: str):
        self.token = token
        self.app = ApplicationBuilder().token(self.token).build()

    def start_command(self, update: Update, context: CallbackContext) -> None:
        """Responds to the /start command."""
        update.message.reply_text("Hello! This is your Telegram bot.")

    def load_handlers(self) -> None:
        """Load command handlers for the bot."""
        start_handler = CommandHandler('start', self.start_command)
        self.app.add_handler(start_handler)

    def run(self) -> None:
        """Runs the Telegram bot."""
        self.load_handlers()
        logging.info("Starting Telegram bot...")
        self.app.run_polling()
