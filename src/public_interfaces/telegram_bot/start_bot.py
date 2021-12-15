"""Module for strating the telegram bot and all the command handlers."""

import logging
from os import environ

from telegram import Bot
from telegram.ext import Updater, CommandHandler
from src.public_interfaces.telegram_bot.commands.actualizar import actualizar
from src.public_interfaces.telegram_bot.commands.ver_valores import ver_valores
from src.public_interfaces.telegram_bot.messages.dolarblue_report import send_dolarvalue_report


def start_telegram_bot() -> None:
    """Start the telegram bot"""
    logging.info("Starting Telegram bot")

    updater = Updater(token=environ.get('TELEGRAM_BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    all_handlers = [
        CommandHandler("ver_valores", ver_valores),
        CommandHandler("actualizar", actualizar)
    ]

    messages: callable[[Bot], None] = [
        send_dolarvalue_report
    ]

    for handler in all_handlers:
        dispatcher.add_handler(handler)

    for message in messages:
        message(updater.bot)

    updater.start_polling()
