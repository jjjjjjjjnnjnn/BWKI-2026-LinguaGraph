"""
LLM Provider Factory

Returns the appropriate provider based on config.yaml settings.
"""

from .base import LLMProvider
from .ollama import OllamaProvider
from .openai import OpenAIProvider


def get_provider(config: dict = None) -> LLMProvider:
    """
    Factory function to get the LLM provider.

    Args:
        config: Full config dict (loads from config.yaml if None)

    Returns:
        LLMProvider instance
    """
    if config is None:
        import yaml
        from pathlib import Path
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    llm_config = config.get("llm", {})
    provider_name = llm_config.get("provider", "ollama")

    if provider_name == "ollama":
        return OllamaProvider(llm_config.get("ollama", {}))
    elif provider_name == "openai":
        return OpenAIProvider(llm_config.get("openai", {}))
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}. Supported: ollama, openai")
