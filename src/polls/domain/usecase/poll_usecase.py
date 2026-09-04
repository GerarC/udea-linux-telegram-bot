from polls.domain.error.poll_validation_error import PollValidationError
from polls.domain.model.poll import Poll
from polls.domain.spi.poll_repository_port import PollRepositoryPort
from polls.domain.utils.constants import MAX_OPTION_LENGTH, MAX_OPTIONS, MAX_QUESTION_LENGTH, MIN_OPTIONS


class PollUsecase:
    def __init__(self, repository_port: PollRepositoryPort) -> None:
        self._repository_port = repository_port

    def parse_poll(self, raw_text: str) -> Poll:
        parts = [part.strip() for part in raw_text.split("|")]
        question = parts[0]
        options = [option for option in parts[1:] if option]

        if not question:
            raise PollValidationError(
                "Falta la pregunta. Uso: /encuesta pregunta | opción1 | opción2 [| opción3 ...]"
            )
        if len(question) > MAX_QUESTION_LENGTH:
            raise PollValidationError(f"La pregunta no puede tener más de {MAX_QUESTION_LENGTH} caracteres.")
        if len(options) < MIN_OPTIONS:
            raise PollValidationError(
                f"Necesitas al menos {MIN_OPTIONS} opciones separadas por '|'. "
                "Uso: /encuesta pregunta | opción1 | opción2"
            )
        if len(options) > MAX_OPTIONS:
            raise PollValidationError(f"No puedes tener más de {MAX_OPTIONS} opciones.")
        if any(len(option) > MAX_OPTION_LENGTH for option in options):
            raise PollValidationError(f"Cada opción debe tener como máximo {MAX_OPTION_LENGTH} caracteres.")

        return Poll(question=question, options=options)

    async def record_poll(self, chat_id: int, user_id: int, username: str, question: str) -> None:
        await self._repository_port.save_poll(chat_id, user_id, username, question)

    async def get_poll_count(self, chat_id: int, user_id: int) -> int:
        return await self._repository_port.get_poll_count(chat_id, user_id)

    async def get_chat_poll_count(self, chat_id: int) -> int:
        return await self._repository_port.get_chat_poll_count(chat_id)
