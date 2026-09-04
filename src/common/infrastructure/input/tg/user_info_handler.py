import html

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from common.domain.api.user_info_service import UserInfoService


def _display_name(user) -> str:
    return f"@{user.username}" if user.username else user.full_name


@inject
async def user_info_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_info_service: UserInfoService = Provide[ApplicationContainer.user_info_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    target = message.reply_to_message.from_user if message.reply_to_message else update.effective_user
    if target is None:
        return

    name = html.escape(_display_name(target))
    info = await user_info_service.get_user_info(message.chat_id, target.id, target.username or target.full_name)
    if not info.sections:
        await message.reply_text(f"Todavía no hay información registrada de {name}.")
        return

    lines = [f"👤 <b>Información de {name}</b>", ""]
    for section in info.sections:
        lines.append(f"<b>{html.escape(section.title)}</b>")
        lines.extend(html.escape(line) for line in section.lines)
        lines.append("")
    await message.reply_text("\n".join(lines).rstrip(), parse_mode=ParseMode.HTML)
