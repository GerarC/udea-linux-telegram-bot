from typing import Protocol

from package_info.domain.model.package_info import PackageInfo


class ArchPackagePort(Protocol):
    """Outbound port for looking up a package in the Arch Linux repositories."""

    async def get_package(self, name: str) -> PackageInfo | None: ...
