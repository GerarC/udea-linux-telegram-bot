from dataclasses import dataclass


@dataclass
class HoroscopeReading:
    sign: str
    horoscope: str
    mood: str
    color: str
    lucky_number: int
    lucky_time: str
    compatibility: str
