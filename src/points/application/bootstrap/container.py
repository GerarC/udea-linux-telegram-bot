from dependency_injector import containers, providers

from points.domain.usecase.points_group_stats_provider import PointsGroupStatsProvider
from points.domain.usecase.points_usecase import PointsUsecase
from points.domain.usecase.points_user_info_provider import PointsUserInfoProvider
from points.domain.usecase.ranking_usecase import RankingUsecase
from points.domain.usecase.user_points_usecase import UserPointsUsecase
from points.domain.usecase.user_position_usecase import UserPositionUsecase
from points.infrastructure.configuration.settings import load_points_settings
from points.infrastructure.output.postgres.adapter.repository_adapter import PostgresPointsRepository
from points.infrastructure.output.postgres.schema import ensure_schema

_settings = load_points_settings()


async def _ensure_points_schema(pool):
    await ensure_schema(pool)
    yield None


class PointsContainer(containers.DeclarativeContainer):
    """Wiring for the points feature: one usecase per domain.api Protocol (one operation each)."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_points_schema, pool=pool)

    repository_port = providers.Singleton(PostgresPointsRepository, pool=pool)

    ranking_usecase = providers.Factory(
        RankingUsecase,
        repository_port=repository_port,
        ranking_limit=_settings.ranking_limit,
    )

    user_points_usecase = providers.Factory(UserPointsUsecase, repository_port=repository_port)

    user_position_usecase = providers.Factory(UserPositionUsecase, repository_port=repository_port)

    usecase = providers.Factory(
        PointsUsecase,
        repository_port=repository_port,
        ranking_service=ranking_usecase,
    )

    user_info_provider = providers.Factory(
        PointsUserInfoProvider,
        user_position_service=user_position_usecase,
        user_points_service=user_points_usecase,
    )

    group_stats_provider = providers.Factory(PointsGroupStatsProvider, ranking_service=ranking_usecase)
