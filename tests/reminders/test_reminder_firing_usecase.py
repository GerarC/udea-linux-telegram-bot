from datetime import UTC, datetime

from reminders.domain.usecase.reminder_firing_usecase import ReminderFiringUsecase
from tests.reminders.fakes import FakeReminderRepository


async def test_fire_reminder_returns_the_reminder_when_still_pending():
    repo = FakeReminderRepository()
    reminder = await repo.create_reminder(1, 42, "fulano", "fulano", "algo", datetime.now(UTC))
    usecase = ReminderFiringUsecase(repository_port=repo)

    fired = await usecase.fire_reminder(reminder.id)

    assert fired is reminder
    assert reminder.fired is True


async def test_fire_reminder_returns_none_when_already_fired():
    repo = FakeReminderRepository()
    reminder = await repo.create_reminder(1, 42, "fulano", "fulano", "algo", datetime.now(UTC))
    usecase = ReminderFiringUsecase(repository_port=repo)

    await usecase.fire_reminder(reminder.id)
    second_attempt = await usecase.fire_reminder(reminder.id)

    assert second_attempt is None


async def test_fire_reminder_returns_none_for_an_unknown_id():
    usecase = ReminderFiringUsecase(repository_port=FakeReminderRepository())

    assert await usecase.fire_reminder(999) is None
