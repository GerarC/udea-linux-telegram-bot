import html
import logging

from dependency_injector.wiring import Provide, inject
from telegram import Message, Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from banter.domain.api.add_compliment_service import AddComplimentService
from banter.domain.api.add_insult_service import AddInsultService
from banter.domain.api.compliment_service import ComplimentService
from banter.domain.api.insult_service import InsultService
from banter.domain.api.target_resolver_service import TargetResolverService
from common.application.bootstrap.container import ApplicationContainer

logger = logging.getLogger(__name__)


async def _resolve_target(
    message: Message,
    context: ContextTypes.DEFAULT_TYPE,
    target_resolver_service: TargetResolverService,
) -> tuple[str, int | None, str] | None:
    # NOTE: reply-to-message takes priority over a typed @username, since it
    # unambiguously identifies a real Telegram user instead of a lookup that can miss.
    reply_user = message.reply_to_message.from_user if message.reply_to_message else None
    if reply_user is not None:
        raw_username = reply_user.username or reply_user.full_name
        display_name = f"@{reply_user.username}" if reply_user.username else reply_user.full_name
        return display_name, reply_user.id, raw_username

    if not context.args:
        return None

    typed_username = " ".join(context.args).lstrip("@")
    target_id = await target_resolver_service.resolve(message.chat_id, typed_username)
    if target_id is None:
        # NOTE: a lookup miss doesn't fail the command - the insult/halago still goes
        # out using the typed text, it just can't be counted in banter_stats.
        logger.warning(
            "Banter target not found in group_members",
            extra={"event": "banter_target_not_found", "chat_id": message.chat_id, "typed_username": typed_username},
        )
    return f"@{typed_username}", target_id, typed_username


async def _requester_is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, message: Message) -> bool | None:
    user = update.effective_user
    if user is None:
        return None

    try:
        member = await context.bot.get_chat_member(message.chat_id, user.id)
    except TelegramError:
        await message.reply_text("No pude verificar si eres admin del grupo. Intenta de nuevo en un momento.")
        return None
    return member.status in ("administrator", "creator")


@inject
async def insultar_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    insult_service: InsultService = Provide[ApplicationContainer.banter.insult_usecase],
    target_resolver_service: TargetResolverService = Provide[ApplicationContainer.banter.target_resolver_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    resolved = await _resolve_target(message, context, target_resolver_service)
    if resolved is None:
        await message.reply_text("Usa: /insultar @usuario, o responde (reply) al mensaje de la persona.")
        return
    display_name, target_id, raw_username = resolved

    insulto = await insult_service.insult(message.chat_id, target_id, raw_username)
    logger.info(
        "Insult sent",
        extra={"event": "insult_sent", "chat_id": message.chat_id, "target": display_name},
    )
    await message.reply_html(f"{html.escape(display_name)}, {html.escape(insulto)}")


@inject
async def halagar_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    compliment_service: ComplimentService = Provide[ApplicationContainer.banter.compliment_usecase],
    target_resolver_service: TargetResolverService = Provide[ApplicationContainer.banter.target_resolver_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    resolved = await _resolve_target(message, context, target_resolver_service)
    if resolved is None:
        await message.reply_text("Usa: /halagar @usuario, o responde (reply) al mensaje de la persona.")
        return
    display_name, target_id, raw_username = resolved

    halago = await compliment_service.compliment(message.chat_id, target_id, raw_username)
    logger.info(
        "Compliment sent",
        extra={"event": "compliment_sent", "chat_id": message.chat_id, "target": display_name},
    )
    await message.reply_html(f"{html.escape(display_name)}, {html.escape(halago)}")


@inject
async def agregar_insulto_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    add_insult_service: AddInsultService = Provide[ApplicationContainer.banter.add_insult_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    if not context.args:
        await message.reply_text("Uso: /agregar_insulto frase del insulto")
        return

    requester_is_admin = await _requester_is_admin(update, context, message)
    if requester_is_admin is None:
        return

    phrase = " ".join(context.args)
    added = await add_insult_service.add(message.chat_id, requester_is_admin, phrase)
    if not added:
        await message.reply_text("Solo los admins pueden agregar insultos.")
        return

    logger.info("Insult added", extra={"event": "insult_added", "chat_id": message.chat_id})
    await message.reply_text("Insulto agregado.")


@inject
async def agregar_halago_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    add_compliment_service: AddComplimentService = Provide[ApplicationContainer.banter.add_compliment_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    if not context.args:
        await message.reply_text("Uso: /agregar_halago frase del halago")
        return

    requester_is_admin = await _requester_is_admin(update, context, message)
    if requester_is_admin is None:
        return

    phrase = " ".join(context.args)
    added = await add_compliment_service.add(message.chat_id, requester_is_admin, phrase)
    if not added:
        await message.reply_text("Solo los admins pueden agregar halagos.")
        return

    logger.info("Compliment added", extra={"event": "compliment_added", "chat_id": message.chat_id})
    await message.reply_text("Halago agregado.")
