from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.ext import ContextTypes

from banter.domain.api.banter_service import BanterService
from common.application.bootstrap.container import ApplicationContainer


@inject
async def insultar_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    banter_service: BanterService = Provide[ApplicationContainer.banter.usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    if not context.args:
        await message.reply_text("Usa: /insultar @usuario")
        return

    usuario = context.args[0]
    insulto = await banter_service.insult()
    await message.reply_text(f"{usuario}, {insulto}")


@inject
async def cumplido_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    banter_service: BanterService = Provide[ApplicationContainer.banter.usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    if not context.args:
        await message.reply_text("Usa: /cumplido @usuario")
        return

    usuario = context.args[0]
    cumplido = await banter_service.compliment()
    await message.reply_text(f"{usuario}, {cumplido}")
