import pytest

from reminders.domain.error.invalid_reminder_error import InvalidReminderError
from reminders.domain.usecase.reminder_parser_usecase import ReminderParserUsecase
from reminders.domain.utils.constants import MAX_REMINDER_MINUTES, MINUTES_PER_DAY, MINUTES_PER_HOUR


def test_parses_minutes():
    usecase = ReminderParserUsecase()

    parsed = usecase.parse("sacar la basura en 30 min")

    assert parsed.message == "sacar la basura"
    assert parsed.minutes == 30


def test_parses_hours():
    usecase = ReminderParserUsecase()

    parsed = usecase.parse("reunión en 2 horas")

    assert parsed.minutes == 2 * MINUTES_PER_HOUR


def test_parses_days():
    usecase = ReminderParserUsecase()

    parsed = usecase.parse("pagar la renta en 3 dias")

    assert parsed.minutes == 3 * MINUTES_PER_DAY


def test_rejects_text_that_does_not_match_the_expected_syntax():
    usecase = ReminderParserUsecase()

    with pytest.raises(InvalidReminderError):
        usecase.parse("esto no tiene el formato correcto")


def test_rejects_a_duration_over_the_max():
    usecase = ReminderParserUsecase()
    days = MAX_REMINDER_MINUTES // MINUTES_PER_DAY + 1

    with pytest.raises(InvalidReminderError):
        usecase.parse(f"algo en {days} dias")


def test_rejects_zero_minutes():
    usecase = ReminderParserUsecase()

    with pytest.raises(InvalidReminderError):
        usecase.parse("algo en 0 min")
