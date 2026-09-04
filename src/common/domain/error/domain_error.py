class DomainError(Exception):
    """Base exception for domain errors in the project."""

    def __init__(self, message: str, user_message: str | None = None) -> None:
        super().__init__(message)
        # NOTE: user-facing text, kept in Spanish since the bot serves a Spanish-speaking group.
        self.user_message = user_message
