from datetime import UTC, datetime, timedelta

from reminders.domain.api.reminder_service import ReminderService
from reminders.domain.model.parsed_reminder import ParsedReminder
from reminders.domain.model.reminder import Reminder
from reminders.domain.spi.reminder_repository_port import ReminderRepositoryPort


class ReminderUsecase(ReminderService):
    def __init__(self, repository_port: ReminderRepositoryPort) -> None:
        self._repository_port = repository_port

    async def schedule_reminder(self, chat_id: int, user_id: int, username: str, parsed: ParsedReminder) -> Reminder:
        remind_at = datetime.now(UTC) + timedelta(minutes=parsed.minutes)
        return await self._repository_port.create_reminder(
            chat_id=chat_id,
            user_id=user_id,
            username=username,
            message=parsed.message,
            remind_at=remind_at,
        )
