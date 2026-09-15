from dependency_injector import containers, providers

from confessions.domain.usecase.confession_deletion_usecase import ConfessionDeletionUsecase
from confessions.domain.usecase.confession_listing_usecase import ConfessionListingUsecase
from confessions.domain.usecase.confession_submission_usecase import ConfessionSubmissionUsecase
from confessions.infrastructure.output.postgres.adapter.repository_adapter import PostgresConfessionRepository
from confessions.infrastructure.output.postgres.schema import ensure_schema


async def _ensure_confessions_schema(pool):
    await ensure_schema(pool)
    yield None


class ConfessionsContainer(containers.DeclarativeContainer):
    """Wiring for the confessions feature: one usecase per domain.api Protocol."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_confessions_schema, pool=pool)

    repository_port = providers.Singleton(PostgresConfessionRepository, pool=pool)

    confession_submission_usecase = providers.Factory(ConfessionSubmissionUsecase, repository_port=repository_port)
    confession_listing_usecase = providers.Factory(ConfessionListingUsecase, repository_port=repository_port)
    confession_deletion_usecase = providers.Factory(ConfessionDeletionUsecase, repository_port=repository_port)
