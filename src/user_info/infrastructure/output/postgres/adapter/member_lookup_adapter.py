import asyncpg

from common.infrastructure.output.postgres.utils.helpers import find_member_by_username
from user_info.domain.spi.member_lookup_port import MemberLookupPort


class PostgresMemberLookupAdapter(MemberLookupPort):
    """Implements MemberLookupPort against the shared group_members table."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def find_user_id_by_username(self, chat_id: int, username: str) -> int | None:
        return await find_member_by_username(self._pool, chat_id, username)
