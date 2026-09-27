from types import SimpleNamespace

from common.infrastructure.input.tg.display_name import display_name, display_name_from_record


def test_display_name_prefers_username():
    user = SimpleNamespace(username="fulano", full_name="Fulano Perez")
    assert display_name(user) == "@fulano"


def test_display_name_falls_back_to_full_name():
    user = SimpleNamespace(username=None, full_name="Fulano Perez")
    assert display_name(user) == "Fulano Perez"


def test_display_name_from_record_prefers_username():
    assert display_name_from_record(42, "fulano") == "@fulano"


def test_display_name_from_record_falls_back_to_user_id():
    assert display_name_from_record(42, "") == "42"
