import asyncio
import logging
from zoneinfo import ZoneInfo

from activity.domain.api.group_stats_service import GroupStatsService
from activity.domain.model.group_stats import GroupStats
from activity.domain.spi.activity_repository_port import ActivityRepositoryPort
from activity.domain.utils.clock import current_month
from activity.domain.utils.constants import DEFAULT_TIMEZONE
from common.domain.spi.group_stats_provider_port import GroupStatsProviderPort


class GroupStatsUsecase(GroupStatsService):
    def __init__(
        self,
        repository_port: ActivityRepositoryPort,
        timezone: str = DEFAULT_TIMEZONE,
        group_stats_providers: list[GroupStatsProviderPort] | None = None,
    ) -> None:
        self._repository_port = repository_port
        self._zone = ZoneInfo(timezone)
        self._group_stats_providers = group_stats_providers or []

    async def get_group_stats(self, chat_id: int) -> GroupStats:
        current = current_month(self._zone)
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
            self._repository_port.get_chat_monthly_totals(chat_id, current),
            self._repository_port.get_chat_all_time_total(chat_id),
            self._repository_port.get_monthly_ranking(chat_id, current, limit=1),
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
