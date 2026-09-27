import html
import logging

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from activity.domain.api.activity_service import ActivityService
from activity.domain.api.all_time_ranking_service import AllTimeRankingService
from activity.domain.api.group_stats_service import GroupStatsService
from activity.domain.api.monthly_history_service import MonthlyHistoryService
from activity.domain.api.monthly_ranking_service import MonthlyRankingService
from activity.domain.model.group_stats import GroupStats
from activity.domain.model.monthly_ranking_entry import MonthlyRankingEntry
from activity.domain.model.user_activity import UserActivity
from activity.domain.utils.constants import WEEKDAY_LABELS
from activity.infrastructure.input.tg.chart_renderer import render_monthly_activity_chart
from common.application.bootstrap.container import ApplicationContainer

logger = logging.getLogger(__name__)

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


def _stat_line(label: str, value: str) -> str:
    return f"<b>{label}:</b> {value}"


def _bold_before_colon(line: str) -> str:
    # NOTE: extra_lines come from other features as plain "Label: value" strings
    # (see GroupStatsProviderPort) - escape first, then bold the label up to the
    # first colon so they read consistently with this feature's own stat lines.
    escaped = html.escape(line)
    label, sep, value = escaped.partition(": ")
    return f"<b>{label}:</b> {value}" if sep else escaped


def _format_group_stats(stats: GroupStats) -> str:
    lines = [
        "📊 <b>Estadísticas del grupo</b>",
        "",
        _stat_line("Mensajes este mes", f"{stats.messages_this_month:,}"),
        _stat_line("Mensajes en total", f"{stats.messages_all_time:,}"),
        _stat_line("Participantes activos este mes", str(stats.active_participants_this_month)),
    ]

    if stats.top_user_this_month is not None:
        top = stats.top_user_this_month
        name = html.escape(_display_name(top.user_id, top.username))
        lines.append(_stat_line("Más activo del mes", f"{name} ({top.message_count} mensajes)"))

    if stats.peak_hour is not None:
        lines.append(_stat_line("Hora pico", f"{stats.peak_hour:02d}:00 – {(stats.peak_hour + 1) % 24:02d}:00"))

    if stats.peak_weekday is not None:
        lines.append(_stat_line("Día más activo", WEEKDAY_LABELS[stats.peak_weekday]))

    if stats.extra_lines:
        lines.append("")
        lines.append("<b>Otros datos</b>")
        for extra_line in stats.extra_lines:
            lines.extend(f"• {_bold_before_colon(sub_line)}" for sub_line in extra_line.split("\n"))

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
    monthly_ranking_service: MonthlyRankingService = Provide[ApplicationContainer.activity.monthly_ranking_usecase],
    all_time_ranking_service: AllTimeRankingService = Provide[ApplicationContainer.activity.all_time_ranking_usecase],
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
        sections.append(_format_monthly(await monthly_ranking_service.get_monthly_ranking(message.chat_id)))
    if scope in (None, "total"):
        sections.append(_format_all_time(await all_time_ranking_service.get_all_time_ranking(message.chat_id)))

    logger.info(
        "Most inactive ranking viewed",
        extra={"event": "most_inactive_viewed", "chat_id": message.chat_id, "scope": scope},
    )
    await message.reply_text("\n\n".join(sections), parse_mode=ParseMode.HTML)


@inject
async def group_stats_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_stats_service: GroupStatsService = Provide[ApplicationContainer.activity.group_stats_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    stats = await group_stats_service.get_group_stats(message.chat_id)
    if stats.messages_all_time == 0:
        await message.reply_text("Todavía no hay mensajes registrados en este grupo.")
        return

    logger.info("Group stats viewed", extra={"event": "group_stats_viewed", "chat_id": message.chat_id})
    await message.reply_text(_format_group_stats(stats), parse_mode=ParseMode.HTML)


@inject
async def actividad_grupo_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    monthly_history_service: MonthlyHistoryService = Provide[ApplicationContainer.activity.monthly_history_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    history = await monthly_history_service.get_monthly_history(message.chat_id)
    if not any(entry.message_count for entry in history):
        await message.reply_text("Todavía no hay actividad registrada en este grupo.")
        return

    logger.info(
        "Group monthly activity chart viewed",
        extra={"event": "monthly_activity_viewed", "chat_id": message.chat_id},
    )
    chart = render_monthly_activity_chart(history)
    await message.reply_photo(photo=chart, caption="📈 Actividad del grupo en los últimos 6 meses")
