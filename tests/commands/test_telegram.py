from bots.telegram_bot.telegram_bot import TelegramBotService
from unittest.mock import MagicMock
from telegram import Update

def test_start_command():
    bot = TelegramBotService(token="fake-token")
    update = MagicMock(spec=Update)
    context = MagicMock()

    update.message.reply_text = MagicMock()

    # Call the start command
    bot.start_command(update, context)

    # Check if the start message was sent
    update.message.reply_text.assert_called_once_with("Hello! This is your Telegram bot.")
