import html
import logging

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from package_info.domain.api.package_lookup_service import PackageLookupService

logger = logging.getLogger(__name__)

USAGE_TEXT = "Uso: /paquete <nombre>"


@inject
async def paquete_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    package_lookup_service: PackageLookupService = Provide[ApplicationContainer.package_info.package_lookup_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    if not context.args:
        await message.reply_text(USAGE_TEXT)
        return

    name = " ".join(context.args)
    package = await package_lookup_service.lookup_package(name)
    logger.info(
        "Package found",
        extra={"event": "package_found", "chat_id": message.chat_id, "query": name, "package": package.name},
    )

    text = (
        f"📦 <b>{html.escape(package.name)}</b> {html.escape(package.version)} "
        f"({html.escape(package.repository)})\n\n"
        f"{html.escape(package.description)}"
    )
    if package.url:
        text += f"\n\n🔗 {html.escape(package.url)}"
    await message.reply_html(text)
