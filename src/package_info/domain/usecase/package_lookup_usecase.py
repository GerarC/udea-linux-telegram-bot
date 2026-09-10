from package_info.domain.api.package_lookup_service import PackageLookupService
from package_info.domain.error.package_not_found_error import PackageNotFoundError
from package_info.domain.model.package_info import PackageInfo
from package_info.domain.spi.arch_package_port import ArchPackagePort


class PackageLookupUsecase(PackageLookupService):
    def __init__(self, arch_port: ArchPackagePort) -> None:
        self._arch_port = arch_port

    async def lookup_package(self, name: str) -> PackageInfo:
        package = await self._arch_port.get_package(name)
        if package is None:
            raise PackageNotFoundError(name)
        return package
