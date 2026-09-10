from reminders.domain.api.pending_reminders_service import PendingRemindersService
from reminders.domain.model.reminder import Reminder
from reminders.domain.spi.reminder_repository_port import ReminderRepositoryPort


class PendingRemindersUsecase(PendingRemindersService):
    def __init__(self, repository_port: ReminderRepositoryPort) -> None:
        self._repository_port = repository_port

    async def get_pending_reminders(self) -> list[Reminder]:
        return await self._repository_port.get_pending()
