from dependency_injector import containers, providers

from banter.domain.usecase.add_compliment_usecase import AddComplimentUsecase
from banter.domain.usecase.add_insult_usecase import AddInsultUsecase
from banter.domain.usecase.banter_group_stats_provider import BanterGroupStatsProvider
from banter.domain.usecase.banter_user_info_provider import BanterUserInfoProvider
from banter.domain.usecase.compliment_usecase import ComplimentUsecase
from banter.domain.usecase.insult_usecase import InsultUsecase
from banter.domain.usecase.target_resolver_usecase import TargetResolverUsecase
from banter.domain.usecase.top_banter_stats_usecase import TopBanterStatsUsecase
from banter.domain.usecase.user_banter_stats_usecase import UserBanterStatsUsecase
from banter.infrastructure.output.postgres.adapter.member_lookup_adapter import PostgresBanterMemberLookupAdapter
from banter.infrastructure.output.postgres.adapter.repository_adapter import PostgresBanterRepository
from banter.infrastructure.output.postgres.adapter.stats_adapter import PostgresBanterStatsRepository
from banter.infrastructure.output.postgres.schema import ensure_schema


async def _ensure_banter_schema(pool):
    await ensure_schema(pool)
    yield None


class BanterContainer(containers.DeclarativeContainer):
    """Wiring for the banter feature: one usecase per domain.api Protocol (one operation each)."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_banter_schema, pool=pool)

    repository_port = providers.Singleton(PostgresBanterRepository, pool=pool)

    stats_port = providers.Singleton(PostgresBanterStatsRepository, pool=pool)

    member_lookup_port = providers.Singleton(PostgresBanterMemberLookupAdapter, pool=pool)

    insult_usecase = providers.Factory(InsultUsecase, phrase_port=repository_port, stats_port=stats_port)

    compliment_usecase = providers.Factory(ComplimentUsecase, phrase_port=repository_port, stats_port=stats_port)

    add_insult_usecase = providers.Factory(AddInsultUsecase, phrase_port=repository_port)

    add_compliment_usecase = providers.Factory(AddComplimentUsecase, phrase_port=repository_port)

    target_resolver_usecase = providers.Factory(TargetResolverUsecase, member_lookup_port=member_lookup_port)

    user_banter_stats_usecase = providers.Factory(UserBanterStatsUsecase, stats_port=stats_port)

    top_banter_stats_usecase = providers.Factory(TopBanterStatsUsecase, stats_port=stats_port)

    user_info_provider = providers.Factory(
        BanterUserInfoProvider, user_banter_stats_service=user_banter_stats_usecase
    )

    group_stats_provider = providers.Factory(
        BanterGroupStatsProvider, top_banter_stats_service=top_banter_stats_usecase
    )
