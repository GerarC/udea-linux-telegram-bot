from dependency_injector import containers, providers

from activity.domain.usecase.activity_usecase import ActivityUsecase
from activity.domain.usecase.activity_user_info_provider import ActivityUserInfoProvider
from activity.infrastructure.configuration.settings import load_activity_settings
from activity.infrastructure.output.postgres.repository_adapter import PostgresActivityRepository
from activity.infrastructure.output.postgres.schema import ensure_schema

_settings = load_activity_settings()


async def _ensure_activity_schema(pool):
    await ensure_schema(pool)
    yield None


class ActivityContainer(containers.DeclarativeContainer):
    """Wiring for the activity feature: builds the adapters and exposes domain.api.ActivityService."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_activity_schema, pool=pool)

    repository_port = providers.Singleton(PostgresActivityRepository, pool=pool)

    usecase = providers.Factory(
        ActivityUsecase,
        repository_port=repository_port,
        ranking_limit=_settings.ranking_limit,
    )

    user_info_provider = providers.Factory(ActivityUserInfoProvider, activity_service=usecase)
