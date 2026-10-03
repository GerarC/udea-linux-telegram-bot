import asyncio
import time

from common.domain.model.user_info_section import UserInfoSection
from common.domain.spi.user_info_provider_port import UserInfoProviderPort
from tests.user_info.fakes import FakeUserInfoProvider
from user_info.domain.usecase.user_info_usecase import UserInfoUsecase


async def test_aggregates_sections_from_every_provider_in_order():
    section_a = UserInfoSection(title="A", lines=["a"])
    section_b = UserInfoSection(title="B", lines=["b"])
    usecase = UserInfoUsecase(
        providers=[FakeUserInfoProvider(section=section_a), FakeUserInfoProvider(section=section_b)]
    )

    info = await usecase.get_user_info(chat_id=1, user_id=42, username="fulano", full_name="fulano")

    assert info.sections == [section_a, section_b]
    assert info.user_id == 42
    assert info.username == "fulano"


async def test_a_provider_returning_none_contributes_nothing():
    section = UserInfoSection(title="A", lines=["a"])
    usecase = UserInfoUsecase(providers=[FakeUserInfoProvider(section=None), FakeUserInfoProvider(section=section)])

    info = await usecase.get_user_info(chat_id=1, user_id=42, username="fulano", full_name="fulano")

    assert info.sections == [section]


async def test_a_provider_raising_does_not_affect_the_others():
    section = UserInfoSection(title="A", lines=["a"])
    usecase = UserInfoUsecase(
        providers=[FakeUserInfoProvider(error=RuntimeError("boom")), FakeUserInfoProvider(section=section)]
    )

    info = await usecase.get_user_info(chat_id=1, user_id=42, username="fulano", full_name="fulano")

    assert info.sections == [section]


async def test_no_providers_means_no_sections():
    usecase = UserInfoUsecase(providers=[])

    info = await usecase.get_user_info(chat_id=1, user_id=42, username="fulano", full_name="fulano")

    assert info.sections == []


class _SlowProvider(UserInfoProviderPort):
    async def get_section(self, chat_id: int, user_id: int, username: str, full_name: str) -> UserInfoSection | None:
        await asyncio.sleep(0.05)
        return UserInfoSection(title="slow", lines=[])


async def test_providers_run_concurrently_instead_of_sequentially():
    usecase = UserInfoUsecase(providers=[_SlowProvider(), _SlowProvider(), _SlowProvider()])

    start = time.monotonic()
    await usecase.get_user_info(chat_id=1, user_id=42, username="fulano", full_name="fulano")
    elapsed = time.monotonic() - start

    # NOTE: sequential would take ~0.15s (3 x 0.05s); parallel stays close to a single sleep.
    assert elapsed < 0.12
