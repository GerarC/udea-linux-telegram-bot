from points.domain.model.user_points import UserPoints
from points.domain.spi.points_repository_port import PointsRepositoryPort


class FakePointsRepository(PointsRepositoryPort):
    def __init__(self) -> None:
        self.points: dict[tuple[int, int], UserPoints] = {}

    async def add_points(self, chat_id: int, user_id: int, username: str, amount: int) -> UserPoints:
        key = (chat_id, user_id)
        current = self.points.get(key)
        new_total = (current.points if current else 0) + amount
        updated = UserPoints(user_id=user_id, username=username, points=new_total)
        self.points[key] = updated
        return updated

    async def get_points(self, chat_id: int, user_id: int) -> UserPoints | None:
        return self.points.get((chat_id, user_id))

    async def get_ranking(self, chat_id: int, limit: int) -> list[UserPoints]:
        entries = [up for (c, _), up in self.points.items() if c == chat_id]
        entries.sort(key=lambda up: up.points, reverse=True)
        return entries[:limit]

    async def get_position(self, chat_id: int, user_id: int) -> int | None:
        entries = [up for (c, _), up in self.points.items() if c == chat_id]
        entries.sort(key=lambda up: up.points, reverse=True)
        for position, up in enumerate(entries, start=1):
            if up.user_id == user_id:
                return position
        return None
