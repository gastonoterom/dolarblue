from typing import Any, Callable
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from src.public_interfaces.telegram_bot.config import ALLOWED_CHAT_ID


def authorized_only(
    command_handler: Callable[[Update, CallbackContext], None]
) -> Callable[..., Any]:
    """Decorator for command routes in telegram that only the bot admin can access.

    For example if a critical command should not be executed,
    decorate the function of its handling with this. Decorated function must have
    update: Update and context: CallbackContext as arguments."""

    def check_access(update: Update, context: CallbackContext) -> None:
        if ALLOWED_CHAT_ID is None or update.effective_chat is None:
            raise TypeError(
                "ALLOWED_CHAT_ID and effective_chat_id CANT BE NONE")

        if update.effective_chat.id != ALLOWED_CHAT_ID:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Peticion denegada.",
            )

            return

        command_handler(update, context)

    return check_access
