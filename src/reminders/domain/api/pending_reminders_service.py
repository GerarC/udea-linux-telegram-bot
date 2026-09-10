from typing import Protocol

from reminders.domain.model.reminder import Reminder


class PendingRemindersService(Protocol):
    """Inbound port for the reminders feature: lists reminders still to be fired."""

    async def get_pending_reminders(self) -> list[Reminder]: ...
