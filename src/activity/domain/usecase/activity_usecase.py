import asyncio
import logging
from datetime import date, datetime
from zoneinfo import ZoneInfo

from activity.domain.model.group_stats import GroupStats
from activity.domain.model.monthly_ranking_entry import MonthlyRankingEntry
from activity.domain.model.user_activity import UserActivity
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from activity.domain.utils.constants import DEFAULT_RANKING_LIMIT, DEFAULT_TIMEZONE
from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort


def _previous_month(period_month: date) -> date:
    if period_month.month == 1:
        return date(period_month.year - 1, 12, 1)
    return date(period_month.year, period_month.month - 1, 1)


class ActivityUsecase:
    def __init__(
        self,
        repository_port: ActivityRepositoryPort,
        ranking_limit: int = DEFAULT_RANKING_LIMIT,
        timezone: str = DEFAULT_TIMEZONE,
        group_stats_providers: list[GroupStatsProviderPort] | None = None,
    ) -> None:
        self._repository_port = repository_port
        self._ranking_limit = ranking_limit
        self._zone = ZoneInfo(timezone)
        self._group_stats_providers = group_stats_providers or []

    def _now(self) -> datetime:
        return datetime.now(self._zone)

    def _current_month(self) -> date:
        now = self._now()
        return date(now.year, now.month, 1)

    async def register_message(self, chat_id: int, user_id: int, username: str) -> None:
        now = self._now()
        period_month = date(now.year, now.month, 1)
        await self._repository_port.register_message(
            chat_id, user_id, username, period_month, now.hour, now.weekday()
        )

    async def get_monthly_ranking(self, chat_id: int, limit: int | None = None) -> list[MonthlyRankingEntry]:
        current_month = self._current_month()
        # NOTE: independent reads, run concurrently instead of round-tripping twice in serial.
        current_ranking, previous_ranking = await asyncio.gather(
            self._repository_port.get_monthly_ranking(chat_id, current_month, limit or self._ranking_limit),
            self._repository_port.get_monthly_ranking(chat_id, _previous_month(current_month)),
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

    async def get_all_time_ranking(self, chat_id: int, limit: int | None = None) -> list[UserActivity]:
        return await self._repository_port.get_all_time_ranking(chat_id, limit or self._ranking_limit)

    async def get_monthly_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        return await self._repository_port.get_monthly_stats(chat_id, user_id, self._current_month())

    async def get_all_time_stats(self, chat_id: int, user_id: int) -> tuple[int, int] | None:
        return await self._repository_port.get_all_time_stats(chat_id, user_id)

    async def get_group_stats(self, chat_id: int) -> GroupStats:
        current_month = self._current_month()
        # NOTE: five independent reads (plus the provider fan-out) - run them all
        # concurrently instead of five serial round-trips to Postgres.
        (
            (messages_this_month, participants),
            messages_all_time,
            top_ranking,
            peak_hour,
            peak_weekday,
            extra_line_results,
        ) = await asyncio.gather(
            self._repository_port.get_chat_monthly_totals(chat_id, current_month),
            self._repository_port.get_chat_all_time_total(chat_id),
            self._repository_port.get_monthly_ranking(chat_id, current_month, limit=1),
            self._repository_port.get_peak_hour(chat_id),
            self._repository_port.get_peak_weekday(chat_id),
            asyncio.gather(*(self._safe_stat_line(provider, chat_id) for provider in self._group_stats_providers)),
        )

        return GroupStats(
            messages_this_month=messages_this_month,
            messages_all_time=messages_all_time,
            active_participants_this_month=participants,
            top_user_this_month=top_ranking[0] if top_ranking else None,
            peak_hour=peak_hour,
            peak_weekday=peak_weekday,
            extra_lines=[line for line in extra_line_results if line is not None],
        )

    @staticmethod
    async def _safe_stat_line(provider: GroupStatsProviderPort, chat_id: int) -> str | None:
        # NOTE: a failing provider (e.g. its DB is unreachable) only drops its own line
        # instead of failing all of /stats_grupo - same policy as UserInfoUsecase.
        try:
            return await provider.get_group_stat_line(chat_id)
        except Exception:
            logging.exception(
                "group_stats provider failed",
                extra={"event": "group_stats_provider_failed", "provider": type(provider).__name__},
            )
            return None
