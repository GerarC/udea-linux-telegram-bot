from common.domain.error.domain_error import DomainError


class PackageNotFoundError(DomainError):
    """Raised when /paquete can't find the requested package in the Arch repositories."""

    def __init__(self, name: str) -> None:
        # NOTE: message is already user-facing Spanish copy explaining what's wrong.
        message = f"No encontré el paquete '{name}' en el repositorio de Arch."
        super().__init__(message, user_message=message)
