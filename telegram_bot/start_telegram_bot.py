"""Module for strating the telegram bot and all the command handlers."""

from os import environ
from telegram.ext import Updater
from telegram_bot.handlers import all_handlers
from main import flask_logger

def start_telegram_bot() -> None:
    """Start the telegram bot"""
    flask_logger.info("Starting Telegram bot")

    updater = Updater(token=environ.get('TELEGRAM_BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    handlers = all_handlers
    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling()
