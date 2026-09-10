import logging
from zoneinfo import ZoneInfo

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from reminders.domain.api.reminder_parser_service import ReminderParserService
from reminders.domain.api.reminder_service import ReminderService
from reminders.domain.utils.constants import TIMEZONE, USAGE_EXAMPLE
from reminders.infrastructure.input.tg.job_handler import fire_reminder_job

logger = logging.getLogger(__name__)


@inject
async def recordar_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    reminder_parser_service: ReminderParserService = Provide[ApplicationContainer.reminders.reminder_parser_usecase],
    reminder_service: ReminderService = Provide[ApplicationContainer.reminders.reminder_usecase],
) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None:
        return

    if not context.args:
        await message.reply_text(USAGE_EXAMPLE)
        return

    raw_text = " ".join(context.args)
    parsed = reminder_parser_service.parse(raw_text)

    username = user.username or user.full_name
    reminder = await reminder_service.schedule_reminder(message.chat_id, user.id, username, parsed)

    context.job_queue.run_once(
        fire_reminder_job,
        when=parsed.minutes * 60,
        data={"reminder_id": reminder.id},
        name=f"reminder:{reminder.id}",
    )

    logger.info(
        "Reminder scheduled",
        extra={
            "event": "reminder_scheduled",
            "chat_id": message.chat_id,
            "user_id": user.id,
            "reminder_id": reminder.id,
            "minutes": parsed.minutes,
        },
    )

    local_time = reminder.remind_at.astimezone(ZoneInfo(TIMEZONE)).strftime("%d/%m %H:%M")
    await message.reply_text(f"⏰ Listo, te lo recuerdo el {local_time} (hora Colombia).")
