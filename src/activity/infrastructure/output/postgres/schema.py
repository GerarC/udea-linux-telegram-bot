import asyncpg

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS user_message_stats (
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    period_month DATE NOT NULL,
    message_count BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (chat_id, user_id, period_month),
    FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id, user_id)
)
"""

# NOTE: chat-level (not per-user), so no FK to group_members - see CLAUDE.md rule 8.
CREATE_TIMELINE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS chat_activity_timeline (
    chat_id BIGINT NOT NULL,
    hour_of_day SMALLINT NOT NULL,
    weekday SMALLINT NOT NULL,
    message_count BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (chat_id, hour_of_day, weekday)
)
"""

HAS_PERIOD_MONTH_COLUMN_SQL = """
SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'user_message_stats' AND column_name = 'period_month'
)
"""

# NOTE: this table predates monthly tracking and was never used by the deployed bot
# (feature not yet released), so dropping the pre-migration table loses no real data.
DROP_LEGACY_TABLE_SQL = "DROP TABLE IF EXISTS user_message_stats"


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        has_period_month = await conn.fetchval(HAS_PERIOD_MONTH_COLUMN_SQL)
        if not has_period_month:
            await conn.execute(DROP_LEGACY_TABLE_SQL)
        await conn.execute(CREATE_TABLE_SQL)
        await conn.execute(CREATE_TIMELINE_TABLE_SQL)
