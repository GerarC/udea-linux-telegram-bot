from dependency_injector import containers, providers

from banter.application.bootstrap.container import BanterContainer
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
