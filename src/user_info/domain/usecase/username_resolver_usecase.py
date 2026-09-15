from user_info.domain.api.username_resolver_service import UsernameResolverService
from user_info.domain.error.user_not_found_error import UserNotFoundError
from user_info.domain.spi.member_lookup_port import MemberLookupPort


class UsernameResolverUsecase(UsernameResolverService):
    def __init__(self, member_lookup_port: MemberLookupPort) -> None:
        self._member_lookup_port = member_lookup_port

    async def resolve_username(self, chat_id: int, username: str) -> int:
        user_id = await self._member_lookup_port.find_user_id_by_username(chat_id, username)
        if user_id is None:
            raise UserNotFoundError(username)
        return user_id
