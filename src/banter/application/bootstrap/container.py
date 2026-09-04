from dependency_injector import containers, providers

from banter.domain.usecase.banter_usecase import BanterUsecase
from banter.infrastructure.output.postgres.repository_adapter import PostgresBanterRepository
from banter.infrastructure.output.postgres.schema import ensure_schema


async def _ensure_banter_schema(pool):
    await ensure_schema(pool)
    yield None


class BanterContainer(containers.DeclarativeContainer):
    """Wiring for the banter feature: builds the adapters and exposes domain.api.BanterService."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_banter_schema, pool=pool)

    repository_port = providers.Singleton(PostgresBanterRepository, pool=pool)

    usecase = providers.Factory(BanterUsecase, phrase_port=repository_port)
