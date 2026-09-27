from datetime import datetime

from reminders.domain.model.reminder import Reminder
from reminders.domain.spi.reminder_repository_port import ReminderRepositoryPort


class FakeReminderRepository(ReminderRepositoryPort):
    def __init__(self) -> None:
        self.created: list[Reminder] = []
        self._next_id = 1

    async def create_reminder(
        self, chat_id: int, user_id: int, username: str, message: str, remind_at: datetime
    ) -> Reminder:
        reminder = Reminder(
            id=self._next_id, chat_id=chat_id, user_id=user_id, message=message, remind_at=remind_at, fired=False
        )
        self._next_id += 1
        self.created.append(reminder)
        return reminder

    async def get_pending(self) -> list[Reminder]:
        return [reminder for reminder in self.created if not reminder.fired]

    async def try_fire(self, reminder_id: int) -> Reminder | None:
        for reminder in self.created:
            if reminder.id == reminder_id and not reminder.fired:
                reminder.fired = True
                return reminder
        return None
