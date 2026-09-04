from common.domain.error.domain_error import DomainError


class PollValidationError(DomainError):
    """Raised when /encuesta is used with an invalid question or option set."""

    def __init__(self, message: str) -> None:
        # NOTE: message is already user-facing Spanish copy explaining what's wrong.
        super().__init__(message, user_message=message)
