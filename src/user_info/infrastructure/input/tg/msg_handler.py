import html
import logging

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from user_info.domain.api.user_info_service import UserInfoService
from user_info.domain.api.username_resolver_service import UsernameResolverService

logger = logging.getLogger(__name__)


def _display_name(user) -> str:
    return f"@{user.username}" if user.username else user.full_name


@inject
async def gdb_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_info_service: UserInfoService = Provide[ApplicationContainer.user_info.usecase],
    username_resolver_service: UsernameResolverService = Provide[
        ApplicationContainer.user_info.username_resolver_usecase
    ],
) -> None:
    message = update.effective_message
    if message is None:
        return

    # NOTE: reply-to-message takes priority over a tagged @username, since Telegram gives
    # us the real User straight away - a typed @username only resolves if the bot has
    # already seen that person post in this chat (see UsernameResolverService).
    reply_user = message.reply_to_message.from_user if message.reply_to_message else None
    if reply_user is not None:
        target_id = reply_user.id
        target_username = reply_user.username or reply_user.full_name
        display_name = _display_name(reply_user)
    elif context.args:
        typed_username = " ".join(context.args).lstrip("@")
        target_id = await username_resolver_service.resolve_username(message.chat_id, typed_username)
        target_username = typed_username
        display_name = f"@{typed_username}"
    else:
        user = update.effective_user
        if user is None:
            return
        target_id = user.id
        target_username = user.username or user.full_name
        display_name = _display_name(user)

    name = html.escape(display_name)
    info = await user_info_service.get_user_info(message.chat_id, target_id, target_username)
    if not info.sections:
        await message.reply_text(f"Todavía no hay información registrada de {name}.")
        return

    logger.info("User info viewed", extra={"event": "user_info_viewed", "chat_id": message.chat_id, "target_id": target_id})
    lines = [f"🐛 <b>Debugueando a {name}</b>", ""]
    for section in info.sections:
        lines.append(f"<b>{html.escape(section.title)}</b>")
        lines.extend(html.escape(line) for line in section.lines)
        lines.append("")
    await message.reply_text("\n".join(lines).rstrip(), parse_mode=ParseMode.HTML)
