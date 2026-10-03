import pytest

from confessions.domain.error.confession_not_found_error import ConfessionNotFoundError
from confessions.domain.usecase.confession_deletion_usecase import ConfessionDeletionUsecase
from tests.confessions.fakes import FakeConfessionRepository


async def test_delete_rejected_when_not_admin():
    repo = FakeConfessionRepository()
    confession = await repo.create_confession(1, 42, "fulano", "fulano", "x" * 20)
    usecase = ConfessionDeletionUsecase(repository_port=repo)

    result = await usecase.delete_confession(chat_id=1, confession_id=confession.id, requester_is_admin=False)

    assert result is None
    assert repo.confessions[confession.id].is_deleted is False


async def test_delete_accepted_when_admin():
    repo = FakeConfessionRepository()
    confession = await repo.create_confession(1, 42, "fulano", "fulano", "x" * 20)
    usecase = ConfessionDeletionUsecase(repository_port=repo)

    result = await usecase.delete_confession(chat_id=1, confession_id=confession.id, requester_is_admin=True)

    assert result.id == confession.id
    assert repo.confessions[confession.id].is_deleted is True


async def test_delete_raises_when_confession_not_found():
    repo = FakeConfessionRepository()
    usecase = ConfessionDeletionUsecase(repository_port=repo)

    with pytest.raises(ConfessionNotFoundError):
        await usecase.delete_confession(chat_id=1, confession_id=999, requester_is_admin=True)


async def test_delete_raises_when_confession_belongs_to_another_chat():
    repo = FakeConfessionRepository()
    confession = await repo.create_confession(1, 42, "fulano", "fulano", "x" * 20)
    usecase = ConfessionDeletionUsecase(repository_port=repo)

    with pytest.raises(ConfessionNotFoundError):
        await usecase.delete_confession(chat_id=999, confession_id=confession.id, requester_is_admin=True)
