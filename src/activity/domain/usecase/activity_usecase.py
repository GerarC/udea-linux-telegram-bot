from datetime import date, datetime, timezone

from activity.domain.model.monthly_ranking_entry import MonthlyRankingEntry
from activity.domain.model.user_activity import UserActivity
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from activity.domain.utils.constants import DEFAULT_RANKING_LIMIT


def _current_month() -> date:
    now = datetime.now(timezone.utc)
    return date(now.year, now.month, 1)


def _previous_month(period_month: date) -> date:
    if period_month.month == 1:
        return date(period_month.year - 1, 12, 1)
    return date(period_month.year, period_month.month - 1, 1)


class ActivityUsecase:
    def __init__(self, repository_port: ActivityRepositoryPort, ranking_limit: int = DEFAULT_RANKING_LIMIT) -> None:
        self._repository_port = repository_port
        self._ranking_limit = ranking_limit

    async def register_message(self, chat_id: int, user_id: int, username: str) -> None:
        await self._repository_port.register_message(chat_id, user_id, username, _current_month())

    async def get_monthly_ranking(self, chat_id: int, limit: int | None = None) -> list[MonthlyRankingEntry]:
        current_month = _current_month()
        current_ranking = await self._repository_port.get_monthly_ranking(
            chat_id, current_month, limit or self._ranking_limit
        )

        previous_ranking = await self._repository_port.get_monthly_ranking(chat_id, _previous_month(current_month))
        previous_positions = {
            activity.user_id: position for position, activity in enumerate(previous_ranking, start=1)
        }

        return [
            MonthlyRankingEntry(
                activity=activity,
                position=position,
                previous_position=previous_positions.get(activity.user_id),
            )
            for position, activity in enumerate(current_ranking, start=1)
        ]

    async def get_all_time_ranking(self, chat_id: int, limit: int | None = None) -> list[UserActivity]:
        return await self._repository_port.get_all_time_ranking(chat_id, limit or self._ranking_limit)

    async def get_monthly_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        return await self._repository_port.get_monthly_stats(chat_id, user_id, _current_month())

    async def get_all_time_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        return await self._repository_port.get_all_time_stats(chat_id, user_id)
