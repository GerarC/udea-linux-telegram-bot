from dependency_injector import containers, providers

from user_info.domain.usecase.user_info_usecase import UserInfoUsecase
from user_info.domain.usecase.username_resolver_usecase import UsernameResolverUsecase
from user_info.infrastructure.output.postgres.adapter.member_lookup_adapter import PostgresMemberLookupAdapter


class UserInfoContainer(containers.DeclarativeContainer):
    """Wiring for the user_info feature: aggregates UserInfoProviderPort instances contributed
    by every other feature (injected by the root container, same shape as the shared pool), plus
    its own username -> user_id lookup against the shared group_members table (for /gdb @usuario).
    """

    info_providers = providers.Dependency()
    pool = providers.Dependency()

    usecase = providers.Factory(UserInfoUsecase, providers=info_providers)

    member_lookup_port = providers.Singleton(PostgresMemberLookupAdapter, pool=pool)
    username_resolver_usecase = providers.Factory(UsernameResolverUsecase, member_lookup_port=member_lookup_port)
