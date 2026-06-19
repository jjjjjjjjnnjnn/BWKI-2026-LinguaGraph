"""
Provider Factory & Router Setup

Creates a fully configured TaskRouter from config.yaml.
This is the ONLY entry point the rest of the project uses.

Usage:
    from src.providers import create_router
    router = create_router()
    response = router.route(TaskRequest(task="concept_extraction", text="..."))
"""

import logging
from pathlib import Path
from typing import Optional

from src.models import TaskType
from .base import LLMProvider
from .mock import MockProvider
from .router import TaskRouter

logger = logging.getLogger(__name__)


def load_config(path: Optional[str] = None) -> dict:
    """Load config.yaml."""
    import yaml
    if path is None:
        path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.warning("Config file not found at %s — using defaults", path)
        return {}
    except yaml.YAMLError as e:
        logger.error("Config file parse error: %s", e)
        return {}


def create_provider(name: str, provider_config: dict) -> LLMProvider:
    """Create a single provider by name."""
    if name == "openai":
        from .openai import OpenAIProvider
        return OpenAIProvider(provider_config)
    elif name == "ollama":
        from .ollama import OllamaProvider
        return OllamaProvider(provider_config)
    elif name == "local":
        from .local import LocalProvider
        return LocalProvider(provider_config)
    elif name == "mock":
        return MockProvider(provider_config)
    else:
        raise ValueError(f"Unknown provider: {name}. Supported: openai, ollama, local, mock")


def create_router(config: Optional[dict] = None) -> TaskRouter:
    """
    Create a fully configured TaskRouter from config.

    Config structure (config.yaml):
        llm:
          providers:
            research: {type: openai, ...}
            runtime:  {type: local, ...}
          routing:
            concept_extraction: research
            npc_dialogue: runtime
    """
    if config is None:
        config = load_config()

    llm_config = config.get("llm", {})
    router = TaskRouter(config)

    # Create all configured providers
    providers = {}
    for name, cfg in llm_config.get("providers", {}).items():
        try:
            providers[name] = create_provider(cfg["type"], cfg)
        except Exception as e:
            print(f"  [WARN] Failed to create provider '{name}': {e}")

    # Always add mock as fallback
    if "mock" not in providers:
        providers["mock"] = MockProvider()

    # Apply routing rules
    for task_name, provider_name in llm_config.get("routing", {}).items():
        task_type = _parse_task_type(task_name)
        if task_type and provider_name in providers:
            router.register(task_type, providers[provider_name])

    # Set defaults (fallback chain)
    for name in llm_config.get("defaults", ["mock"]):
        if name in providers:
            router.set_default(providers[name])

    return router


def _parse_task_type(name: str) -> TaskType:
    """Parse string to TaskType."""
    try:
        return TaskType(name)
    except ValueError:
        return None


# Legacy support — old get_provider() that returns a single provider
def get_provider(config: Optional[dict] = None) -> LLMProvider:
    """
    Returns the primary available provider for backward compatibility.

    Reads llm.defaults chain from config.yaml and returns the first
    available provider. Falls back to MockProvider if nothing is available.

    Prefer create_router() for new code.
    """
    if config is None:
        config = load_config()

    llm_config = config.get("llm", {})
    providers_config = llm_config.get("providers", {})
    defaults_chain = llm_config.get("defaults", ["mock"])

    # Try each configured provider in defaults chain
    for name in defaults_chain:
        if name in providers_config:
            cfg = providers_config[name]
            try:
                provider = create_provider(cfg["type"], cfg)
                if provider.is_available():
                    return provider
            except Exception:
                continue

    # Ultimate fallback: MockProvider (always works)
    return MockProvider()
