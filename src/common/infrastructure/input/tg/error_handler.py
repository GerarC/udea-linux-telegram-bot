import logging

from telegram import Update
from telegram.ext import ContextTypes

from common.domain.error.domain_error import DomainError

# NOTE: user-facing text in Spanish, the bot serves a Spanish-speaking group.
GENERIC_ERROR_MESSAGE = "Algo salió mal procesando eso 😵‍💫. Intenta de nuevo en un momento."


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global handler for exceptions raised by any Telegram handler."""
    error = context.error
    chat_id = update.effective_chat.id if isinstance(update, Update) and update.effective_chat else None
    log_extra = {"event": "handler_exception", "chat_id": chat_id, "error_type": type(error).__name__}

    is_domain_error = isinstance(error, DomainError) and error.user_message
    if is_domain_error:
        logging.warning("Domain error while processing update: %s", error, extra=log_extra)
    else:
        logging.error("Unhandled exception while processing update", exc_info=error, extra=log_extra)

    if not (isinstance(update, Update) and update.effective_message is not None):
        return

    user_message = error.user_message if is_domain_error else GENERIC_ERROR_MESSAGE
    await update.effective_message.reply_text(user_message)
