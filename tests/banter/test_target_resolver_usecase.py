from banter.domain.usecase.target_resolver_usecase import TargetResolverUsecase
from tests.banter.fakes import FakeMemberLookupPort


async def test_resolve_returns_user_id_when_member_found():
    port = FakeMemberLookupPort(members={(1, "fulano"): 42})
    usecase = TargetResolverUsecase(member_lookup_port=port)

    assert await usecase.resolve(1, "fulano") == 42


async def test_resolve_returns_none_when_member_not_found():
    usecase = TargetResolverUsecase(member_lookup_port=FakeMemberLookupPort())

    assert await usecase.resolve(1, "desconocido") is None
