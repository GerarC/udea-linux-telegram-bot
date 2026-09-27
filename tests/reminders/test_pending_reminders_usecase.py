from datetime import UTC, datetime

from reminders.domain.usecase.pending_reminders_usecase import PendingRemindersUsecase
from tests.reminders.fakes import FakeReminderRepository


async def test_returns_only_reminders_that_have_not_fired_yet():
    repo = FakeReminderRepository()
    pending = await repo.create_reminder(1, 42, "fulano", "pendiente", datetime.now(UTC))
    fired = await repo.create_reminder(1, 42, "fulano", "ya sonó", datetime.now(UTC))
    fired.fired = True
    usecase = PendingRemindersUsecase(repository_port=repo)

    result = await usecase.get_pending_reminders()

    assert result == [pending]
