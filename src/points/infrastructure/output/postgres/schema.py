import asyncpg

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS autispuntos (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    points INT NOT NULL DEFAULT 0,
    PRIMARY KEY (chat_id, user_id)
)
"""

HAS_USERNAME_COLUMN_SQL = """
SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'autispuntos' AND column_name = 'username'
)
"""

# Backfill group_members from the old autispuntos.username column before dropping it.
BACKFILL_MEMBERS_SQL = """
INSERT INTO group_members (chat_id, user_id, username)
SELECT chat_id, user_id, username FROM autispuntos
ON CONFLICT (chat_id, user_id) DO UPDATE SET username = EXCLUDED.username
"""

DROP_USERNAME_COLUMN_SQL = "ALTER TABLE autispuntos DROP COLUMN username"

ADD_MEMBER_FK_SQL = """
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'autispuntos_member_fkey'
    ) THEN
        ALTER TABLE autispuntos
        ADD CONSTRAINT autispuntos_member_fkey
        FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id, user_id);
    END IF;
END $$;
"""


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn, conn.transaction():
        await conn.execute(CREATE_TABLE_SQL)

        has_username = await conn.fetchval(HAS_USERNAME_COLUMN_SQL)
        if has_username:
            # One-time migration: keep existing points, move usernames to group_members.
            await conn.execute(BACKFILL_MEMBERS_SQL)
            await conn.execute(DROP_USERNAME_COLUMN_SQL)

        await conn.execute(ADD_MEMBER_FK_SQL)
