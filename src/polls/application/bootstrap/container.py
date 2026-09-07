from dependency_injector import containers, providers

from polls.domain.usecase.chat_poll_count_usecase import ChatPollCountUsecase
from polls.domain.usecase.poll_count_usecase import PollCountUsecase
from polls.domain.usecase.poll_parser_usecase import PollParserUsecase
from polls.domain.usecase.poll_recorder_usecase import PollRecorderUsecase
from polls.domain.usecase.polls_group_stats_provider import PollsGroupStatsProvider
from polls.domain.usecase.polls_user_info_provider import PollsUserInfoProvider
from polls.infrastructure.output.postgres.adapter.repository_adapter import PostgresPollRepository
from polls.infrastructure.output.postgres.schema import ensure_schema


async def _ensure_polls_schema(pool):
    await ensure_schema(pool)
    yield None


class PollsContainer(containers.DeclarativeContainer):
    """Wiring for the polls feature: one usecase per domain.api Protocol (one operation each)."""

    pool = providers.Dependency()

    schema_ready = providers.Resource(_ensure_polls_schema, pool=pool)

    repository_port = providers.Singleton(PostgresPollRepository, pool=pool)

    parser_usecase = providers.Factory(PollParserUsecase)

    recorder_usecase = providers.Factory(PollRecorderUsecase, repository_port=repository_port)

    poll_count_usecase = providers.Factory(PollCountUsecase, repository_port=repository_port)

    chat_poll_count_usecase = providers.Factory(ChatPollCountUsecase, repository_port=repository_port)

    user_info_provider = providers.Factory(PollsUserInfoProvider, poll_count_service=poll_count_usecase)

    group_stats_provider = providers.Factory(
        PollsGroupStatsProvider, chat_poll_count_service=chat_poll_count_usecase
    )
