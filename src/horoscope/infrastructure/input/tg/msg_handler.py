import logging

from dependency_injector.wiring import Provide, inject
from telegram import Update
from telegram.ext import ContextTypes

from common.application.bootstrap.container import ApplicationContainer
from horoscope.domain.api.horoscope_service import HoroscopeService
from horoscope.domain.utils.constants import VALID_SIGNS

logger = logging.getLogger(__name__)

USAGE_TEXT = f"Uso: /horoscopo <signo> ({', '.join(VALID_SIGNS)})"


@inject
async def horoscopo_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    horoscope_service: HoroscopeService = Provide[ApplicationContainer.horoscope.horoscope_usecase],
) -> None:
    message = update.effective_message
    if message is None:
        return

    if not context.args:
        await message.reply_text(USAGE_TEXT)
        return

    reading = await horoscope_service.get_horoscope(context.args[0])
    logger.info(
        "Horoscope viewed",
        extra={"event": "horoscope_viewed", "chat_id": message.chat_id, "sign": reading.sign},
    )

    text = (
        f"🔮 <b>Horóscopo de {reading.sign}</b>\n\n"
        f"{reading.horoscope}\n\n"
        f"🎭 Mood: {reading.mood}\n"
        f"🎨 Color de la suerte: {reading.color}\n"
        f"🔢 Número de la suerte: {reading.lucky_number}\n"
        f"⏰ Hora de la suerte: {reading.lucky_time}\n"
        f"💞 Compatible hoy con: {reading.compatibility}"
    )
    await message.reply_html(text)
