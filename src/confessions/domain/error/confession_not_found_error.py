from common.domain.error.domain_error import DomainError


class ConfessionNotFoundError(DomainError):
    """Raised when /borrar_confesion targets an id that doesn't exist in this chat."""

    def __init__(self, confession_id: int) -> None:
        # NOTE: message is already user-facing Spanish copy explaining what's wrong.
        message = f"No existe la confesión #{confession_id} en este grupo."
        super().__init__(message, user_message=message)
