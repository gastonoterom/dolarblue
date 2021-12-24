"""Handler for bot command ver_valores."""

from telegram import Update
import telegram
from telegram.ext import CallbackContext
from src.classes import DolarBlueUtils


def fuentes(update: Update, context: CallbackContext) -> None:
    """Handles the fuentes bot command, which sends the user all the dolarblue cached values"""

    dolarblue_values = "Fuentes:\n\n"

    for dolarblue in DolarBlueUtils.get_all_dolarblue_values():
        parsed_date = dolarblue.date_time.strftime("%m-%d-%Y %H:%M")

        dolarblue_values += f"*{dolarblue.source.source_name.capitalize()}* - {parsed_date}\n\
            \tcompra: {dolarblue.buy_price}\n\
            \tventa: {dolarblue.sell_price}\n\
            \tpromedio: {dolarblue.average}\n\n"

    assert update.effective_chat is not None

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dolarblue_values,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
