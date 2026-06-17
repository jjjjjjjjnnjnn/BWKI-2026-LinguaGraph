"""
Abstract base class for LLM providers.

All providers must implement the `extract` method.
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract LLM provider interface."""

    @abstractmethod
    def extract(self, prompt: str, system: str = "") -> str:
        """
        Call LLM and return raw text response.

        Args:
            prompt: User prompt (the student answer + instructions)
            system: System prompt (role definition)

        Returns:
            Raw LLM response text (expected to be JSON)

        Raises:
            ConnectionError: If LLM is unreachable
            ValueError: If response is invalid
        """
        raise NotImplementedError

    def is_available(self) -> bool:
        """Check if the provider is reachable."""
        try:
            self.extract("test", "Reply with OK")
            return True
        except Exception:
            return False
