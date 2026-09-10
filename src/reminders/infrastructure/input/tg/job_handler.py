import logging

from dependency_injector.wiring import Provide, inject
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from reminders.domain.api.reminder_firing_service import ReminderFiringService

logger = logging.getLogger(__name__)


@inject
async def fire_reminder_job(
    context: ContextTypes.DEFAULT_TYPE,
    reminder_firing_service: ReminderFiringService = Provide[ApplicationContainer.reminders.reminder_firing_usecase],
) -> None:
    reminder_id = context.job.data["reminder_id"]
    reminder = await reminder_firing_service.fire_reminder(reminder_id)
    if reminder is None:
        logger.info("Reminder already fired, skipping", extra={"event": "reminder_skip", "reminder_id": reminder_id})
        return

    logger.info(
        "Reminder fired",
        extra={"event": "reminder_fired", "chat_id": reminder.chat_id, "reminder_id": reminder.id},
    )
    await context.bot.send_message(reminder.chat_id, f"⏰ Recordatorio: {reminder.message}")
