from typing import Protocol

from polls.domain.model.poll import Poll


class PollParserService(Protocol):
    """Inbound port for the polls feature: parsing/validating the raw /encuesta text."""

    def parse_poll(self, raw_text: str) -> Poll:
        """Parses '<question> | <option1> | <option2> [| ...]', raising PollValidationError if invalid."""
        ...
