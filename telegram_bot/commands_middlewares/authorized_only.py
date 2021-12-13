"""Middleware function for authorized only bot commands."""

import logging
from typing import Callable
import os
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

def authorized_only(command_handler: Callable[[Update, CallbackContext], None]):
    """Authorized only decorator"""
    def check_access(update: Update, context: CallbackContext) -> None:
        """Decorator function for authorized-only bot commands."""
        allowed_chat_id = os.environ.get("ALLOWED_CHAT_ID")

        assert allowed_chat_id is not None
        assert update.effective_chat is not None

        if update.effective_chat.id != int(allowed_chat_id):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Peticion denegada.",
            )

            return

        command_handler(update, context)

    return check_access
