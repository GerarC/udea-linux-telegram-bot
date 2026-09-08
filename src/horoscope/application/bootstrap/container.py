from dependency_injector import containers, providers

from horoscope.domain.usecase.horoscope_usecase import HoroscopeUsecase
from horoscope.infrastructure.output.postgres.adapter.repository_adapter import PostgresHoroscopeRepository
from horoscope.infrastructure.output.postgres.schema import ensure_schema


async def _ensure_horoscope_schema(pool):
    await ensure_schema(pool)
    yield None


class HoroscopeContainer(containers.DeclarativeContainer):
    """Wiring for the horoscope feature: one usecase for the single domain.api Protocol."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_horoscope_schema, pool=pool)

    repository_port = providers.Singleton(PostgresHoroscopeRepository, pool=pool)

    horoscope_usecase = providers.Factory(HoroscopeUsecase, phrase_port=repository_port)
