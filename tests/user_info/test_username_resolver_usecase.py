import pytest

from tests.user_info.fakes import FakeMemberLookupPort
from user_info.domain.error.user_not_found_error import UserNotFoundError
from user_info.domain.usecase.username_resolver_usecase import UsernameResolverUsecase


async def test_resolves_a_known_username():
    usecase = UsernameResolverUsecase(member_lookup_port=FakeMemberLookupPort(members={(1, "fulano"): 42}))

    assert await usecase.resolve_username(1, "fulano") == 42


async def test_raises_when_the_username_is_unknown():
    usecase = UsernameResolverUsecase(member_lookup_port=FakeMemberLookupPort())

    with pytest.raises(UserNotFoundError):
        await usecase.resolve_username(1, "desconocido")
