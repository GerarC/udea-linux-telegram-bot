from dependency_injector import containers, providers

from news.application.bootstrap.container import NewsContainer


class ApplicationContainer(containers.DeclarativeContainer):
    """Root container: aggregates each feature's container."""

    news = providers.Container(NewsContainer)
