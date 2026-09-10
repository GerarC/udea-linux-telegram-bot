import logging

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from polls.domain.api.poll_parser_service import PollParserService
from polls.domain.api.poll_recorder_service import PollRecorderService

logger = logging.getLogger(__name__)

USAGE_TEXT = "Uso: /encuesta pregunta | opción1 | opción2 [| opción3 ...] (2 a 10 opciones)"


@inject
async def encuesta_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    poll_parser_service: PollParserService = Provide[ApplicationContainer.polls.parser_usecase],
    poll_recorder_service: PollRecorderService = Provide[ApplicationContainer.polls.recorder_usecase],
) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None or not message.text:
        return

    _, _, raw = message.text.partition(" ")
    if not raw.strip():
        await message.reply_text(USAGE_TEXT)
        return

    poll = poll_parser_service.parse_poll(raw)
    await context.bot.send_poll(
        chat_id=message.chat_id,
        question=poll.question,
        options=poll.options,
        is_anonymous=False,
        allows_multiple_answers=False,
    )
    await poll_recorder_service.record_poll(message.chat_id, user.id, user.username or user.full_name, poll.question)
    logger.info(
        "Poll created",
        extra={
            "event": "poll_created",
            "chat_id": message.chat_id,
            "user_id": user.id,
            "option_count": len(poll.options),
        },
    )

    try:
        await message.delete()
    except TelegramError:
        # NOTE: deleting another user's message needs the bot to be a group admin
        # with delete rights - not fatal, the poll itself was already created fine.
        logging.warning(
            "Could not delete /encuesta command message",
            extra={"event": "poll_message_delete_failed", "chat_id": message.chat_id},
        )
