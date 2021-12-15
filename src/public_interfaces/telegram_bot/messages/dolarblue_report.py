"""Sends a dolarblue updated report to the admin in telegram."""

import logging
from datetime import datetime
import telegram
from telegram import Bot
from src.pub_sub.subscribers.update_values_sub import dolarblue_cache_updated
from src.public_interfaces.telegram_bot.config import ALLOWED_CHAT_ID, ADMIN_CHAT_ID


def send_dolarblue_report(bot: Bot) -> None:
    """Subscribes the report handler to the values-updated event in pubsub
    to send the report to the admin when the process is finished."""

    def handle_report(report: dict[str, bool]) -> None:
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

    dolarblue_cache_updated(
        handler=handle_report
    )
