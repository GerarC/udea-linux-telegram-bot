from reminders.domain.api.reminder_parser_service import ReminderParserService
from reminders.domain.error.invalid_reminder_error import InvalidReminderError
from reminders.domain.model.parsed_reminder import ParsedReminder
from reminders.domain.utils.constants import (
    MAX_REMINDER_MINUTES,
    MIN_REMINDER_MINUTES,
    MINUTES_PER_DAY,
    MINUTES_PER_HOUR,
    REMINDER_PATTERN,
)


class ReminderParserUsecase(ReminderParserService):
    def parse(self, raw_text: str) -> ParsedReminder:
        match = REMINDER_PATTERN.match(raw_text.strip())
        if match is None:
            raise InvalidReminderError("No entendí el formato del recordatorio.")

        message = match.group("message").strip()
        amount = int(match.group("amount"))
        unit = match.group("unit").lower()

        if unit.startswith("d"):
            minutes = amount * MINUTES_PER_DAY
        elif unit.startswith("h"):
            minutes = amount * MINUTES_PER_HOUR
        else:
            minutes = amount

        if not (MIN_REMINDER_MINUTES <= minutes <= MAX_REMINDER_MINUTES):
            raise InvalidReminderError(
                f"La duración debe estar entre {MIN_REMINDER_MINUTES} minuto y "
                f"{MAX_REMINDER_MINUTES // MINUTES_PER_DAY} días."
            )

        return ParsedReminder(message=message, minutes=minutes)
