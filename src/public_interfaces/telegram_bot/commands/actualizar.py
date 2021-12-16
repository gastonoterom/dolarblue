from datetime import datetime
import logging
from telegram import Update
import telegram
from telegram.ext import CallbackContext
from src.classes import DolarBlueSource
from src.pub_sub.publishers.update_values_pub import pub_update_values
from src.public_interfaces.telegram_bot.commands_middlewares.authorized_only import authorized_only


@authorized_only
def actualizar(update: Update, context: CallbackContext) -> None:
    """Handles the /actualizar bot command, which publishes a request to update all the dolarblue cached values

    FOR ADMINS ONLY, critical operation"""

    assert update.effective_chat is not None

    # Publish an update-values request
    pub_update_values()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Actualizando valores de dolar blue.",
        parse_mode=telegram.ParseMode.MARKDOWN
    )
