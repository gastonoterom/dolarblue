"""This module contains an array with all the commands the bot handles."""

from telegram.ext.commandhandler import CommandHandler
from telegram_bot.commands.actualizar import actualizar
from telegram_bot.commands.ver_valores import ver_valores

all_handlers = [
    CommandHandler("ver_valores", ver_valores),
    CommandHandler("actualizar", actualizar)
]
