from typing import Protocol

from reminders.domain.model.parsed_reminder import ParsedReminder


class ReminderParserService(Protocol):
    """Inbound port: parses the raw text after /recordar into a message + duration."""

    def parse(self, raw_text: str) -> ParsedReminder: ...
