from dependency_injector import containers, providers

from activity.application.bootstrap.container import ActivityContainer
from banter.application.bootstrap.container import BanterContainer
from common.domain.usecase.user_info_usecase import UserInfoUsecase
from common.infrastructure.configuration.settings import load_settings
from common.infrastructure.output.postgres.pool import init_pool
from news.application.bootstrap.container import NewsContainer
from points.application.bootstrap.container import PointsContainer

_settings = load_settings()


class ApplicationContainer(containers.DeclarativeContainer):
    """Root container: aggregates each feature's container and shares the DB pool."""

    db_pool = providers.Resource(
        init_pool,
        host=_settings.db_host,
        port=_settings.db_port,
        database=_settings.db_name,
        user=_settings.db_user,
        password=_settings.db_password,
    )

    news = providers.Container(NewsContainer, pool=db_pool)
    points = providers.Container(PointsContainer, pool=db_pool)
    banter = providers.Container(BanterContainer, pool=db_pool)
    activity = providers.Container(ActivityContainer, pool=db_pool)

    # NOTE: /usuario_info fans out to every feature's user_info_provider. A feature that
    # has per-user data to show just adds its own provider here - see
    # common/domain/spi/user_info_provider_port.py.
    user_info_providers = providers.List(
        points.user_info_provider,
        activity.user_info_provider,
    )

    user_info_usecase = providers.Factory(UserInfoUsecase, providers=user_info_providers)
