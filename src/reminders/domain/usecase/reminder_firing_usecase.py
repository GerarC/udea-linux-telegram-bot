from reminders.domain.api.reminder_firing_service import ReminderFiringService
from reminders.domain.model.reminder import Reminder
from reminders.domain.spi.reminder_repository_port import ReminderRepositoryPort


class ReminderFiringUsecase(ReminderFiringService):
    def __init__(self, repository_port: ReminderRepositoryPort) -> None:
        self._repository_port = repository_port

    async def fire_reminder(self, reminder_id: int) -> Reminder | None:
        return await self._repository_port.try_fire(reminder_id)
