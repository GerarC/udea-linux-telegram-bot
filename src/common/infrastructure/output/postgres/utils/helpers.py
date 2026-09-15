import asyncpg

from common.infrastructure.output.postgres.utils.constants import FIND_MEMBER_BY_USERNAME_SQL, UPSERT_MEMBER_SQL


async def upsert_member(conn: asyncpg.Connection, chat_id: int, user_id: int, username: str) -> None:
    """Ensures a group_members row exists/is up to date for (chat_id, user_id).

    Any feature that needs to reference a user in a group should call this
    (within its own transaction) before writing rows that FK to group_members.
    """
    await conn.execute(UPSERT_MEMBER_SQL, chat_id, user_id, username)


async def find_member_by_username(pool: asyncpg.Pool, chat_id: int, username: str) -> int | None:
    """Resolves a typed @username to a user_id, for features that need to target a user
    that wasn't reached via reply-to-message (which already carries a real Telegram User).

    Only finds users the bot has already seen post in this chat (group_members is
    populated by upsert_member, called whenever a tracked message comes in).
    """
    async with pool.acquire() as conn:
        return await conn.fetchval(FIND_MEMBER_BY_USERNAME_SQL, chat_id, username)
