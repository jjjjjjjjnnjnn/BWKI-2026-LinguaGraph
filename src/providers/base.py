"""
Provider Abstraction Layer — Abstract Base Class

All providers (OpenAI, Ollama, Local GGUF, WebLLM, Mock) implement
this interface. The entire pipeline only depends on `generate()`.

Key design principle:
    Input  → TaskRequest (统一)
    Output → TaskResponse (统一)
    Provider is just a swappable backend.
"""

from abc import ABC, abstractmethod
from src.models import TaskRequest, TaskResponse


class LLMProvider(ABC):
    """Abstract LLM provider — all providers implement this."""

    @abstractmethod
    def generate(self, request: TaskRequest) -> TaskResponse:
        """
        Core method: take a TaskRequest, return a TaskResponse.

        Every provider implements this one method.
        The caller never needs to know which backend is running.
        """
        ...

    def batch_generate(self, requests: list[TaskRequest]) -> list[TaskResponse]:
        """Batch processing — override if provider supports true batching."""
        return [self.generate(req) for req in requests]

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is reachable / configured."""
        ...

    def name(self) -> str:
        """Human-readable provider name."""
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"<{self.name()}>"
