from typing import Protocol

from reminders.domain.model.reminder import Reminder


class ReminderFiringService(Protocol):
    """Inbound port for the reminders feature: atomically fires a due reminder."""

    async def fire_reminder(self, reminder_id: int) -> Reminder | None: ...
