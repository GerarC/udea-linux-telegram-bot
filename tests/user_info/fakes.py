from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort
from user_info.domain.spi.member_lookup_port import MemberLookupPort


class FakeUserInfoProvider(UserInfoProviderPort):
    def __init__(self, section: UserInfoSection | None = None, error: Exception | None = None) -> None:
        self._section = section
        self._error = error

    async def get_section(self, chat_id: int, user_id: int, username: str) -> UserInfoSection | None:
        if self._error is not None:
            raise self._error
        return self._section


class FakeMemberLookupPort(MemberLookupPort):
    def __init__(self, members: dict[tuple[int, str], int] | None = None) -> None:
        self.members = dict(members or {})

    async def find_user_id_by_username(self, chat_id: int, username: str) -> int | None:
        return self.members.get((chat_id, username))
