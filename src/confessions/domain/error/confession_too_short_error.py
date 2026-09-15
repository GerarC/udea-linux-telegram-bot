from common.domain.error.domain_error import DomainError
from confessions.domain.utils.constants import MIN_CONTENT_LENGTH


class ConfessionTooShortError(DomainError):
    """Raised when /confesar is used with content shorter than MIN_CONTENT_LENGTH."""

    def __init__(self) -> None:
        # NOTE: message is already user-facing Spanish copy explaining what's wrong.
        message = f"La confesión debe tener al menos {MIN_CONTENT_LENGTH} caracteres."
        super().__init__(message, user_message=message)
