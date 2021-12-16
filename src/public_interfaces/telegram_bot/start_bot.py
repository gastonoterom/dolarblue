from typing import Callable, List, cast
from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import Dispatcher
from src.public_interfaces.telegram_bot.commands.actualizar import actualizar
from src.public_interfaces.telegram_bot.commands.ver_valores import ver_valores
from src.public_interfaces.telegram_bot.config import BOT_TOKEN
from src.public_interfaces.telegram_bot.messages.dolarblue_report import send_dolarblue_report


def start_telegram_bot() -> None:
    """Start the telegram bot with its command handlers and event-based messaging"""
    updater = Updater(token=BOT_TOKEN, use_context=True)

    dispatcher = cast(Dispatcher, updater.dispatcher)

    all_handlers = [
        CommandHandler("ver_valores", ver_valores),
        CommandHandler("actualizar", actualizar)
    ]

    messages: List[Callable] = [
        send_dolarblue_report
    ]

    for handler in all_handlers:
        dispatcher.add_handler(handler)

    for message in messages:
        message(bot=updater.bot)

    updater.start_polling()
