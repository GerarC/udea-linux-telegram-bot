from common.domain.error.domain_error import DomainError
from reminders.domain.utils.constants import USAGE_EXAMPLE


class InvalidReminderError(DomainError):
    """Raised when /recordar's text doesn't match the expected syntax, or the duration is out of range."""

    def __init__(self, reason: str) -> None:
        # NOTE: message is already user-facing Spanish copy explaining what's wrong.
        message = f"{reason} {USAGE_EXAMPLE}"
        super().__init__(message, user_message=message)
