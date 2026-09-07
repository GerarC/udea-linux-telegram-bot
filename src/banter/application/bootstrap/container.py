from dependency_injector import containers, providers

from banter.domain.usecase.compliment_usecase import ComplimentUsecase
from banter.domain.usecase.insult_usecase import InsultUsecase
from banter.infrastructure.output.postgres.adapter.repository_adapter import PostgresBanterRepository
from banter.infrastructure.output.postgres.schema import ensure_schema


async def _ensure_banter_schema(pool):
    await ensure_schema(pool)
    yield None


class BanterContainer(containers.DeclarativeContainer):
    """Wiring for the banter feature: one usecase per domain.api Protocol (one operation each)."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_banter_schema, pool=pool)

    repository_port = providers.Singleton(PostgresBanterRepository, pool=pool)

    insult_usecase = providers.Factory(InsultUsecase, phrase_port=repository_port)

    compliment_usecase = providers.Factory(ComplimentUsecase, phrase_port=repository_port)
