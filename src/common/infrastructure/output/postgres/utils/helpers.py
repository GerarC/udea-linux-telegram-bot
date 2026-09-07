import asyncpg

from common.infrastructure.output.postgres.utils.constants import UPSERT_MEMBER_SQL


async def upsert_member(conn: asyncpg.Connection, chat_id: int, user_id: int, username: str) -> None:
    """Ensures a group_members row exists/is up to date for (chat_id, user_id).

    Any feature that needs to reference a user in a group should call this
    (within its own transaction) before writing rows that FK to group_members.
    """
    await conn.execute(UPSERT_MEMBER_SQL, chat_id, user_id, username)
