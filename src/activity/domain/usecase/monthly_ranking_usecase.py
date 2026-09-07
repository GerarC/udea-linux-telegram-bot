import asyncio
from zoneinfo import ZoneInfo

from activity.domain.api.monthly_ranking_service import MonthlyRankingService
from activity.domain.model.monthly_ranking_entry import MonthlyRankingEntry
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from activity.domain.utils.clock import current_month, previous_month
from activity.domain.utils.constants import DEFAULT_RANKING_LIMIT, DEFAULT_TIMEZONE


class MonthlyRankingUsecase(MonthlyRankingService):
    def __init__(
        self,
        repository_port: ActivityRepositoryPort,
        ranking_limit: int = DEFAULT_RANKING_LIMIT,
        timezone: str = DEFAULT_TIMEZONE,
    ) -> None:
        self._repository_port = repository_port
        self._ranking_limit = ranking_limit
        self._zone = ZoneInfo(timezone)

    async def get_monthly_ranking(self, chat_id: int, limit: int | None = None) -> list[MonthlyRankingEntry]:
        current = current_month(self._zone)
        # NOTE: independent reads, run concurrently instead of round-tripping twice in serial.
        current_ranking, previous_ranking = await asyncio.gather(
            self._repository_port.get_monthly_ranking(chat_id, current, limit or self._ranking_limit),
            self._repository_port.get_monthly_ranking(chat_id, previous_month(current)),
        )
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
