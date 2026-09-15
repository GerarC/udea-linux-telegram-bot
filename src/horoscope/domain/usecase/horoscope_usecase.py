from datetime import datetime
from zoneinfo import ZoneInfo

from horoscope.domain.api.horoscope_service import HoroscopeService
from horoscope.domain.error.invalid_sign_error import InvalidSignError
from horoscope.domain.model.horoscope_reading import HoroscopeReading
from horoscope.domain.spi.horoscope_phrase_port import HoroscopePhrasePort
from horoscope.domain.utils.constants import (
    LUCKY_COLORS,
    LUCKY_NUMBER_MAX,
    LUCKY_NUMBER_MIN,
    LUCKY_TIMES,
    MOODS,
    TIMEZONE,
    VALID_SIGNS,
)
from horoscope.domain.utils.deterministic_pick import deterministic_choice, deterministic_index, deterministic_permutation
from horoscope.domain.utils.text_normalization import strip_accents

FALLBACK_HOROSCOPE = "las estrellas están en mantenimiento programado, intenta más tarde"


class HoroscopeUsecase(HoroscopeService):
    def __init__(self, phrase_port: HoroscopePhrasePort) -> None:
        self._phrase_port = phrase_port

    async def get_horoscope(self, sign: str) -> HoroscopeReading:
        normalized = strip_accents(sign.strip().lower())
        if normalized not in VALID_SIGNS:
            raise InvalidSignError(sign)

        today = datetime.now(ZoneInfo(TIMEZONE)).date().isoformat()

        phrase_count = await self._phrase_port.get_phrase_count()
        horoscope_text = FALLBACK_HOROSCOPE
        if phrase_count:
            # NOTE: one shuffle per day shared by all signs, instead of an independent
            # pick per sign, so the 12 signs never collide on the same phrase that day.
            daily_order = deterministic_permutation(f"{today}|horoscope", phrase_count)
            index = daily_order[VALID_SIGNS.index(normalized) % phrase_count]
            horoscope_text = await self._phrase_port.get_phrase(index) or FALLBACK_HOROSCOPE

        compatible_signs = [s for s in VALID_SIGNS if s != normalized]
        lucky_number = LUCKY_NUMBER_MIN + deterministic_index(
            f"{today}|{normalized}|number", LUCKY_NUMBER_MAX - LUCKY_NUMBER_MIN + 1
        )

        return HoroscopeReading(
            sign=normalized,
            horoscope=horoscope_text,
            mood=deterministic_choice(f"{today}|{normalized}|mood", MOODS),
            color=deterministic_choice(f"{today}|{normalized}|color", LUCKY_COLORS),
            lucky_number=lucky_number,
            lucky_time=deterministic_choice(f"{today}|{normalized}|time", LUCKY_TIMES),
            compatibility=deterministic_choice(f"{today}|{normalized}|compat", compatible_signs),
        )
