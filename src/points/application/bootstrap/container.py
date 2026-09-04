from dependency_injector import containers, providers

from points.domain.usecase.points_usecase import PointsUsecase
from points.infrastructure.configuration.settings import load_points_settings
from points.infrastructure.output.postgres.repository_adapter import PostgresPointsRepository
from points.infrastructure.output.postgres.schema import ensure_schema

_settings = load_points_settings()


async def _ensure_points_schema(pool):
    await ensure_schema(pool)
    yield None


class PointsContainer(containers.DeclarativeContainer):
    """Wiring for the points feature: builds the adapters and exposes domain.api.PointsService."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_points_schema, pool=pool)

    repository_port = providers.Singleton(PostgresPointsRepository, pool=pool)

    usecase = providers.Factory(
        PointsUsecase,
        repository_port=repository_port,
        ranking_limit=_settings.ranking_limit,
    )
