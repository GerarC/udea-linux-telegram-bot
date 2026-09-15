from common.domain.error.domain_error import DomainError


class UserNotFoundError(DomainError):
    """Raised when /gdb is used tagging a @username the bot has never seen post in this chat."""

    def __init__(self, username: str) -> None:
        # NOTE: message is already user-facing Spanish copy explaining what's wrong.
        message = f"No encontré a @{username} en este grupo. Probá respondiendo (reply) su mensaje en vez de mencionarlo."
        super().__init__(message, user_message=message)
