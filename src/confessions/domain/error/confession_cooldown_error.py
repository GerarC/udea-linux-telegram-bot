from common.domain.error.domain_error import DomainError
from confessions.domain.utils.constants import COOLDOWN_MINUTES


class ConfessionCooldownError(DomainError):
    """Raised when a user tries /confesar again before COOLDOWN_MINUTES have passed."""

    def __init__(self) -> None:
        # NOTE: message is already user-facing Spanish copy explaining what's wrong.
        message = f"Debes esperar {COOLDOWN_MINUTES} minutos entre confesión y confesión."
        super().__init__(message, user_message=message)
