from datetime import UTC, datetime

from dotenv import load_dotenv

load_dotenv()

from telegram import Update

from common.application.bootstrap.container import ApplicationContainer
from common.infrastructure.configuration.logging_config import setup_logging
from common.infrastructure.configuration.settings import load_settings
from common.infrastructure.input.tg.bot import build_application, register_commands
from reminders.infrastructure.input.tg.job_handler import fire_reminder_job


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
            "horoscope.infrastructure.input.tg.msg_handler",
            "package_info.infrastructure.input.tg.msg_handler",
            "reminders.infrastructure.input.tg.msg_handler",
            "reminders.infrastructure.input.tg.job_handler",
        ]
    )

    async def _reschedule_pending_reminders(application) -> None:
        # NOTE: JobQueue is in-memory only, but Fly.io's filesystem is ephemeral -
        # every reminder still pending in Postgres must be re-armed on every restart.
        pending_reminders_usecase = await container.reminders.pending_reminders_usecase()
        pending = await pending_reminders_usecase.get_pending_reminders()
        now = datetime.now(UTC)
        for reminder in pending:
            delay_seconds = max((reminder.remind_at - now).total_seconds(), 0)
            application.job_queue.run_once(
                fire_reminder_job,
                when=delay_seconds,
                data={"reminder_id": reminder.id},
                name=f"reminder:{reminder.id}",
            )

    async def on_startup(application) -> None:
        await container.init_resources()
        await register_commands(application)
        await _reschedule_pending_reminders(application)

    async def on_shutdown(_app) -> None:
        await container.shutdown_resources()

    app = build_application(settings.telegram_bot_token, post_init=on_startup, post_shutdown=on_shutdown)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
