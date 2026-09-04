from dependency_injector import containers, providers

from user_info.domain.usecase.user_info_usecase import UserInfoUsecase


class UserInfoContainer(containers.DeclarativeContainer):
    """Wiring for the user_info feature: aggregates UserInfoProviderPort instances contributed
    by every other feature (injected by the root container, same shape as the shared pool).
    """

    info_providers = providers.Dependency()

    usecase = providers.Factory(UserInfoUsecase, providers=info_providers)
