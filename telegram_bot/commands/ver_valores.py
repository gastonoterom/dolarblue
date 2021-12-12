"""Handler for bot command ver_valores."""

from telegram import Update
from telegram.ext import CallbackContext
from classes.dolar_blue_sources.all_sources import all_dolar_blue_sources

def ver_valores(update: Update, context: CallbackContext):
    """Handles the ver_valores bot command, which sends the user all the dolarblue cached values"""

    dolarblue_values = "Cotizaciones de dolar blue obtenidas:\n\n"

    for src in all_dolar_blue_sources:
        value = src.get_cached_blue()
        if value:
            dolarblue_values += f"**{src.source_name.capitalize()}:** - {value.date_time}\n\
            \tcompra: {value.buy_price}\n\
            \tventa: {value.sell_price}\n\
            \tpromedio: {value.average}\n\n"

    assert update.effective_chat is not None

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dolarblue_values
    )
