from telegram import Message, Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes


async def requester_is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, message: Message) -> bool | None:
    """Checks whether the user who triggered this update is an admin of the chat.

    Returns None when the check itself couldn't be resolved - either there's no
    effective_user, or Telegram's API call failed (already replied to the user in
    that case). The caller should just return in that case, same as a validation
    failure - it does not mean "not an admin".
    """
    user = update.effective_user
    if user is None:
        return None

    try:
        member = await context.bot.get_chat_member(message.chat_id, user.id)
    except TelegramError:
        await message.reply_text("No pude verificar si eres admin del grupo. Intenta de nuevo en un momento.")
        return None
    return member.status in ("administrator", "creator")
