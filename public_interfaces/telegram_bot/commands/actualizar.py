"""Handler for bot command actualizar."""

from datetime import datetime
import logging
from telegram import Update
import telegram
from telegram.ext import CallbackContext
from classes.dolar_blue_sources.all_sources import all_dolar_blue_sources
from public_interfaces.telegram_bot.commands_middlewares.authorized_only import authorized_only

@authorized_only
def actualizar(update: Update, context: CallbackContext) -> None:
    """Handles the actualizar bot command, which updates all the dolarblue cached values"""
    logging.info("Updating dolarblue values")
    assert update.effective_chat is not None

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Actualizando valores de dolar blue.",
        parse_mode=telegram.ParseMode.MARKDOWN
    )

    parsed_date = datetime.now().strftime("%m-%d-%Y %H:%M")

    response = f"Cotizaciones actualizadas - {parsed_date}\n"

    for src in all_dolar_blue_sources:
        response += f"\t{src.source_name.capitalize()} - "
        success = src.update_cache()
        if success:
            response += "exito\n"
            logging.info("Success updating %s values", src.source_name)
        else:
            response += "fallo\n"
            logging.info("Failure updating %s values", src.source_name)

    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            parse_mode=telegram.ParseMode.MARKDOWN
    )
