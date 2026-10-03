from telegram import Message, MessageEntity, User


def mentioned_user(message: Message) -> User | None:
    """The real User behind a tag picked from Telegram's mention picker.

    Users WITHOUT a username can't be typed as "@username": Telegram sends the tag as a
    `text_mention` entity that carries the full User (id included), while the visible
    text is just their name. Users with a username arrive as a plain "@username" text
    instead (entity type `mention`), which this does not cover.
    """
    for entity in message.entities or ():
        if entity.type == MessageEntity.TEXT_MENTION and entity.user is not None:
            return entity.user
    return None
