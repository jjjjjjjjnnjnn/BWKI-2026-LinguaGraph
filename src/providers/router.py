"""
Task Router — dispatches TaskRequest to the appropriate Provider.

Architecture:
    Input (TaskRequest)
        │
    Task Router
        │
        ├─ concept_extraction  →  Research Provider (OpenAI/Ollama)
        ├─ npc_dialogue        →  Runtime Provider (Local GGUF)
        ├─ translation         →  Translation Provider
        └─ annotation_assist   →  Lightweight Provider (Local 0.5B)

The Router is provider-agnostic: swapping backends is a config change,
not a code change.
"""

from typing import Optional
from src.models import TaskRequest, TaskResponse, TaskType
from src.providers.base import LLMProvider


class TaskRouter:
    """
    Routes tasks to providers based on task type and availability.

    Each task type can be mapped to a different backend.
    Fallback chain: primary → secondary → mock (never fail silently).
    """

    def __init__(self, config: dict = None):
        self.config = config or {}
        self._routes: dict[TaskType, list[LLMProvider]] = {}
        self._default_providers: list[LLMProvider] = []

    def register(self, task_type: TaskType, provider: LLMProvider, priority: int = 0):
        """Register a provider for a task type."""
        if task_type not in self._routes:
            self._routes[task_type] = []
        self._routes[task_type].append((priority, provider))
        self._routes[task_type].sort(key=lambda x: x[0])

    def set_default(self, provider: LLMProvider):
        """Set default provider (fallback for unregistered tasks)."""
        self._default_providers.append(provider)

    def route(self, request: TaskRequest) -> TaskResponse:
        """
        Route a request to the best available provider.

        Priority:
        1. Task-specific registered providers (highest priority first)
        2. Default providers
        3. Error if nothing available
        """
        # Try task-specific providers
        if request.task in self._routes:
            for _, provider in self._routes[request.task]:
                if provider.is_available():
                    return provider.generate(request)

        # Try default providers
        for provider in self._default_providers:
            if provider.is_available():
                return provider.generate(request)

        # Nothing available
        return TaskResponse(
            task=request.task,
            error=(
                f"No available provider for task '{request.task.value}'. "
                f"Check your config.yaml and ensure at least one provider is running."
            ),
        )

    def get_provider_for(self, task_type: TaskType) -> Optional[LLMProvider]:
        """Get the best available provider for a task type."""
        if task_type in self._routes:
            for _, provider in self._routes[task_type]:
                if provider.is_available():
                    return provider
        for provider in self._default_providers:
            if provider.is_available():
                return provider
        return None

    def is_task_available(self, task_type: TaskType) -> bool:
        """Check if any provider can handle this task."""
        return self.get_provider_for(task_type) is not None

    def status(self) -> dict:
        """Report all registered providers and their availability."""
        status = {}
        for task_type, providers in self._routes.items():
            status[task_type.value] = [
                {
                    "name": p.name(),
                    "available": p.is_available(),
                }
                for _, p in providers
            ]
        status["defaults"] = [
            {"name": p.name(), "available": p.is_available()}
            for p in self._default_providers
        ]
        return status
