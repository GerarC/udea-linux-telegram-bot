import pytest

from polls.domain.error.poll_validation_error import PollValidationError
from polls.domain.model.poll import Poll
from polls.domain.usecase.poll_parser_usecase import PollParserUsecase
from polls.domain.utils.constants import MAX_OPTION_LENGTH, MAX_OPTIONS, MAX_QUESTION_LENGTH, MIN_OPTIONS


def test_parses_a_valid_poll():
    usecase = PollParserUsecase()

    poll = usecase.parse_poll("¿Cuál prefieres? | Opción A | Opción B")

    assert poll == Poll(question="¿Cuál prefieres?", options=["Opción A", "Opción B"])


def test_rejects_missing_question():
    usecase = PollParserUsecase()

    with pytest.raises(PollValidationError):
        usecase.parse_poll(" | A | B")


def test_rejects_too_few_options():
    usecase = PollParserUsecase()
    options = " | ".join(["x"] * (MIN_OPTIONS - 1))

    with pytest.raises(PollValidationError):
        usecase.parse_poll(f"pregunta | {options}")


def test_accepts_exactly_the_minimum_number_of_options():
    usecase = PollParserUsecase()
    options = " | ".join(["x"] * MIN_OPTIONS)

    poll = usecase.parse_poll(f"pregunta | {options}")

    assert len(poll.options) == MIN_OPTIONS


def test_rejects_too_many_options():
    usecase = PollParserUsecase()
    options = " | ".join(f"opcion{i}" for i in range(MAX_OPTIONS + 1))

    with pytest.raises(PollValidationError):
        usecase.parse_poll(f"pregunta | {options}")


def test_rejects_question_over_the_max_length():
    usecase = PollParserUsecase()
    question = "x" * (MAX_QUESTION_LENGTH + 1)

    with pytest.raises(PollValidationError):
        usecase.parse_poll(f"{question} | A | B")


def test_rejects_an_option_over_the_max_length():
    usecase = PollParserUsecase()
    option = "x" * (MAX_OPTION_LENGTH + 1)

    with pytest.raises(PollValidationError):
        usecase.parse_poll(f"pregunta | {option} | B")
