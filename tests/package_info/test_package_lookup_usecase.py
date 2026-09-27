import pytest

from package_info.domain.error.package_not_found_error import PackageNotFoundError
from package_info.domain.model.package_info import PackageInfo
from package_info.domain.usecase.package_lookup_usecase import PackageLookupUsecase
from tests.package_info.fakes import FakeArchPackagePort


async def test_returns_the_package_when_found():
    package = PackageInfo(name="linux", version="6.10", description="kernel", repository="core", url="https://x")
    usecase = PackageLookupUsecase(arch_port=FakeArchPackagePort({"linux": package}))

    result = await usecase.lookup_package("linux")

    assert result == package


async def test_raises_when_the_package_is_not_found():
    usecase = PackageLookupUsecase(arch_port=FakeArchPackagePort())

    with pytest.raises(PackageNotFoundError):
        await usecase.lookup_package("no-existe")
