"""Sends a dolarblue updated report to the admin in telegram."""

import logging
from datetime import datetime
from typing import Dict

import telegram
from telegram import Bot
from src.pub_sub.subscribers.update_values_sub import subscribe_to_cache_updated
from src.public_interfaces.telegram_bot.config import  ADMIN_CHAT_ID


@subscribe_to_cache_updated
def send_dolarblue_report(bot: Bot, report: Dict[str, bool]) -> None:
    logging.info("Sending report via telegram")

    parsed_date = datetime.now().strftime("%m-%d-%Y %H:%M")
    response = f"Cotizaciones actualizadas - {parsed_date}\n"

    for src, success in report.items():
        response += f"  \t{src.capitalize()} - "
        response += "exito\n" if success else "fallo\n"

    bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=response,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
