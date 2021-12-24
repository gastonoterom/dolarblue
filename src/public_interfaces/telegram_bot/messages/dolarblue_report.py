import logging
from datetime import datetime
from typing import Dict, Optional
import telegram
from telegram import Bot
from src.classes.dolar_blue import DolarBlue
from src.pub_sub.subscribers.update_values_sub import subscribe_to_cache_updated
from src.public_interfaces.telegram_bot.config import ADMIN_CHAT_ID


@subscribe_to_cache_updated
def send_dolarblue_report(bot: Bot, report: Dict[str, Optional[DolarBlue]]) -> None:
    """When called sends a report of the updated dolarblue sources to the bot master.

    The bot master chat id is defined in the config.py of the module"""

    logging.info("Sending report via telegram")

    parsed_date = datetime.now().strftime("%m-%d-%Y %H:%M")
    response = f"Cotizaciones actualizadas - {parsed_date}\n"

    for src, dolarblue in report.items():
        response += f"      {src.capitalize()} - "
        response += "exito\n" if dolarblue else "fallo\n"

    bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=response,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
