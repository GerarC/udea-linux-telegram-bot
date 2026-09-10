from dependency_injector import containers, providers

from reminders.domain.usecase.pending_reminders_usecase import PendingRemindersUsecase
from reminders.domain.usecase.reminder_firing_usecase import ReminderFiringUsecase
from reminders.domain.usecase.reminder_parser_usecase import ReminderParserUsecase
from reminders.domain.usecase.reminder_usecase import ReminderUsecase
from reminders.infrastructure.output.postgres.adapter.repository_adapter import PostgresReminderRepository
from reminders.infrastructure.output.postgres.schema import ensure_schema


async def _ensure_reminders_schema(pool):
    await ensure_schema(pool)
    yield None


class RemindersContainer(containers.DeclarativeContainer):
    """Wiring for the reminders feature: parsing + persistence, one usecase per Protocol."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_reminders_schema, pool=pool)

    repository_port = providers.Singleton(PostgresReminderRepository, pool=pool)

    reminder_parser_usecase = providers.Factory(ReminderParserUsecase)
    reminder_usecase = providers.Factory(ReminderUsecase, repository_port=repository_port)
    reminder_firing_usecase = providers.Factory(ReminderFiringUsecase, repository_port=repository_port)
    pending_reminders_usecase = providers.Factory(PendingRemindersUsecase, repository_port=repository_port)
