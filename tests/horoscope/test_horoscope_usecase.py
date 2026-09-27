import pytest

from horoscope.domain.error.invalid_sign_error import InvalidSignError
from horoscope.domain.usecase.horoscope_usecase import FALLBACK_HOROSCOPE, HoroscopeUsecase
from horoscope.domain.utils.constants import VALID_SIGNS
from tests.horoscope.fakes import FakeHoroscopePhrasePort


async def test_raises_for_an_invalid_sign():
    usecase = HoroscopeUsecase(phrase_port=FakeHoroscopePhrasePort())

    with pytest.raises(InvalidSignError):
        await usecase.get_horoscope("no-es-un-signo")


async def test_normalizes_sign_case_accents_and_surrounding_whitespace():
    usecase = HoroscopeUsecase(phrase_port=FakeHoroscopePhrasePort(["frase"]))

    reading = await usecase.get_horoscope("  GÉMINIS  ")

    assert reading.sign == "geminis"


async def test_uses_the_fallback_text_when_no_phrases_are_available():
    usecase = HoroscopeUsecase(phrase_port=FakeHoroscopePhrasePort())

    reading = await usecase.get_horoscope("aries")

    assert reading.horoscope == FALLBACK_HOROSCOPE


async def test_same_sign_gives_the_same_reading_within_the_same_day():
    usecase = HoroscopeUsecase(phrase_port=FakeHoroscopePhrasePort(["a", "b", "c"]))

    first = await usecase.get_horoscope("leo")
    second = await usecase.get_horoscope("leo")

    assert first == second


async def test_all_signs_get_distinct_phrases_when_phrase_count_matches_sign_count():
    phrases = [chr(ord("a") + i) for i in range(len(VALID_SIGNS))]
    usecase = HoroscopeUsecase(phrase_port=FakeHoroscopePhrasePort(phrases))

    readings = [await usecase.get_horoscope(sign) for sign in VALID_SIGNS]

    assert len({reading.horoscope for reading in readings}) == len(VALID_SIGNS)


async def test_compatibility_never_matches_the_sign_itself():
    usecase = HoroscopeUsecase(phrase_port=FakeHoroscopePhrasePort())

    for sign in VALID_SIGNS:
        reading = await usecase.get_horoscope(sign)
        assert reading.compatibility != sign
