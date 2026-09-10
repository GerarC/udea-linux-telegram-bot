from typing import Protocol

from package_info.domain.model.package_info import PackageInfo


class PackageLookupService(Protocol):
    """Inbound port for the package_info feature: look up a package by name."""

    async def lookup_package(self, name: str) -> PackageInfo: ...
