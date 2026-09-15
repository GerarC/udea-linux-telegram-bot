from common.domain.error.domain_error import DomainError
from confessions.domain.utils.constants import MAX_CONTENT_LENGTH


class ConfessionTooLongError(DomainError):
    """Raised when /confesar is used with content longer than MAX_CONTENT_LENGTH."""

    def __init__(self) -> None:
        # NOTE: message is already user-facing Spanish copy explaining what's wrong.
        message = f"La confesión no puede tener más de {MAX_CONTENT_LENGTH} caracteres."
        super().__init__(message, user_message=message)
