from banter.domain.api.target_resolver_service import TargetResolverService
from banter.domain.spi.member_lookup_port import MemberLookupPort


class TargetResolverUsecase(TargetResolverService):
    def __init__(self, member_lookup_port: MemberLookupPort) -> None:
        self._member_lookup_port = member_lookup_port

    async def resolve(self, chat_id: int, username: str) -> int | None:
        return await self._member_lookup_port.find_user_id_by_username(chat_id, username)
