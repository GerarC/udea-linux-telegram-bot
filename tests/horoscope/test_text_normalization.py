from horoscope.domain.utils.text_normalization import strip_accents


def test_strip_accents_removes_diacritics():
    assert strip_accents("géminis") == "geminis"


def test_strip_accents_leaves_plain_ascii_untouched():
    assert strip_accents("aries") == "aries"
