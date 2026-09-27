from types import SimpleNamespace
from unittest.mock import AsyncMock

from telegram.error import TelegramError

from common.infrastructure.input.tg.admin_check import requester_is_admin


def _make_update_and_context(member_status: str | None = "administrator", raise_error: bool = False):
    update = SimpleNamespace(effective_user=SimpleNamespace(id=1))
    message = SimpleNamespace(chat_id=100, reply_text=AsyncMock())

    if raise_error:
        get_chat_member = AsyncMock(side_effect=TelegramError("boom"))
    else:
        get_chat_member = AsyncMock(return_value=SimpleNamespace(status=member_status))
    context = SimpleNamespace(bot=SimpleNamespace(get_chat_member=get_chat_member))

    return update, context, message


async def test_true_for_administrator():
    update, context, message = _make_update_and_context(member_status="administrator")
    assert await requester_is_admin(update, context, message) is True


async def test_true_for_creator():
    update, context, message = _make_update_and_context(member_status="creator")
    assert await requester_is_admin(update, context, message) is True


async def test_false_for_regular_member():
    update, context, message = _make_update_and_context(member_status="member")
    assert await requester_is_admin(update, context, message) is False


async def test_none_and_replies_when_telegram_api_fails():
    update, context, message = _make_update_and_context(raise_error=True)

    result = await requester_is_admin(update, context, message)

    assert result is None
    message.reply_text.assert_awaited_once()


async def test_none_when_there_is_no_effective_user():
    update = SimpleNamespace(effective_user=None)
    context = SimpleNamespace(bot=SimpleNamespace())
    message = SimpleNamespace(chat_id=100)

    assert await requester_is_admin(update, context, message) is None
