import httpx

from package_info.domain.model.package_info import PackageInfo
from package_info.domain.spi.arch_package_port import ArchPackagePort
from package_info.infrastructure.output.http.utils.constants import ARCH_PACKAGE_SEARCH_URL, REQUEST_TIMEOUT_SECONDS


class ArchPackageAdapter(ArchPackagePort):
    """Implements ArchPackagePort against the official Arch Linux packages JSON API."""

    async def get_package(self, name: str) -> PackageInfo | None:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.get(ARCH_PACKAGE_SEARCH_URL, params={"name": name})
        response.raise_for_status()

        results = response.json().get("results") or []
        if not results:
            return None

        result = results[0]
        return PackageInfo(
            name=result["pkgname"],
            version=f"{result['pkgver']}-{result['pkgrel']}",
            description=result.get("pkgdesc") or "",
            repository=result.get("repo") or "",
            url=result.get("url") or "",
        )
