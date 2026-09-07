import asyncpg

from common.infrastructure.output.postgres.utils.helpers import upsert_member
from points.domain.model.user_points import UserPoints
from points.domain.spi.points_repository_port import PointsRepositoryPort
from points.infrastructure.output.postgres.utils.constants import (
    ADD_POINTS_SQL,
    GET_POINTS_SQL,
    GET_POSITION_SQL,
    GET_RANKING_SQL,
)


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

    async def get_position(self, chat_id: int, user_id: int) -> int | None:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(GET_POSITION_SQL, chat_id, user_id)
