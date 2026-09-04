import html

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from activity.domain.api.activity_service import ActivityService
from activity.domain.model.monthly_ranking_entry import MonthlyRankingEntry
from activity.domain.model.user_activity import UserActivity
from common.application.bootstrap.container import ApplicationContainer

USAGE_TEXT = "Uso: /mas_desocupados [mes|total] (sin argumento muestra ambos)"


def _display_name(user_id: int, username: str) -> str:
    return f"@{username}" if username else str(user_id)


def _movement_badge(entry: MonthlyRankingEntry) -> str:
    if entry.previous_position is None:
        return "🆕"
    if entry.previous_position > entry.position:
        return "🔼"
    if entry.previous_position < entry.position:
        return "🔽"
    return "➖"


def _format_monthly(entries: list[MonthlyRankingEntry]) -> str:
    if not entries:
        return "🗓️ <b>Top desocupados del mes</b>\n\nTodavía no hay mensajes registrados este mes."
    lines = ["🗓️ <b>Top desocupados del mes</b>", ""]
    for entry in entries:
        name = html.escape(_display_name(entry.activity.user_id, entry.activity.username))
        lines.append(f"{entry.position}. {name} — {entry.activity.message_count} mensajes {_movement_badge(entry)}")
    return "\n".join(lines)


def _format_all_time(entries: list[UserActivity]) -> str:
    if not entries:
        return "🏆 <b>Top desocupados de todo el tiempo</b>\n\nTodavía no hay mensajes registrados en este grupo."
    lines = ["🏆 <b>Top desocupados de todo el tiempo</b>", ""]
    for position, entry in enumerate(entries, start=1):
        name = html.escape(_display_name(entry.user_id, entry.username))
        lines.append(f"{position}. {name} — {entry.message_count} mensajes")
    return "\n".join(lines)


@inject
async def track_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    activity_service: ActivityService = Provide[ApplicationContainer.activity.usecase],
) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None or not message.text:
        return

    await activity_service.register_message(message.chat_id, user.id, user.username or user.full_name)


@inject
async def most_inactive_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    activity_service: ActivityService = Provide[ApplicationContainer.activity.usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    scope = context.args[0].lower() if context.args else None
    if scope not in (None, "mes", "total"):
        await message.reply_text(USAGE_TEXT)
        return

    sections = []
    if scope in (None, "mes"):
        sections.append(_format_monthly(await activity_service.get_monthly_ranking(message.chat_id)))
    if scope in (None, "total"):
        sections.append(_format_all_time(await activity_service.get_all_time_ranking(message.chat_id)))

    await message.reply_text("\n\n".join(sections), parse_mode=ParseMode.HTML)
