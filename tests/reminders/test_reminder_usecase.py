from datetime import UTC, datetime, timedelta

from reminders.domain.model.parsed_reminder import ParsedReminder
from reminders.domain.usecase.reminder_usecase import ReminderUsecase
from tests.reminders.fakes import FakeReminderRepository


async def test_schedule_reminder_persists_with_remind_at_in_the_future():
    repo = FakeReminderRepository()
    usecase = ReminderUsecase(repository_port=repo)
    parsed = ParsedReminder(message="sacar la basura", minutes=30)

    before = datetime.now(UTC)
    reminder = await usecase.schedule_reminder(
        chat_id=1, user_id=42, username="fulano", full_name="fulano", parsed=parsed
    )
    after = datetime.now(UTC)

    assert reminder.message == "sacar la basura"
    assert before + timedelta(minutes=30) <= reminder.remind_at <= after + timedelta(minutes=30)
    assert repo.created == [reminder]
