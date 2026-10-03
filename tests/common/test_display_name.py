from types import SimpleNamespace

from common.infrastructure.input.tg.display_name import display_name, display_name_from_record, mention_html


def test_mention_html_tags_by_id_and_escapes_the_name():
    assert mention_html(42, "<b>x</b>") == '<a href="tg://user?id=42">&lt;b&gt;x&lt;/b&gt;</a>'


def test_display_name_prefers_username_but_tags_by_id():
    user = SimpleNamespace(id=42, username="fulano", full_name="Fulano Perez")
    assert display_name(user) == '<a href="tg://user?id=42">@fulano</a>'


def test_display_name_tags_users_without_username_by_full_name():
    user = SimpleNamespace(id=42, username=None, full_name="Fulano Perez")
    assert display_name(user) == '<a href="tg://user?id=42">Fulano Perez</a>'


def test_display_name_from_record_prefers_username():
    assert display_name_from_record(42, "fulano", "Fulano Perez") == '<a href="tg://user?id=42">@fulano</a>'


def test_display_name_from_record_uses_full_name_when_no_username():
    assert display_name_from_record(42, "", "Fulano Perez") == '<a href="tg://user?id=42">Fulano Perez</a>'


def test_display_name_from_record_falls_back_to_placeholder_when_nothing_is_stored():
    assert display_name_from_record(42, "", "") == '<a href="tg://user?id=42">alguien</a>'
