import inspect
from typing import Callable
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from src.libs.scraping.utils import MethodNotCompatibleError
from src.public_interfaces.telegram_bot.config import ALLOWED_CHAT_ID


def authorized_only(command_handler: Callable[[Update, CallbackContext], None]):
    """Decorator for command routes in telegram that only the bot admin can access.

    For example if a critical command should not be executed, decorate the function of its handling with this.
    Decorated function must have update: Update and context: CallbackContext as arguments."""

    # Inspect the function to see if it is compatible
    inspected_handler = inspect.getfullargspec(command_handler)

    handler_has_update = "update" in inspected_handler.args and \
                         inspected_handler.annotations.get("update") == Update

    handler_has_context = "context" in inspected_handler.args and \
                          inspected_handler.annotations.get("context") == CallbackContext

    if (handler_has_update and handler_has_context) is not True:
        raise MethodNotCompatibleError("Decorated function is incompatible:\
        it has no valid update and context arguments")

    def check_access(update: Update, context: CallbackContext) -> None:

        if ALLOWED_CHAT_ID is not None or update.effective_chat is not None:
            raise TypeError("ALLOWED_CHAT_ID and effective chat id CANT BE NONE")

        if update.effective_chat.id != ALLOWED_CHAT_ID:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Peticion denegada.",
            )

            return

        command_handler(update, context)

    return check_access
