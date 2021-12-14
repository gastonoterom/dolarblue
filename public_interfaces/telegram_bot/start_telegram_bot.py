"""Module for strating the telegram bot and all the command handlers."""

import logging
from os import environ
from telegram.ext import Updater
from public_interfaces.telegram_bot.handlers import all_handlers

def start_telegram_bot() -> None:
    """Start the telegram bot"""
    logging.info("Starting Telegram bot")

    updater = Updater(token=environ.get('TELEGRAM_BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    handlers = all_handlers
    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling()
