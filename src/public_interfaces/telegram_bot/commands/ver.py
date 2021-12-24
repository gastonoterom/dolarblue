"""Handler for bot command ver_valores."""

from telegram import Update
import telegram
from telegram.ext import CallbackContext
from src.classes import DolarBlueUtils


def ver(update: Update, context: CallbackContext) -> None:
    """Handles the ver bot command, which sends the average dolarblue value"""

    dolarblue = DolarBlueUtils.get_average().get_cached_blue()

    assert update.effective_chat is not None and dolarblue is not None

    parsed_date = dolarblue.date_time.strftime("%d-%m-%Y %H:%M")

    dolarblue_values = f"""Valor actual\n{parsed_date}\n
Compra: {dolarblue.buy_price}
Venta: {dolarblue.sell_price}
Promedio: {dolarblue.average}"""

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dolarblue_values,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
