from package_info.domain.model.package_info import PackageInfo
from package_info.domain.spi.arch_package_port import ArchPackagePort


class FakeArchPackagePort(ArchPackagePort):
    def __init__(self, packages: dict[str, PackageInfo] | None = None) -> None:
        self.packages = dict(packages or {})

    async def get_package(self, name: str) -> PackageInfo | None:
        return self.packages.get(name)
