import html
import logging

from dependency_injector.wiring import Provide, inject
from telegram import Message, Update
from telegram.ext import ContextTypes

from banter.domain.api.compliment_service import ComplimentService
from banter.domain.api.insult_service import InsultService
from common.application.bootstrap.container import ApplicationContainer

logger = logging.getLogger(__name__)


def _resolve_target(message: Message, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    # NOTE: reply-to-message takes priority over a plain text mention, since it
    # unambiguously identifies a real Telegram user instead of arbitrary typed text.
    reply_user = message.reply_to_message.from_user if message.reply_to_message else None
    if reply_user is not None:
        return f"@{reply_user.username}" if reply_user.username else reply_user.full_name
    if context.args:
        return " ".join(context.args)
    return None


@inject
async def insultar_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    insult_service: InsultService = Provide[ApplicationContainer.banter.insult_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    usuario = _resolve_target(message, context)
    if usuario is None:
        await message.reply_text("Usa: /insultar @usuario, o responde (reply) al mensaje de la persona.")
        return

    insulto = await insult_service.insult()
    logger.info(
        "Insult sent",
        extra={"event": "insult_sent", "chat_id": message.chat_id, "target": usuario},
    )
    await message.reply_html(f"{html.escape(usuario)}, {html.escape(insulto)}")


@inject
async def cumplido_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    compliment_service: ComplimentService = Provide[ApplicationContainer.banter.compliment_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    usuario = _resolve_target(message, context)
    if usuario is None:
        await message.reply_text("Usa: /cumplido @usuario, o responde (reply) al mensaje de la persona.")
        return

    cumplido = await compliment_service.compliment()
    logger.info(
        "Compliment sent",
        extra={"event": "compliment_sent", "chat_id": message.chat_id, "target": usuario},
    )
    await message.reply_html(f"{html.escape(usuario)}, {html.escape(cumplido)}")
