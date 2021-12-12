"""Module for strating the telegram bot and all the command handlers."""

from os import environ
from typing import List
from telegram.ext import Updater
from telegram.ext import CommandHandler

def start_telegram_bot() -> None:
    """Start the telegram bot"""
    updater = Updater(token=environ.get('TELEGRAM_BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    handlers: List[CommandHandler] = []
    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling()
