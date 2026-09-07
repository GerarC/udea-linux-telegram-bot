from dependency_injector import containers, providers

from activity.domain.usecase.activity_usecase import ActivityUsecase
from activity.domain.usecase.activity_user_info_provider import ActivityUserInfoProvider
from activity.domain.usecase.all_time_ranking_usecase import AllTimeRankingUsecase
from activity.domain.usecase.all_time_stats_usecase import AllTimeStatsUsecase
from activity.domain.usecase.group_stats_usecase import GroupStatsUsecase
from activity.domain.usecase.monthly_ranking_usecase import MonthlyRankingUsecase
from activity.domain.usecase.monthly_stats_usecase import MonthlyStatsUsecase
from activity.infrastructure.configuration.settings import load_activity_settings
from activity.infrastructure.output.postgres.adapter.repository_adapter import PostgresActivityRepository
from activity.infrastructure.output.postgres.schema import ensure_schema

_settings = load_activity_settings()


async def _ensure_activity_schema(pool):
    await ensure_schema(pool)
    yield None


class ActivityContainer(containers.DeclarativeContainer):
    """Wiring for the activity feature: one usecase per domain.api Protocol (one operation each)."""

    pool = providers.Dependency()
    # NOTE: providers that want to add a line to /stats_grupo (e.g. polls) - see
    # common/domain/spi/group_stats_provider_port.py. Defaults to empty so this
    # container doesn't hard-require a feature it knows nothing about.
    group_stats_providers = providers.Dependency(default=[])

    schema_ready = providers.Resource(_ensure_activity_schema, pool=pool)

    repository_port = providers.Singleton(PostgresActivityRepository, pool=pool)

    usecase = providers.Factory(
        ActivityUsecase,
        repository_port=repository_port,
        timezone=_settings.timezone,
    )

    monthly_ranking_usecase = providers.Factory(
        MonthlyRankingUsecase,
        repository_port=repository_port,
        ranking_limit=_settings.ranking_limit,
        timezone=_settings.timezone,
    )

    all_time_ranking_usecase = providers.Factory(
        AllTimeRankingUsecase,
        repository_port=repository_port,
        ranking_limit=_settings.ranking_limit,
    )

    monthly_stats_usecase = providers.Factory(
        MonthlyStatsUsecase,
        repository_port=repository_port,
        timezone=_settings.timezone,
    )

    all_time_stats_usecase = providers.Factory(AllTimeStatsUsecase, repository_port=repository_port)

    group_stats_usecase = providers.Factory(
        GroupStatsUsecase,
        repository_port=repository_port,
        timezone=_settings.timezone,
        group_stats_providers=group_stats_providers,
    )

    user_info_provider = providers.Factory(
        ActivityUserInfoProvider,
        monthly_stats_service=monthly_stats_usecase,
        all_time_stats_service=all_time_stats_usecase,
    )
