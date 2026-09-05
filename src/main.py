from dotenv import load_dotenv

load_dotenv()

from telegram import Update

from common.application.bootstrap.container import ApplicationContainer
from common.infrastructure.configuration.logging_config import setup_logging
from common.infrastructure.configuration.settings import load_settings
from common.infrastructure.input.tg.bot import build_application, register_commands


def main() -> None:
    settings = load_settings()
    setup_logging(settings.log_level)

    container = ApplicationContainer()
    container.wire(
        modules=[
            "news.infrastructure.input.tg.msg_handler",
            "points.infrastructure.input.tg.msg_handler",
            "banter.infrastructure.input.tg.msg_handler",
            "activity.infrastructure.input.tg.msg_handler",
            "user_info.infrastructure.input.tg.msg_handler",
            "polls.infrastructure.input.tg.msg_handler",
        ]
    )

    async def on_startup(application) -> None:
        await container.init_resources()
        await register_commands(application)

    async def on_shutdown(_app) -> None:
        await container.shutdown_resources()

    app = build_application(settings.telegram_bot_token, post_init=on_startup, post_shutdown=on_shutdown)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
