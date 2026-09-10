from datetime import datetime
from typing import Protocol

from reminders.domain.model.reminder import Reminder


class ReminderRepositoryPort(Protocol):
    """Outbound port for persisting and retrieving reminders."""

    async def create_reminder(
        self, chat_id: int, user_id: int, username: str, message: str, remind_at: datetime
    ) -> Reminder: ...

    async def get_pending(self) -> list[Reminder]: ...

    async def try_fire(self, reminder_id: int) -> Reminder | None: ...
