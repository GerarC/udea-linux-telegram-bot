from dependency_injector import containers, providers

from package_info.domain.usecase.package_lookup_usecase import PackageLookupUsecase
from package_info.infrastructure.output.http.adapter.arch_package_adapter import ArchPackageAdapter


class PackageInfoContainer(containers.DeclarativeContainer):
    """Wiring for the package_info feature: no shared pool, calls the Arch Linux HTTP API."""

    arch_port = providers.Singleton(ArchPackageAdapter)

    package_lookup_usecase = providers.Factory(PackageLookupUsecase, arch_port=arch_port)
