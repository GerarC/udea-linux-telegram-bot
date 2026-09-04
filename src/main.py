import logging

from dotenv import load_dotenv

load_dotenv()  # must run before importing the containers below: they read env vars at import time

from telegram import Update

from common.application.bootstrap.container import ApplicationContainer
from common.infrastructure.configuration.settings import load_settings
from common.infrastructure.input.tg.bot import build_application


def main() -> None:
    settings = load_settings()
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        level=settings.log_level,
    )

    container = ApplicationContainer()
    container.wire(modules=["news.infrastructure.input.tg.msg_handler"])

    app = build_application(settings.telegram_bot_token)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
