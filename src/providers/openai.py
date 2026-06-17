"""
OpenAI Provider

Calls OpenAI API (or any OpenAI-compatible endpoint like Gemini, DeepSeek, etc.).

Requires:
  - OPENAI_API_KEY environment variable, or
  - api_key in config.yaml
"""

import os
from openai import OpenAI
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI / compatible API provider."""

    def __init__(self, config: dict = None):
        config = config or {}
        self.model = config.get("model", "gpt-4.1-mini")
        self.api_key = config.get("api_key") or os.environ.get("OPENAI_API_KEY")
        self.base_url = config.get("base_url")  # None for OpenAI, or custom URL

        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY env var "
                "or llm.openai.api_key in config.yaml"
            )

        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url

        self.client = OpenAI(**client_kwargs)

    def extract(self, prompt: str, system: str = "") -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1
        )

        return response.choices[0].message.content

    def __repr__(self):
        return f"OpenAIProvider(model={self.model})"
