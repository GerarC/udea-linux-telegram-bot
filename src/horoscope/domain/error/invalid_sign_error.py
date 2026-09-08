from common.domain.error.domain_error import DomainError
from horoscope.domain.utils.constants import VALID_SIGNS


class InvalidSignError(DomainError):
    """Raised when /horoscopo is used with a sign that isn't one of the 12 valid ones."""

    def __init__(self, sign: str) -> None:
        # NOTE: message is already user-facing Spanish copy explaining what's wrong.
        message = f"'{sign}' no es un signo válido. Usa uno de: {', '.join(VALID_SIGNS)}"
        super().__init__(message, user_message=message)
