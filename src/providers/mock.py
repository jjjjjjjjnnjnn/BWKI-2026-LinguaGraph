"""
Mock Provider — returns deterministic responses for testing.

No model required. Useful for:
- Testing pipeline without API keys
- CI/CD integration tests
- Pipeline development offline
"""

import time

from src.models import TaskRequest, TaskResponse, TaskType
from .base import LLMProvider


MOCK_RESPONSES = {
    TaskType.CONCEPT_EXTRACTION: (
        '{"concepts": ["freedom", "choice", "responsibility"], '
        '"relations": [{"source": "freedom", "target": "choice", "type": "enables"}]}'
    ),
    TaskType.RELATION_EXTRACTION: (
        '{"relations": [{"source": "freedom", "target": "responsibility", "type": "requires"}]}'
    ),
    TaskType.NPC_DIALOGUE: (
        '{"dialogue": "Hello traveler.", "emotion": "neutral"}'
    ),
    TaskType.BIOGRAPHY: (
        "In this life, you helped 10 villagers and built a school."
    ),
}


class MockProvider(LLMProvider):
    """Mock provider — deterministic responses, no model needed."""

    def __init__(self, config: dict = None):
        self._available = True

    def generate(self, request: TaskRequest) -> TaskResponse:
        start = time.time()
        # Simulate small delay
        elapsed = (time.time() - start) * 1000

        raw = MOCK_RESPONSES.get(request.task, f"[mock response for {request.task}]")

        return TaskResponse(
            task=request.task,
            raw_text=raw,
            confidence=0.5,
            tokens_in=len(request.text.split()),
            tokens_out=len(raw.split()),
            latency_ms=elapsed,
        )

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool):
        self._available = available

    def __repr__(self):
        return "MockProvider()"
