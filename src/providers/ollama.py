"""
Ollama Provider

Calls Ollama via its OpenAI-compatible API endpoint.
Default: http://127.0.0.1:11434/v1

Setup:
  1. Install Ollama: https://ollama.com
  2. Pull model: ollama pull qwen3:8b
  3. Ollama runs automatically on localhost:11434
"""

from openai import OpenAI
from .base import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider (via OpenAI-compatible endpoint)."""

    def __init__(self, config: dict = None):
        config = config or {}
        self.base_url = config.get("base_url", "http://127.0.0.1:11434/v1")
        self.model = config.get("model", "qwen3:8b")
        self.client = OpenAI(
            base_url=self.base_url,
            api_key="ollama"  # Ollama doesn't need a real key
        )

    def extract(self, prompt: str, system: str = "") -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        # /no_think disables Qwen3 thinking mode for faster responses
        messages.append({"role": "user", "content": f"/no_think\n{prompt}"})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1,
            max_tokens=1000
        )

        content = response.choices[0].message.content
        # Strip thinking tags if present (Qwen3 models)
        if "<think>" in content and "</think>" in content:
            content = content.split("</think>")[-1].strip()
        elif content.startswith("<think>"):
            # Thinking tag not closed - take everything after
            parts = content.split("</think>", 1)
            content = parts[-1].strip() if len(parts) > 1 else ""
        return content

    def __repr__(self):
        return f"OllamaProvider(model={self.model}, url={self.base_url})"
