from common.domain.error.domain_error import DomainError


class FetchingNewsError(DomainError):
    """Exception raised for errors when fetching news articles."""

    def __init__(self, message: str) -> None:
        # NOTE: user-facing text in Spanish, the bot serves a Spanish-speaking group.
        super().__init__(message, user_message="No pude traer noticias justo ahora 📰💥. Intenta más tarde.")