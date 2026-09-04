import html

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from news.domain.api.news_service import NewsService


@inject
async def on_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    news_service: NewsService = Provide[ApplicationContainer.news.usecase],
) -> None:
    message = update.effective_message
    if message is None or not message.text:
        return

    item = await news_service.handle_message(message.chat_id, message.text)
    if item is None:
        return

    text_body = (
        f"📰 <b>{html.escape(item.title)}</b>\n"
        f"<i>{html.escape(item.source)}</i>\n"
        f"{html.escape(item.link)}"
    )
    await message.reply_text(text_body, parse_mode=ParseMode.HTML)
