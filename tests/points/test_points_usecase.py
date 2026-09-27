from points.domain.usecase.points_usecase import PointsUsecase
from points.domain.usecase.ranking_usecase import RankingUsecase
from tests.points.fakes import FakePointsRepository


def _make_usecase(repo: FakePointsRepository) -> PointsUsecase:
    return PointsUsecase(repository_port=repo, ranking_service=RankingUsecase(repo))


async def test_grant_points_rejected_when_not_admin():
    repo = FakePointsRepository()
    usecase = _make_usecase(repo)

    result = await usecase.grant_points(
        chat_id=1, granter_is_admin=False, target_id=42, target_username="fulano", amount=5
    )

    assert result is None
    assert repo.points == {}


async def test_grant_points_accepted_when_admin_and_builds_ranking():
    repo = FakePointsRepository()
    usecase = _make_usecase(repo)

    result = await usecase.grant_points(
        chat_id=1, granter_is_admin=True, target_id=42, target_username="fulano", amount=5
    )

    assert result.target.points == 5
    assert len(result.ranking) == 1
    assert result.ranking[0].user_points.user_id == 42


async def test_grant_points_accumulates_across_calls_including_negative_amounts():
    repo = FakePointsRepository()
    usecase = _make_usecase(repo)

    await usecase.grant_points(chat_id=1, granter_is_admin=True, target_id=42, target_username="fulano", amount=5)
    result = await usecase.grant_points(
        chat_id=1, granter_is_admin=True, target_id=42, target_username="fulano", amount=-2
    )

    assert result.target.points == 3
