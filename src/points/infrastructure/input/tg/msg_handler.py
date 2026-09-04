import html

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.constants import ParseMode
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from points.domain.api.points_service import PointsService
from points.domain.model.ranking_entry import RankingEntry

RANK_EMOJI_LEVELS = ("🧠🧠🧠", "🧠🧠", "🧠")


def _display_name(user) -> str:
    return f"@{user.username}" if user.username else user.full_name


def _format_ranking(ranking: list[RankingEntry]) -> str:
    lines = ["🏆 <b>Ranking de Autismo del grupo</b>", ""]
    for position, entry in enumerate(ranking, start=1):
        badge = RANK_EMOJI_LEVELS[position - 1] if position <= len(RANK_EMOJI_LEVELS) else ""
        user_points = entry.user_points
        name = html.escape(f"@{user_points.username}" if user_points.username else str(user_points.user_id))
        level = html.escape(entry.level_label)
        line = f"{position}. {name} — {user_points.points} Autispuntos ({level})"
        lines.append(f"{line} {badge}".rstrip())
    return "\n".join(lines)


@inject
async def grant_points_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    points_service: PointsService = Provide[ApplicationContainer.points.usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    if message.reply_to_message is None or message.reply_to_message.from_user is None:
        await message.reply_text("Responde (reply) al mensaje de la persona a quien le quieres dar Autispuntos.")
        return

    if not context.args:
        await message.reply_text("Uso: responde al mensaje de la persona con /autispuntos +3 (o -3).")
        return

    try:
        amount = int(context.args[0])
    except ValueError:
        await message.reply_text("La cantidad debe ser un número, ej: /autispuntos +3")
        return

    granter = update.effective_user
    target = message.reply_to_message.from_user
    chat_id = message.chat_id

    try:
        member = await context.bot.get_chat_member(chat_id, granter.id)
    except TelegramError:
        await message.reply_text("No pude verificar si eres admin del grupo. Intenta de nuevo en un momento.")
        return
    granter_is_admin = member.status in ("administrator", "creator")

    result = await points_service.grant_points(
        chat_id=chat_id,
        granter_is_admin=granter_is_admin,
        target_id=target.id,
        target_username=target.username or target.full_name,
        amount=amount,
    )

    if result is None:
        await message.reply_text("Solo los admins pueden otorgar Autispuntos.")
        return

    granter_name = html.escape(_display_name(granter))
    target_name = html.escape(_display_name(target))
    verb = "le ha otorgado" if amount >= 0 else "le ha quitado"
    amount_text = f"+{amount}" if amount >= 0 else str(abs(amount))

    text_body = (
        f"🧠 {granter_name} {verb} {amount_text} Autispuntos a {target_name}.\n\n"
        f"{target_name} ahora tiene {result.target.points} Autispuntos.\n"
        f"Nivel de autismo: {html.escape(result.level_label)}.\n\n"
        f"{_format_ranking(result.ranking)}"
    )
    await message.reply_text(text_body, parse_mode=ParseMode.HTML)


@inject
async def ranking_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    points_service: PointsService = Provide[ApplicationContainer.points.usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    ranking = await points_service.get_ranking(message.chat_id)
    if not ranking:
        await message.reply_text("Todavía nadie tiene Autispuntos en este grupo.")
        return

    await message.reply_text(_format_ranking(ranking), parse_mode=ParseMode.HTML)


@inject
async def my_points_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    points_service: PointsService = Provide[ApplicationContainer.points.usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    target = message.reply_to_message.from_user if message.reply_to_message else update.effective_user
    if target is None:
        return

    entry = await points_service.get_points(
        chat_id=message.chat_id,
        user_id=target.id,
        username=target.username or target.full_name,
    )
    name = html.escape(_display_name(target))
    level = html.escape(entry.level_label)
    text_body = f"{name} tiene {entry.user_points.points} Autispuntos.\nNivel de autismo: {level}."
    await message.reply_text(text_body, parse_mode=ParseMode.HTML)
