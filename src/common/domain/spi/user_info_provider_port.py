from typing import Protocol

from common.domain.model.user_info_section import UserInfoSection


class UserInfoProviderPort(Protocol):
    """Implemented by any feature that wants to contribute a section to /info_usuario.

    Registered into common's UserInfoUsecase via a providers.List in the root
    container - see ApplicationContainer.user_info_providers.
    """

    async def get_section(self, chat_id: int, user_id: int, username: str) -> UserInfoSection | None:
        """Returns None when the feature has nothing to show for this user yet."""
        ...
