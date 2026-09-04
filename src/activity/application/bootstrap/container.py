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
    # NOTE: providers that want to add a line to /stats_grupo (e.g. polls) - see
    # common/domain/spi/group_stats_provider_port.py. Defaults to empty so this
    # container doesn't hard-require a feature it knows nothing about.
    group_stats_providers = providers.Dependency(default=[])

    schema_ready = providers.Resource(_ensure_activity_schema, pool=pool)

    repository_port = providers.Singleton(PostgresActivityRepository, pool=pool)

    usecase = providers.Factory(
        ActivityUsecase,
        repository_port=repository_port,
        ranking_limit=_settings.ranking_limit,
        timezone=_settings.timezone,
        group_stats_providers=group_stats_providers,
    )

    user_info_provider = providers.Factory(ActivityUserInfoProvider, activity_service=usecase)
