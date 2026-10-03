from datetime import UTC, datetime

from telegram import Chat, Message, MessageEntity, User

from common.infrastructure.input.tg.mentioned_user import mentioned_user

CHAT = Chat(id=1, type="supergroup")
SENDER = User(id=1, first_name="Yo", is_bot=False)


def _message(text: str, entities: list[MessageEntity]) -> Message:
    return Message(message_id=1, date=datetime.now(UTC), chat=CHAT, from_user=SENDER, text=text, entities=entities)


def test_returns_the_user_of_a_text_mention():
    target = User(id=42, first_name="Camilo", is_bot=False)
    message = _message(
        "/halagar Camilo",
        [
            MessageEntity(type=MessageEntity.BOT_COMMAND, offset=0, length=8),
            MessageEntity(type=MessageEntity.TEXT_MENTION, offset=9, length=6, user=target),
        ],
    )

    assert mentioned_user(message) == target


def test_ignores_plain_at_mentions_and_returns_none_without_entities():
    plain = _message(
        "/halagar @fulano",
        [
            MessageEntity(type=MessageEntity.BOT_COMMAND, offset=0, length=8),
            MessageEntity(type=MessageEntity.MENTION, offset=9, length=7),
        ],
    )

    assert mentioned_user(plain) is None
    assert mentioned_user(_message("/halagar", [])) is None
