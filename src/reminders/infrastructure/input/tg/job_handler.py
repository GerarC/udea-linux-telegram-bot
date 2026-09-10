from dependency_injector.wiring import Provide, inject
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from reminders.domain.api.reminder_firing_service import ReminderFiringService


@inject
async def fire_reminder_job(
    context: ContextTypes.DEFAULT_TYPE,
    reminder_firing_service: ReminderFiringService = Provide[ApplicationContainer.reminders.reminder_firing_usecase],
) -> None:
    reminder_id = context.job.data["reminder_id"]
    reminder = await reminder_firing_service.fire_reminder(reminder_id)
    if reminder is None:
        return
    await context.bot.send_message(reminder.chat_id, f"⏰ Recordatorio: {reminder.message}")
