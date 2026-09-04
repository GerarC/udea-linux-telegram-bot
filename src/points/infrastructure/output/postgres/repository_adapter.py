import asyncpg

from common.infrastructure.output.postgres.members import upsert_member
from points.domain.model.user_points import UserPoints
from points.domain.spi.points_repository_port import PointsRepositoryPort

ADD_POINTS_SQL = """
INSERT INTO autispuntos (chat_id, user_id, points)
VALUES ($1, $2, $3)
ON CONFLICT (chat_id, user_id)
DO UPDATE SET points = autispuntos.points + EXCLUDED.points
RETURNING points
"""

GET_POINTS_SQL = """
SELECT gm.user_id, gm.username, ap.points
FROM autispuntos ap
JOIN group_members gm ON gm.chat_id = ap.chat_id AND gm.user_id = ap.user_id
WHERE ap.chat_id = $1 AND ap.user_id = $2
"""

GET_RANKING_SQL = """
SELECT gm.user_id, gm.username, ap.points
FROM autispuntos ap
JOIN group_members gm ON gm.chat_id = ap.chat_id AND gm.user_id = ap.user_id
WHERE ap.chat_id = $1
ORDER BY ap.points DESC
LIMIT $2
"""


class PostgresPointsRepository(PointsRepositoryPort):
    """Implements PointsRepositoryPort against Postgres via asyncpg."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def add_points(self, chat_id: int, user_id: int, username: str, amount: int) -> UserPoints:
        async with self._pool.acquire() as conn, conn.transaction():
            await upsert_member(conn, chat_id, user_id, username)
            points = await conn.fetchval(ADD_POINTS_SQL, chat_id, user_id, amount)
        return UserPoints(user_id=user_id, username=username, points=points)

    async def get_points(self, chat_id: int, user_id: int) -> UserPoints | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(GET_POINTS_SQL, chat_id, user_id)
        if row is None:
            return None
        return UserPoints(user_id=row["user_id"], username=row["username"], points=row["points"])

    async def get_ranking(self, chat_id: int, limit: int) -> list[UserPoints]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(GET_RANKING_SQL, chat_id, limit)
        return [UserPoints(user_id=row["user_id"], username=row["username"], points=row["points"]) for row in rows]
