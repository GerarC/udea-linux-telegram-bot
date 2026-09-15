import html
import logging
import random

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from confessions.domain.api.confession_deletion_service import ConfessionDeletionService
from confessions.domain.api.confession_listing_service import ConfessionListingService
from confessions.domain.api.confession_submission_service import ConfessionSubmissionService
from confessions.domain.model.confession import Confession

logger = logging.getLogger(__name__)

USAGE_TEXT = "Uso: /confesar <texto> (entre 15 y 500 caracteres)."

# NOTE: user-facing flavor text in Spanish - the bot serves a Spanish-speaking group.
CONFESSION_TITLES = (
    ("🕯️", "Confesión anónima", "Enviado desde las profundidades del /dev/null"),
    ("🩸", "Confesión del abismo", "El universo decidió que esto debía saberse"),
    ("🧠", "Confesión residual", "Transmitido anónimamente"),
)


def _format_confession(confession: Confession) -> str:
    emoji, title, footer = random.choice(CONFESSION_TITLES)
    content = html.escape(confession.content)
    return f"{emoji} <b>{title} #{confession.id}</b>\n\n" f'"{content}"\n\n' f"— {footer}"


@inject
async def confesar_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    submission_service: ConfessionSubmissionService = Provide[
        ApplicationContainer.confessions.confession_submission_usecase
    ],
) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None:
        return

    if not context.args:
        await message.reply_text(USAGE_TEXT)
        return

    content = " ".join(context.args)
    username = user.username or user.full_name

    confession = await submission_service.submit_confession(message.chat_id, user.id, username, content)

    logger.info(
        "Confession submitted",
        extra={"event": "confession_submitted", "chat_id": message.chat_id, "confession_id": confession.id},
    )

    await context.bot.send_message(message.chat_id, _format_confession(confession), parse_mode=ParseMode.HTML)

    try:
        await message.delete()
    except TelegramError:
        # NOTE: deleting the /confesar message needs the bot to be a group admin with
        # delete rights - not fatal, but the confession stops being anonymous without it
        # since the original message still shows the author's name.
        logger.warning(
            "Could not delete /confesar command message",
            extra={"event": "confession_message_delete_failed", "chat_id": message.chat_id},
        )


@inject
async def confesiones_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    listing_service: ConfessionListingService = Provide[ApplicationContainer.confessions.confession_listing_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    confessions = await listing_service.list_confessions(message.chat_id)
    if not confessions:
        await message.reply_text("Todavía no hay confesiones en este grupo.")
        return

    logger.info(
        "Confessions listed", extra={"event": "confessions_listed", "chat_id": message.chat_id}
    )

    text = "\n\n".join(_format_confession(confession) for confession in confessions)
    await message.reply_html(text)


@inject
async def borrar_confesion_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    deletion_service: ConfessionDeletionService = Provide[
        ApplicationContainer.confessions.confession_deletion_usecase
    ],
) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None:
        return

    if not context.args:
        await message.reply_text("Uso: /borrar_confesion <id>")
        return

    try:
        confession_id = int(context.args[0])
    except ValueError:
        await message.reply_text("El id debe ser un número, ej: /borrar_confesion 142")
        return

    chat_id = message.chat_id

    try:
        member = await context.bot.get_chat_member(chat_id, user.id)
    except TelegramError:
        await message.reply_text("No pude verificar si eres admin del grupo. Intenta de nuevo en un momento.")
        return
    requester_is_admin = member.status in ("administrator", "creator")

    result = await deletion_service.delete_confession(chat_id, confession_id, requester_is_admin)

    if result is None:
        await message.reply_text("Solo los admins pueden borrar confesiones.")
        return

    logger.info(
        "Confession deleted",
        extra={"event": "confession_deleted", "chat_id": chat_id, "confession_id": confession_id},
    )
    await message.reply_text(f"🗑️ Confesión #{confession_id} borrada.")
