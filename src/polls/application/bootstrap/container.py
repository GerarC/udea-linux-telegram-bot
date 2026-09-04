from dependency_injector import containers, providers

from polls.domain.usecase.poll_usecase import PollUsecase
from polls.domain.usecase.polls_group_stats_provider import PollsGroupStatsProvider
from polls.domain.usecase.polls_user_info_provider import PollsUserInfoProvider
from polls.infrastructure.output.postgres.repository_adapter import PostgresPollRepository
from polls.infrastructure.output.postgres.schema import ensure_schema


async def _ensure_polls_schema(pool):
    await ensure_schema(pool)
    yield None


class PollsContainer(containers.DeclarativeContainer):
    """Wiring for the polls feature: builds the adapters and exposes domain.api.PollService."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_polls_schema, pool=pool)

    repository_port = providers.Singleton(PostgresPollRepository, pool=pool)

    usecase = providers.Factory(PollUsecase, repository_port=repository_port)

    user_info_provider = providers.Factory(PollsUserInfoProvider, poll_service=usecase)

    group_stats_provider = providers.Factory(PollsGroupStatsProvider, poll_service=usecase)
