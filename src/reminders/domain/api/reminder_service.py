from typing import Protocol

from reminders.domain.model.parsed_reminder import ParsedReminder
from reminders.domain.model.reminder import Reminder


class ReminderService(Protocol):
    """Inbound port for the reminders feature: schedules (persists) a reminder."""

    async def schedule_reminder(self, chat_id: int, user_id: int, username: str, parsed: ParsedReminder) -> Reminder: ...
